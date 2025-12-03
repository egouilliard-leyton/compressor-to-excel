"""
FastAPI application for compressor-to-excel service.

Provides REST API endpoints for uploading ZIP files containing PDFs
and receiving Excel output with combined compressor data.
"""
import tempfile
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add parent directory to path to import extract_pdf_text
sys.path.insert(0, str(Path(__file__).parent.parent))

from extract_pdf_text import process_multiple_pdfs
from api.config import settings
from api.utils import (
    extract_zip_file,
    find_pdf_files,
    cleanup_directory,
    validate_file_size,
    sanitize_filename
)
from api.models import ErrorResponse, HealthResponse, ProcessingSummary

# Ensure temp directory exists
settings.ensure_temp_dir()

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint providing API information.
    
    Returns:
        JSONResponse: API information and available endpoints
    """
    return JSONResponse(
        content={
            "name": settings.API_TITLE,
            "version": settings.API_VERSION,
            "description": settings.API_DESCRIPTION,
            "status": "running",
            "endpoints": {
                "health": "/api/health",
                "upload": "/api/upload",
                "docs": "/api/docs",
                "redoc": "/api/redoc",
                "openapi": "/api/openapi.json"
            }
        }
    )


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Service status and version
    """
    return HealthResponse(
        status="healthy",
        version=settings.API_VERSION
    )


@app.post("/api/upload", tags=["Upload"])
async def upload_zip_file(file: UploadFile = File(..., description="ZIP file containing PDFs")):
    """
    Upload a ZIP file containing PDF files and receive Excel output.
    
    The ZIP file should contain one or more PDF files. All PDFs will be processed
    and combined into a single Excel file with Date, Consumo, and Compressor columns.
    
    Args:
        file: ZIP file upload
    
    Returns:
        Excel file download (application/vnd.openxmlformats-officedocument.spreadsheetml.sheet)
    
    Raises:
        400: Invalid ZIP file, no PDFs found, or validation error
        413: File too large
        500: Processing error
    """
    temp_zip_path = None
    extract_dir = None
    temp_excel_path = None
    
    try:
        # Validate file type
        if not file.filename or not file.filename.lower().endswith('.zip'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be a ZIP file (.zip extension)"
            )
        
        # Save uploaded file to temporary location
        temp_zip_path = Path(tempfile.mktemp(suffix='.zip', dir=settings.TEMP_DIR))
        
        # Read file content and validate size
        file_content = await file.read()
        file_size = len(file_content)
        
        if file_size > settings.MAX_ZIP_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"ZIP file size {file_size / (1024*1024):.2f} MB exceeds limit of {settings.MAX_ZIP_SIZE / (1024*1024):.2f} MB"
            )
        
        # Write to temporary file
        with open(temp_zip_path, 'wb') as f:
            f.write(file_content)
        
        # Validate ZIP file size
        validate_file_size(temp_zip_path, settings.MAX_ZIP_SIZE)
        
        # Extract ZIP file
        try:
            extract_dir = extract_zip_file(temp_zip_path)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error extracting ZIP file: {str(e)}"
            )
        
        # Find PDF files in extracted directory
        pdf_files = find_pdf_files(extract_dir)
        
        if not pdf_files:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No PDF files found in ZIP archive"
            )
        
        # Validate individual PDF sizes
        for pdf_file in pdf_files:
            try:
                validate_file_size(pdf_file, settings.MAX_PDF_SIZE)
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"PDF file {pdf_file.name} exceeds size limit: {str(e)}"
                )
        
        # Create temporary Excel file
        temp_excel_path = Path(tempfile.mktemp(suffix='.xlsx', dir=settings.TEMP_DIR))
        
        # Process PDFs using existing function
        try:
            summary = process_multiple_pdfs(pdf_files, temp_excel_path)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing PDFs: {str(e)}"
            )
        
        # Generate output filename
        output_filename = sanitize_filename(file.filename or "output.xlsx")
        if not output_filename.endswith('.xlsx'):
            output_filename = output_filename.rsplit('.', 1)[0] + '.xlsx'
        
        # Return Excel file as download
        return FileResponse(
            path=str(temp_excel_path),
            filename=output_filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f'attachment; filename="{output_filename}"'
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Unexpected error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
    finally:
        # Cleanup temporary files
        # Note: FileResponse will handle the Excel file cleanup after download
        # We'll clean up the ZIP and extraction directory immediately
        if temp_zip_path and temp_zip_path.exists():
            try:
                temp_zip_path.unlink()
            except Exception:
                pass
        
        # Cleanup extraction directory after a delay to allow file operations to complete
        if extract_dir and extract_dir.exists():
            # Schedule cleanup in background (simplified - in production use proper task queue)
            import threading
            def delayed_cleanup():
                import time
                time.sleep(settings.CLEANUP_DELAY)
                cleanup_directory(extract_dir)
            threading.Thread(target=delayed_cleanup, daemon=True).start()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)


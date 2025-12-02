<!-- 184508be-6713-46fd-b8e9-b3db6daf618d 19b9d128-c5ec-4662-b99c-6022cab0b5fd -->
# Create API for ZIP File Upload and Excel Output

## Overview

Build a REST API that allows users to upload a ZIP file containing PDF files, processes all PDFs using the existing extraction logic, and returns a single Excel file with all compressor data combined.

## Technology Choices

- **Framework**: FastAPI (modern, async support, automatic OpenAPI docs, excellent file upload handling)
- **Processing**: Synchronous (simpler for MVP, can upgrade to async later)
- **Response**: Direct file download (HTTP response with Excel file)
- **File Limits**: Configurable (default reasonable limits, can be adjusted)
- **Authentication**: None initially (can be added later)

## Implementation Details

### File Structure

```
compressor-to-excel/
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI app and routes
│   ├── models.py            # Pydantic models for request/response
│   ├── utils.py             # Helper functions (zip handling, temp files)
│   └── config.py            # Configuration settings
├── extract_pdf_text.py      # Existing extraction logic (reuse)
├── requirements.txt         # Updated with FastAPI dependencies
└── docs/
    └── api.md               # API documentation
```

### API Endpoints

#### POST /api/upload

- **Description**: Upload ZIP file and get Excel output
- **Request**: 
  - Content-Type: multipart/form-data
  - Body: `file` (ZIP file)
- **Response**: 
  - Success (200): Excel file download
  - Error (400/500): JSON error message
- **Processing Flow**:

  1. Receive ZIP file upload
  2. Validate ZIP file
  3. Extract PDFs to temporary directory
  4. Process PDFs using existing `process_multiple_pdfs()` function
  5. Return Excel file as HTTP response
  6. Clean up temporary files

#### GET /api/health

- **Description**: Health check endpoint
- **Response**: JSON with status

#### GET /api/docs

- **Description**: Automatic OpenAPI documentation (FastAPI built-in)

### Core Components

#### 1. ZIP File Handling (`api/utils.py`)

- Extract ZIP file to temporary directory
- Validate ZIP contains PDF files
- List extracted PDF files
- Clean up temporary files after processing

#### 2. API Route Handler (`api/main.py`)

- Handle file upload
- Validate file type and size
- Coordinate ZIP extraction and PDF processing
- Stream Excel file response
- Error handling and cleanup

#### 3. Configuration (`api/config.py`)

- File size limits (ZIP and individual PDFs)
- Temporary directory settings
- Processing timeouts
- All configurable via environment variables

#### 4. Request/Response Models (`api/models.py`)

- Pydantic models for validation
- Error response models
- Success response metadata

### Integration with Existing Code

- Reuse `extract_pdf_text.py` functions:
  - `process_multiple_pdfs()` - Main processing logic
  - `find_pdf_files()` - PDF discovery
  - `extract_pdf_to_worksheet()` - Individual PDF processing
- Create wrapper functions if needed for API context
- Maintain existing memory-efficient processing

### Error Handling

- **Invalid ZIP**: Return 400 with clear error message
- **No PDFs in ZIP**: Return 400 with helpful message
- **Processing errors**: Return 500 with error details
- **File too large**: Return 413 with size limit info
- **Timeout**: Return 504 if processing takes too long
- **Cleanup**: Always clean temporary files, even on errors

### Security Considerations

- Validate file types (ZIP only)
- Limit file sizes (configurable)
- Sanitize filenames
- Use temporary directories with proper permissions
- Clean up temporary files immediately after use
- Consider rate limiting for production

### Testing Strategy

- Unit tests for ZIP extraction
- Unit tests for API endpoints
- Integration tests with sample ZIP files
- Error case testing
- File size limit testing

### Documentation

- API endpoint documentation (FastAPI auto-generates OpenAPI/Swagger)
- Usage examples
- Error code reference
- Configuration guide

## Implementation Steps

1. Set up FastAPI project structure
2. Create configuration module with environment variables
3. Implement ZIP file extraction utilities
4. Create API route handlers
5. Integrate with existing PDF processing code
6. Add error handling and validation
7. Add cleanup and resource management
8. Create API documentation
9. Add health check endpoint
10. Test with sample ZIP files
11. Update requirements.txt
12. Create deployment guide

## Example Usage

```bash
# Upload ZIP file via curl
curl -X POST "http://localhost:8000/api/upload" \
  -H "accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@compressors.zip" \
  --output result.xlsx

# Python client example
import requests

with open('compressors.zip', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/upload',
        files={'file': f}
    )
    with open('output.xlsx', 'wb') as out:
        out.write(response.content)
```

## Configuration Options

- `MAX_ZIP_SIZE`: Maximum ZIP file size (default: 500MB)
- `MAX_PDF_SIZE`: Maximum individual PDF size (default: 100MB)
- `MAX_PDFS`: Maximum number of PDFs per ZIP (default: 100)
- `TEMP_DIR`: Temporary directory for extraction (default: system temp)
- `PROCESSING_TIMEOUT`: Maximum processing time in seconds (default: 3600)
- `CLEANUP_DELAY`: Delay before cleanup in seconds (default: 60)

## Future Enhancements

- Async processing with job queue (Celery/Redis)
- Progress tracking endpoint
- Authentication/authorization
- Rate limiting
- File caching
- Multiple output formats
- Batch processing status API

### To-dos

- [ ] Add openpyxl (or pandas with openpyxl) to requirements.txt
- [ ] Create process_compressor_txt.py with command-line argument parsing
- [ ] Implement function to extract compressor number from filename (COMPRESOR4 -> Compressor 4)
- [ ] Implement function to parse .txt file and extract Date and Consumo values using regex
- [ ] Implement function to write data to Excel file with Date, Consumo, and Compressor columns
- [ ] Add error handling for file I/O, malformed data, and edge cases
"""
Utility functions for ZIP file handling and temporary file management.
"""
import zipfile
import tempfile
import shutil
from pathlib import Path
from typing import List, Optional
import os

from api.config import settings


def extract_zip_file(zip_path: Path, extract_to: Optional[Path] = None) -> Path:
    """
    Extract ZIP file to a temporary directory.
    
    Args:
        zip_path: Path to the ZIP file
        extract_to: Optional directory to extract to (creates temp dir if not provided)
    
    Returns:
        Path to the extraction directory
    
    Raises:
        zipfile.BadZipFile: If file is not a valid ZIP
        ValueError: If ZIP is empty or contains no PDFs
    """
    # Validate ZIP file
    if not zip_path.exists():
        raise FileNotFoundError(f"ZIP file not found: {zip_path}")
    
    if not zipfile.is_zipfile(zip_path):
        raise zipfile.BadZipFile(f"File is not a valid ZIP: {zip_path}")
    
    # Create extraction directory
    if extract_to is None:
        extract_to = Path(tempfile.mkdtemp(dir=settings.TEMP_DIR))
    else:
        extract_to.mkdir(parents=True, exist_ok=True)
    
    # Extract ZIP file
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Validate ZIP contents
            file_list = zip_ref.namelist()
            if not file_list:
                raise ValueError("ZIP file is empty")
            
            # Check for PDF files
            pdf_files = [f for f in file_list if f.lower().endswith('.pdf')]
            if not pdf_files:
                raise ValueError("ZIP file contains no PDF files")
            
            # Check PDF count limit
            if len(pdf_files) > settings.MAX_PDFS:
                raise ValueError(
                    f"ZIP contains {len(pdf_files)} PDFs, exceeds limit of {settings.MAX_PDFS}"
                )
            
            # Extract all files
            zip_ref.extractall(extract_to)
            
            # Sanitize extracted paths (prevent zip slip attacks)
            for member in zip_ref.namelist():
                member_path = extract_to / member
                # Check if path is within extract_to directory
                try:
                    member_path.resolve().relative_to(extract_to.resolve())
                except ValueError:
                    # Path is outside extract_to, remove it
                    if member_path.exists():
                        if member_path.is_file():
                            member_path.unlink()
                        elif member_path.is_dir():
                            shutil.rmtree(member_path)
            
            return extract_to
            
    except zipfile.BadZipFile:
        raise
    except Exception as e:
        # Clean up extraction directory on error
        if extract_to.exists():
            shutil.rmtree(extract_to, ignore_errors=True)
        raise ValueError(f"Error extracting ZIP file: {str(e)}")


def find_pdf_files(directory: Path) -> List[Path]:
    """
    Find all PDF files in a directory.
    
    Args:
        directory: Directory to search
    
    Returns:
        List of Path objects for PDF files found
    """
    pdf_files = []
    
    if not directory.exists() or not directory.is_dir():
        return pdf_files
    
    # Find PDF files (case-insensitive)
    pdf_files = sorted(directory.glob("*.pdf")) + sorted(directory.glob("*.PDF"))
    
    # Remove duplicates
    pdf_files = list(dict.fromkeys(pdf_files))
    
    return pdf_files


def cleanup_directory(directory: Path, delay: Optional[int] = None):
    """
    Clean up a temporary directory.
    
    Args:
        directory: Directory to remove
        delay: Optional delay in seconds before cleanup
    """
    if delay:
        import time
        time.sleep(delay)
    
    if directory.exists() and directory.is_dir():
        try:
            shutil.rmtree(directory)
        except Exception:
            # Ignore cleanup errors
            pass


def validate_file_size(file_path: Path, max_size: int) -> bool:
    """
    Validate that a file size is within limits.
    
    Args:
        file_path: Path to file
        max_size: Maximum allowed size in bytes
    
    Returns:
        True if file size is within limit
    
    Raises:
        ValueError: If file exceeds size limit
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_size = file_path.stat().st_size
    
    if file_size > max_size:
        raise ValueError(
            f"File size {file_size / (1024*1024):.2f} MB exceeds limit of {max_size / (1024*1024):.2f} MB"
        )
    
    return True


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to prevent path traversal attacks.
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove path separators and dangerous characters
    sanitized = os.path.basename(filename)
    # Remove any remaining dangerous characters
    sanitized = "".join(c for c in sanitized if c.isalnum() or c in "._-")
    return sanitized


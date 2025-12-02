"""
Configuration settings for the API.

All settings can be configured via environment variables.
"""
import os
from pathlib import Path


class Settings:
    """API configuration settings."""
    
    # File size limits (in bytes)
    MAX_ZIP_SIZE: int = int(os.getenv("MAX_ZIP_SIZE", str(500 * 1024 * 1024)))  # 500MB default
    MAX_PDF_SIZE: int = int(os.getenv("MAX_PDF_SIZE", str(100 * 1024 * 1024)))  # 100MB default
    
    # Processing limits
    MAX_PDFS: int = int(os.getenv("MAX_PDFS", "100"))  # Maximum PDFs per ZIP
    PROCESSING_TIMEOUT: int = int(os.getenv("PROCESSING_TIMEOUT", "3600"))  # 1 hour default
    
    # Temporary directory
    TEMP_DIR: Path = Path(os.getenv("TEMP_DIR", os.path.join(os.path.sep, "tmp", "compressor-api")))
    
    # Cleanup delay (seconds to wait before cleanup)
    CLEANUP_DELAY: int = int(os.getenv("CLEANUP_DELAY", "60"))
    
    # API settings
    API_TITLE: str = "Compressor to Excel API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API for processing ZIP files containing compressor PDFs and generating Excel output"
    
    @classmethod
    def ensure_temp_dir(cls):
        """Ensure temporary directory exists and create if needed."""
        cls.TEMP_DIR.mkdir(parents=True, exist_ok=True)
        return cls.TEMP_DIR


# Global settings instance
settings = Settings()


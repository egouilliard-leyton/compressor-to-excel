"""
Pydantic models for request/response validation.
"""
from typing import Optional
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(default="healthy", description="Service status")
    version: str = Field(..., description="API version")


class ProcessingSummary(BaseModel):
    """Summary of processing results."""
    success_count: int = Field(..., description="Number of successfully processed PDFs")
    failure_count: int = Field(..., description="Number of failed PDFs")
    total_rows: int = Field(..., description="Total data rows written to Excel")
    failed_files: list = Field(default_factory=list, description="List of failed files with error messages")


# Compressor to Excel API Documentation

## Overview

The Compressor to Excel API provides a REST interface for processing ZIP files containing compressor PDF data and generating Excel output files. The API accepts ZIP archives containing one or more PDF files, extracts compressor data from each PDF, and returns a single Excel file with separate sheets for each compressor number, ensuring all data stays within Excel's row limit.

## Base URL

```
http://localhost:8001  # Default for Docker Compose
http://localhost:8000  # Default for Docker direct or local development
```

## Authentication

Currently, no authentication is required. This may be added in future versions.

## Endpoints

### Health Check

**GET** `/api/health`

Check the health status of the API service.

**Response:**

```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

**Example:**

```bash
curl http://localhost:8001/api/health  # Docker Compose
curl http://localhost:8000/api/health  # Docker direct or local
```

### Upload ZIP File

**POST** `/api/upload`

Upload a ZIP file containing PDF files and receive an Excel file with combined compressor data.

**Request:**

- **Content-Type**: `multipart/form-data`
- **Body**: Form data with `file` field containing the ZIP file

**Response:**

- **Success (200)**: Excel file download (`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`)
- **Error (400)**: Invalid ZIP file, no PDFs found, or validation error
- **Error (413)**: File too large
- **Error (500)**: Processing error

**Example using curl:**

```bash
# Docker Compose (port 8001)
curl -X POST "http://localhost:8001/api/upload" \
  -H "accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@compressors.zip" \
  --output result.xlsx

# Docker direct or local (port 8000)
curl -X POST "http://localhost:8000/api/upload" \
  -H "accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@compressors.zip" \
  --output result.xlsx
```

**Example using Python:**

```python
import requests

# Use port 8001 for Docker Compose, 8000 for Docker direct/local
api_url = 'http://localhost:8001/api/upload'

with open('compressors.zip', 'rb') as f:
    response = requests.post(
        api_url,
        files={'file': f}
    )
    
    if response.status_code == 200:
        with open('output.xlsx', 'wb') as out:
            out.write(response.content)
        print("Excel file saved successfully")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
```

**Example using JavaScript (fetch):**

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

// Use port 8001 for Docker Compose, 8000 for Docker direct/local
fetch('http://localhost:8001/api/upload', {
  method: 'POST',
  body: formData
})
.then(response => {
  if (response.ok) {
    return response.blob();
  }
  throw new Error('Upload failed');
})
.then(blob => {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'output.xlsx';
  a.click();
});
```

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Codes

- **400 Bad Request**: Invalid ZIP file, no PDFs found, file validation failed
- **413 Payload Too Large**: ZIP file or individual PDF exceeds size limit
- **500 Internal Server Error**: Processing error or unexpected server error

## File Requirements

### ZIP File Requirements

- File extension must be `.zip`
- Maximum size: 500 MB (configurable via `MAX_ZIP_SIZE` environment variable)
- Must contain at least one PDF file
- Maximum number of PDFs: 100 (configurable via `MAX_PDFS` environment variable)

### PDF File Requirements

- File extension must be `.pdf` (case-insensitive)
- Maximum size per PDF: 100 MB (configurable via `MAX_PDF_SIZE` environment variable)
- PDFs should follow the compressor data format expected by the extraction logic
- Filenames should contain compressor number pattern: `COMPRESOR<number>` (e.g., `COMPRESOR4-ABR-JUN-25.PDF`)

## Excel Output Format

The generated Excel file is organized with **separate sheets for each compressor number**. This ensures that each compressor's data stays within Excel's limit of 1,048,576 rows per sheet.

**Sheet Organization:**
- Each compressor number gets its own sheet (e.g., "Compressor 1", "Compressor 4", "Compressor 5")
- If multiple PDFs have the same compressor number, they are all combined into the same sheet
- Sheet names are sanitized to comply with Excel's naming rules (max 31 characters, no special characters)

**Each sheet contains the following columns:**

1. **Date**: Date and time in format `DD/MM/YYYY HH:MM:SS`
2. **Consumo**: Consumption value (numeric)
3. **Compressor**: Compressor identifier (e.g., "Compressor 4")

**Example:**
If you upload a ZIP containing PDFs for Compressor 1, Compressor 4, and Compressor 5, the Excel file will have three sheets:
- Sheet "Compressor 1" - Contains all data from Compressor 1 PDFs
- Sheet "Compressor 4" - Contains all data from Compressor 4 PDFs  
- Sheet "Compressor 5" - Contains all data from Compressor 5 PDFs

## Configuration

The API can be configured using environment variables:

- `MAX_ZIP_SIZE`: Maximum ZIP file size in bytes (default: 524288000 = 500MB)
- `MAX_PDF_SIZE`: Maximum individual PDF size in bytes (default: 104857600 = 100MB)
- `MAX_PDFS`: Maximum number of PDFs per ZIP (default: 100)
- `TEMP_DIR`: Temporary directory for file extraction (default: `/tmp/compressor-api`)
- `PROCESSING_TIMEOUT`: Maximum processing time in seconds (default: 3600)
- `CLEANUP_DELAY`: Delay before cleanup in seconds (default: 60)

## Running the API

### Development Mode

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API (default port 8000)
python -m api.main

# Or using uvicorn directly
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode

**Using Docker Compose (Recommended):**
```bash
docker-compose up -d
# API will be available at http://localhost:8001
```

**Using Docker directly:**
```bash
docker build -t compressor-api .
docker run -d -p 8000:8000 compressor-api
# API will be available at http://localhost:8000
```

**Using uvicorn directly:**
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: 
  - http://localhost:8001/api/docs (Docker Compose)
  - http://localhost:8000/api/docs (Docker direct or local)
- **ReDoc**: 
  - http://localhost:8001/api/redoc (Docker Compose)
  - http://localhost:8000/api/redoc (Docker direct or local)
- **OpenAPI JSON**: 
  - http://localhost:8001/api/openapi.json (Docker Compose)
  - http://localhost:8000/api/openapi.json (Docker direct or local)

## Rate Limiting

Currently, no rate limiting is implemented. This should be added for production deployments.

## Security Considerations

- File type validation (ZIP files only)
- File size limits
- Filename sanitization to prevent path traversal attacks
- Temporary file cleanup after processing
- CORS middleware configured (adjust `allow_origins` for production)

## Troubleshooting

### ZIP file is rejected

- Ensure the file has a `.zip` extension
- Verify the file is a valid ZIP archive
- Check that the file size is within limits
- Ensure the ZIP contains at least one PDF file

### No PDFs found in ZIP

- Verify PDF files have `.pdf` extension (case-insensitive)
- Check that PDFs are in the root of the ZIP (not in subdirectories)
- Ensure PDFs are not corrupted

### Processing fails

- Check PDF file format matches expected compressor data format
- Verify PDF files are not corrupted
- Check server logs for detailed error messages
- Ensure sufficient disk space in temporary directory

### File download issues

- Verify the response status code is 200
- Check that the response Content-Type is correct
- Ensure sufficient disk space for the output file

## Example Workflow

1. Prepare a ZIP file containing one or more compressor PDF files
2. Send POST request to `/api/upload` with the ZIP file
3. Receive Excel file download with combined data organized into separate sheets per compressor
4. Open Excel file to view compressor data - each compressor will have its own sheet with Date, Consumo, and Compressor columns

## Support

For issues or questions, please refer to the main project documentation or contact the development team.


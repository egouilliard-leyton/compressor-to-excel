# Tool Hub Integration Guide

This document provides comprehensive information for integrating the Compressor to Excel API into the Tool Hub platform. It explains the project, what needs to be built, and how to get everything running.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Tool Hub Requirements](#2-tool-hub-requirements)
3. [Docker Setup & Deployment](#3-docker-setup--deployment)
4. [Implementation Status](#4-implementation-status)

---

## 1. Project Overview

### Repository Location

**GitLab Repository**: https://gitlab.leyton.fr/caes/compressor-to-excel-api

This is the main repository containing all source code, documentation, and Docker configuration files for the Compressor to Excel API.

### What This Project Does

The Compressor to Excel API is a REST service that processes ZIP files containing compressor PDF data and converts them into structured Excel files. The system extracts date and consumption values from PDF files and organizes them into Excel spreadsheets with separate sheets for each compressor number.

### The Process Flow

The complete workflow follows these steps:

1. **Upload**: User uploads a ZIP file containing one or more PDF files via the API
2. **Extraction**: The API extracts the ZIP file to a temporary directory
3. **PDF Processing**: Each PDF file is processed to extract:
   - Date and time stamps (format: `DD/MM/YYYY HH:MM:SS`)
   - Consumption values (`Consumo`)
   - Compressor number (extracted from filename pattern: `COMPRESOR<number>`)
4. **Excel Generation**: All extracted data is combined into a single Excel file with:
   - Separate sheets for each compressor number
   - Three columns per sheet: Date, Consumo, Compressor
   - Automatic handling of Excel's row limit (1,048,576 rows per sheet)
5. **Download**: The generated Excel file is returned to the user as a download

### Purpose and Use Cases

This tool is designed for:
- **Data Analysis**: Converting compressor PDF reports into structured Excel format for analysis
- **Batch Processing**: Processing multiple compressor PDFs simultaneously
- **Data Consolidation**: Combining data from multiple compressors into a single file
- **Automation**: Enabling programmatic access to compressor data extraction

### Technical Architecture

The API is built using:
- **FastAPI**: Modern Python web framework for building REST APIs
- **PyMuPDF (fitz)**: Fast PDF text extraction library
- **openpyxl**: Excel file generation library
- **Docker**: Containerized deployment for easy setup and scaling

The system is designed to be:
- **Memory-efficient**: Processes large PDFs (6000+ pages) using batch processing
- **Error-resilient**: Continues processing even if some PDFs fail
- **Scalable**: Supports multiple concurrent workers via uvicorn
- **Secure**: Validates file types, sizes, and sanitizes filenames

---

## 2. Tool Hub Requirements

### Overview

The Tool Hub needs a simple, user-friendly interface that allows users to upload ZIP files and download the resulting Excel files. The UI should be straightforward and focused on the core workflow.

### UI Components Required

#### 2.1 File Upload Section

**Purpose**: Allow users to select and upload ZIP files

**Requirements**:
- File input element that accepts only `.zip` files
- Visual indication of selected file (filename display)
- File size validation feedback (show file size, warn if approaching limits)
- Drag-and-drop support (optional but recommended for better UX)

**Implementation Notes**:
- Maximum file size: 500 MB (configurable via API)
- File type restriction: Only ZIP files should be accepted
- Display file size after selection

#### 2.2 Upload Button

**Purpose**: Trigger the API call to process the uploaded file

**Requirements**:
- Disabled state when no file is selected
- Loading state during processing (disable button, show spinner)
- Clear visual feedback when clicked

**Behavior**:
- On click: Send POST request to `/api/upload` endpoint
- Include the selected ZIP file in the request as `multipart/form-data`
- Handle the response appropriately (success or error)

#### 2.3 Download Button

**Purpose**: Allow users to download the generated Excel file

**Requirements**:
- Hidden/disabled initially
- Appears after successful processing
- Triggers file download when clicked
- Shows filename of the Excel file to be downloaded

**Behavior**:
- On successful API response: Show download button with Excel filename
- On click: Trigger browser download of the Excel file
- Use the filename from API response or generate a default name

#### 2.4 Status/Loading Indicator

**Purpose**: Provide feedback during processing

**Requirements**:
- Show loading spinner/animation during API call
- Display status messages:
  - "Uploading..." during file upload
  - "Processing..." during PDF extraction and Excel generation
  - "Ready for download" when complete
- Show error messages if processing fails

#### 2.5 Error Handling Display

**Purpose**: Inform users of any errors

**Requirements**:
- Display API error messages clearly
- Handle common error scenarios:
  - Invalid file type (not a ZIP file)
  - File too large
  - No PDFs found in ZIP
  - Processing errors
  - Network errors
- Use user-friendly error messages (translate technical API errors)

### API Integration Details

#### Endpoint Configuration

**Base URL**: Configurable (default examples below)
- Docker Compose: `http://localhost:8001`
- Docker Direct: `http://localhost:8000`
- Production: Configure based on deployment

**Endpoints**:
- `POST /api/upload` - Upload ZIP file and receive Excel file
- `GET /api/health` - Health check (optional, for monitoring)

#### Request Format

```javascript
// Example JavaScript implementation
const formData = new FormData();
formData.append('file', zipFile); // zipFile is the selected file from input

fetch('http://localhost:8001/api/upload', {
  method: 'POST',
  body: formData
})
.then(response => {
  if (response.ok) {
    return response.blob(); // Excel file as blob
  }
  // Handle error response
  return response.json().then(err => {
    throw new Error(err.detail || 'Upload failed');
  });
})
.then(blob => {
  // Create download link
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'compressor-data.xlsx'; // or use filename from response headers
  a.click();
  window.URL.revokeObjectURL(url);
})
.catch(error => {
  // Display error message to user
  console.error('Error:', error);
});
```

#### Response Handling

**Success Response (200)**:
- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- Body: Excel file binary data
- Headers: `Content-Disposition` with filename

**Error Responses**:
- **400 Bad Request**: JSON with `{"detail": "error message"}`
- **413 Payload Too Large**: JSON with file size limit information
- **500 Internal Server Error**: JSON with error details

### User Experience Considerations

1. **Progressive Feedback**: Show status at each stage (uploading → processing → ready)
2. **File Validation**: Validate file type and size before upload
3. **Clear Instructions**: Provide brief instructions on what files are expected
4. **Error Recovery**: Allow users to retry after errors
5. **Accessibility**: Ensure UI is accessible (keyboard navigation, screen readers)
6. **Mobile Responsive**: Design should work on mobile devices (though file uploads may be limited)

### Example UI Flow

```
┌─────────────────────────────────────┐
│  Compressor PDF to Excel Converter  │
├─────────────────────────────────────┤
│                                     │
│  [Select ZIP File] [Browse...]     │
│  Selected: compressors.zip (45 MB)  │
│                                     │
│  [Upload and Process]               │
│                                     │
│  Status: Ready to upload           │
│                                     │
└─────────────────────────────────────┘

After upload:
┌─────────────────────────────────────┐
│  Compressor PDF to Excel Converter  │
├─────────────────────────────────────┤
│                                     │
│  Selected: compressors.zip (45 MB)  │
│                                     │
│  [Processing...] ⏳                  │
│                                     │
│  Status: Processing PDFs...         │
│                                     │
└─────────────────────────────────────┘

After success:
┌─────────────────────────────────────┐
│  Compressor PDF to Excel Converter  │
├─────────────────────────────────────┤
│                                     │
│  ✓ Processing complete!             │
│                                     │
│  [Download Excel File]              │
│  compressor-data.xlsx               │
│                                     │
│  [Upload Another File]              │
│                                     │
└─────────────────────────────────────┘
```

---

## 3. Docker Setup & Deployment

### Prerequisites

Before deploying the API, ensure you have:

- **Docker** installed (version 20.10 or later)
- **Docker Compose** installed (version 2.0 or later, recommended)
- At least **2GB** of available disk space
- At least **512MB** of available RAM (2GB recommended for production)

### Quick Start with Docker Compose (Recommended)

Docker Compose is the easiest way to get the API running:

1. **Navigate to the project directory:**
   ```bash
   cd compressor-to-excel
   ```

2. **Build and start the container:**
   ```bash
   docker-compose up -d
   ```
   
   This will:
   - Build the Docker image
   - Start the API container
   - Map port 8001 on your host to port 8000 in the container

3. **Verify the API is running:**
   ```bash
   curl http://localhost:8001/api/health
   ```
   
   Expected response:
   ```json
   {
     "status": "healthy",
     "version": "1.0.0"
   }
   ```

4. **View logs (optional):**
   ```bash
   docker-compose logs -f api
   ```

5. **Stop the container:**
   ```bash
   docker-compose down
   ```

### Port Configuration

**Important**: The API uses different ports depending on deployment method:

- **Docker Compose**: Port **8001** on host (mapped to 8000 in container)
- **Docker Direct**: Port **8000** on host (mapped to 8000 in container)
- **Local Development**: Port **8000**

The container always uses port 8000 internally. Only the host port mapping differs.

**Changing the port** (if 8001 is in use):
```bash
PORT=8002 docker-compose up -d
```

### Using Docker Directly

If you prefer not to use Docker Compose:

1. **Build the Docker image:**
   ```bash
   docker build -t compressor-api .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     --name compressor-api \
     -p 8000:8000 \
     -e WORKERS=4 \
     -v compressor-temp:/tmp/compressor-api \
     compressor-api
   ```

3. **Verify it's running:**
   ```bash
   curl http://localhost:8000/api/health
   ```

4. **View logs:**
   ```bash
   docker logs -f compressor-api
   ```

5. **Stop the container:**
   ```bash
   docker stop compressor-api
   docker rm compressor-api
   ```

### Environment Variables Configuration

The API can be configured using environment variables. Key options:

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | API host address |
| `PORT` | `8000` | API port (container internal) |
| `WORKERS` | `4` | Number of uvicorn workers |
| `MAX_ZIP_SIZE` | `524288000` | Max ZIP size in bytes (500 MB) |
| `MAX_PDF_SIZE` | `104857600` | Max PDF size in bytes (100 MB) |
| `MAX_PDFS` | `100` | Maximum PDFs per ZIP |
| `PROCESSING_TIMEOUT` | `3600` | Processing timeout in seconds |
| `TEMP_DIR` | `/tmp/compressor-api` | Temporary directory path |

**Setting environment variables with Docker Compose:**

Create a `.env` file in the project root:
```bash
WORKERS=8
MAX_ZIP_SIZE=1073741824
MAX_PDF_SIZE=209715200
```

Then run:
```bash
docker-compose up -d
```

**Setting environment variables with Docker directly:**
```bash
docker run -d \
  --name compressor-api \
  -p 8000:8000 \
  -e WORKERS=8 \
  -e MAX_ZIP_SIZE=1073741824 \
  compressor-api
```

### Health Check Verification

The container includes automatic health checks. Verify health status:

```bash
# Check container status
docker ps

# Look for "healthy" status in the output

# Test health endpoint directly
curl http://localhost:8001/api/health  # Docker Compose
curl http://localhost:8000/api/health  # Docker Direct
```

### Troubleshooting Common Issues

#### Container Won't Start

1. **Check logs:**
   ```bash
   docker logs compressor-api
   ```

2. **Check port availability:**
   ```bash
   # Check if port 8001 is in use (Docker Compose)
   lsof -i :8001
   
   # Or check port 8000 (Docker Direct)
   lsof -i :8000
   ```
   
   **Solution**: Change port using `PORT` environment variable

3. **Check disk space:**
   ```bash
   docker system df
   ```

#### API Not Responding

1. **Check if container is running:**
   ```bash
   docker ps
   ```

2. **Check health status:**
   ```bash
   docker inspect compressor-api | grep Health
   ```

3. **Test health endpoint:**
   ```bash
   curl http://localhost:8001/api/health
   ```

#### File Upload Issues

1. **Check temporary directory permissions:**
   ```bash
   docker exec compressor-api ls -la /tmp/compressor-api
   ```

2. **Check disk space in volume:**
   ```bash
   docker volume inspect compressor-temp
   ```

3. **Increase file size limits:**
   Set `MAX_ZIP_SIZE` and `MAX_PDF_SIZE` environment variables

#### Performance Issues

1. **Increase worker count:**
   Set `WORKERS` environment variable (recommended: `(2 × CPU cores) + 1`)

2. **Monitor resource usage:**
   ```bash
   docker stats compressor-api
   ```

3. **Increase resource limits:**
   Update `docker-compose.yml` resource limits section

### Production Deployment Considerations

1. **Resource Limits**: The `docker-compose.yml` includes resource limits:
   - CPU: Maximum 2 cores, reserved 0.5 cores
   - Memory: Maximum 2GB, reserved 512MB
   - Adjust based on your server capacity

2. **Worker Count**: Recommended formula:
   ```
   WORKERS = (2 × CPU cores) + 1
   ```
   Example for 4-core server: `WORKERS=9`

3. **Restart Policy**: The container is configured with `restart: unless-stopped` to ensure automatic restarts after system reboots

4. **Security**: 
   - Container runs as non-root user (`appuser`)
   - Temporary files are isolated in Docker volume
   - File type and size validation
   - Filename sanitization

5. **Monitoring**: Use health check endpoint (`/api/health`) for monitoring

### Updating the Container

To update to the latest code:

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose build --no-cache
docker-compose up -d
```

### Cleaning Up

**Remove container and volumes:**
```bash
# Using Docker Compose
docker-compose down -v

# Using Docker directly
docker stop compressor-api
docker rm compressor-api
docker volume rm compressor-temp
```

**Clean up unused resources:**
```bash
docker system prune -a
```

---

## 4. Implementation Status

### What's Done ✅

The following components are **fully implemented and tested**:

#### 4.1 REST API

- ✅ **Upload Endpoint** (`POST /api/upload`)
  - Accepts ZIP file uploads via multipart/form-data
  - Validates file type and size
  - Extracts ZIP files to temporary directory
  - Processes all PDFs in the ZIP
  - Generates Excel file with separate sheets per compressor
  - Returns Excel file as download response
  - Comprehensive error handling

- ✅ **Health Check Endpoint** (`GET /api/health`)
  - Returns API status and version
  - Used for monitoring and health checks

- ✅ **API Documentation**
  - Automatic OpenAPI/Swagger documentation at `/api/docs`
  - ReDoc documentation at `/api/redoc`
  - OpenAPI JSON schema at `/api/openapi.json`

#### 4.2 PDF Processing Logic

- ✅ **PDF Text Extraction**
  - Uses PyMuPDF (fitz) for fast, memory-efficient extraction
  - Handles large PDFs (6000+ pages) using batch processing
  - Extracts date/time and consumption values using regex patterns

- ✅ **Compressor Number Extraction**
  - Automatically identifies compressor number from filename
  - Supports patterns: `COMPRESOR<number>`, `COMPRESOR-<number>`, etc.
  - Fallback naming for files that don't match pattern

- ✅ **Data Parsing**
  - Parses date/time format: `DD/MM/YYYY HH:MM:SS`
  - Extracts consumption values (handles integers and floats)
  - Skips headers, page markers, and empty lines

#### 4.3 Excel Generation

- ✅ **Multi-Sheet Excel Files**
  - Creates separate sheets for each compressor number
  - Handles Excel's row limit (1,048,576 rows per sheet)
  - Combines multiple PDFs with same compressor into one sheet

- ✅ **Column Structure**
  - Date column: Date and time stamps
  - Consumo column: Consumption values
  - Compressor column: Compressor identifier

- ✅ **Memory Efficiency**
  - Uses openpyxl WriteOnlyWorksheet mode
  - Batch writes to reduce memory usage
  - Processes files incrementally

#### 4.4 ZIP File Handling

- ✅ **ZIP Extraction**
  - Validates ZIP file format
  - Extracts to temporary directory
  - Validates ZIP contains PDF files
  - Checks PDF count limits

- ✅ **Security**
  - Filename sanitization to prevent path traversal
  - File type validation (ZIP files only)
  - File size limits (configurable)
  - Temporary file cleanup

#### 4.5 Docker Configuration

- ✅ **Dockerfile**
  - Multi-stage build for optimized image size
  - Python 3.12 base image
  - System dependencies for PDF libraries
  - Non-root user for security
  - Health check configuration

- ✅ **Docker Compose**
  - Pre-configured service definition
  - Environment variable support
  - Volume management for temporary files
  - Resource limits configuration
  - Restart policy

#### 4.6 Error Handling

- ✅ **Validation Errors**
  - Invalid file type (400 Bad Request)
  - File too large (413 Payload Too Large)
  - No PDFs in ZIP (400 Bad Request)
  - Empty ZIP file (400 Bad Request)

- ✅ **Processing Errors**
  - PDF extraction failures (500 Internal Server Error)
  - Excel generation errors (500 Internal Server Error)
  - Detailed error messages in JSON format

- ✅ **Resource Management**
  - Automatic cleanup of temporary files
  - Delayed cleanup to allow file downloads
  - Error recovery and cleanup on failures

#### 4.7 Documentation

- ✅ **API Documentation** (`docs/api.md`)
  - Complete endpoint reference
  - Request/response examples
  - Error code reference
  - Configuration guide

- ✅ **Docker Documentation** (`docs/docker.md`)
  - Setup instructions
  - Configuration guide
  - Troubleshooting guide
  - Production deployment tips

- ✅ **User Guides**
  - How to use API via browser
  - How to use API via command line
  - How to use API via Python

### What Needs to be Done 🔨

The following components need to be implemented in the Tool Hub:

#### 4.8 Tool Hub UI Component

- ❌ **File Upload UI**
  - File input element for ZIP file selection
  - File type restriction (ZIP only)
  - File size display and validation feedback
  - Drag-and-drop support (optional)
  - Visual file selection indicator

- ❌ **Upload Button**
  - Button to trigger API upload
  - Disabled state when no file selected
  - Loading state during processing
  - Click handler to call API endpoint

- ❌ **Download Button**
  - Button to download Excel file
  - Hidden initially, shown after successful processing
  - Filename display
  - Download trigger functionality

- ❌ **Status/Loading Indicator**
  - Loading spinner during processing
  - Status messages (uploading, processing, ready)
  - Progress feedback (if possible)

- ❌ **Error Display**
  - Error message display area
  - User-friendly error messages
  - Error recovery options (retry button)

#### 4.9 Frontend Integration

- ❌ **API Client Code**
  - JavaScript/TypeScript function to call `/api/upload`
  - FormData construction for file upload
  - Response handling (success and error cases)
  - Blob handling for Excel file download

- ❌ **State Management**
  - File selection state
  - Upload/processing state
  - Error state
  - Download ready state

- ❌ **UI Styling**
  - Consistent styling with Tool Hub design system
  - Responsive design for mobile devices
  - Accessibility considerations (keyboard navigation, ARIA labels)

#### 4.10 Connection Configuration

- ❌ **API Endpoint Configuration**
  - Configurable API base URL
  - Environment-specific configuration (dev, staging, production)
  - CORS configuration (if needed)

- ❌ **Error Handling Integration**
  - Map API error codes to user-friendly messages
  - Handle network errors
  - Handle timeout errors
  - Retry logic (optional)

#### 4.11 Testing

- ❌ **UI Testing**
  - File upload functionality
  - Error handling
  - Download functionality
  - Loading states

- ❌ **Integration Testing**
  - End-to-end workflow testing
  - API connectivity testing
  - Error scenario testing

### Implementation Checklist

Use this checklist to track Tool Hub integration progress:

- [ ] Create file upload UI component
- [ ] Implement file selection handler
- [ ] Add file validation (type and size)
- [ ] Create upload button with loading state
- [ ] Implement API client function (`POST /api/upload`)
- [ ] Handle API response (success and error)
- [ ] Create download button component
- [ ] Implement Excel file download functionality
- [ ] Add status/loading indicator
- [ ] Implement error display component
- [ ] Add user-friendly error messages
- [ ] Style components to match Tool Hub design
- [ ] Test file upload workflow
- [ ] Test error scenarios
- [ ] Test download functionality
- [ ] Verify mobile responsiveness
- [ ] Test accessibility features
- [ ] Configure API endpoint URL
- [ ] Deploy and test in Tool Hub environment

---

## Summary

The Compressor to Excel API is **fully implemented and ready for integration**. The API provides a complete backend service for processing ZIP files containing compressor PDFs and generating Excel output files.

**Repository**: https://gitlab.leyton.fr/caes/compressor-to-excel-api

**What you need to build**: A simple UI in the Tool Hub with file upload, processing status, and download functionality. The API handles all the complex processing logic, so the frontend can focus on providing a clean user experience.

**Getting Started**: Use Docker Compose to quickly get the API running, then integrate the UI components using the API endpoint details provided in this document.

For questions or issues, refer to the detailed API documentation (`docs/api.md`) and Docker deployment guide (`docs/docker.md`).


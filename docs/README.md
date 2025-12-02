# Documentation

This directory contains all documentation for the Compressor PDF to Excel Converter tool.

## Documentation Structure

### [User Guide](user-guide.md)
**For end users** - Step-by-step instructions on how to use the tool.

This guide covers:
- How to process a single PDF file
- How to process multiple PDF files
- How to process all PDFs in a directory
- Troubleshooting common issues
- Understanding the output format

**Start here if you want to use the tool.**

### [API Documentation](api.md)
**For developers** - REST API reference and technical details.

This documentation covers:
- API endpoints and request/response formats
- Authentication and security
- Error codes and troubleshooting
- Configuration options
- Example code in multiple languages

**Start here if you want to integrate the API into your applications.**

### [Docker Deployment Guide](docker.md)
**For DevOps and deployment** - Docker containerization and deployment instructions.

This documentation covers:
- Building Docker images
- Running with Docker Compose
- Configuration and environment variables
- Production deployment considerations
- Troubleshooting Docker issues

**Start here if you want to deploy the API using Docker.**

### [How To Use API via Web Browser](how-to-use-api-browser.md)
**For end users** - Step-by-step guide for using the API through your web browser.

This guide covers:
- Accessing the API documentation page
- Uploading ZIP files through the web interface
- Downloading Excel output files
- Troubleshooting common browser issues

**Start here if you prefer using a web browser.**

### [How To Use API via Command Line](how-to-use-api-command-line.md)
**For users comfortable with command line** - Guide for using the API with curl.

This guide covers:
- Installing and using curl
- Uploading ZIP files from the command line
- Checking API health status
- Automating with scripts

**Start here if you prefer command-line tools or need to automate.**

### [How To Use API via Python](how-to-use-api-python.md)
**For Python developers** - Guide for integrating the API into Python scripts.

This guide covers:
- Installing the requests library
- Writing Python scripts to upload files
- Processing multiple files automatically
- Error handling and best practices

**Start here if you're writing Python scripts or applications.**

### [Technical Documentation](technical.md)
**For developers** - Technical details about the implementation.

This documentation covers:
- Architecture and design decisions
- Memory optimization strategies
- Code structure and organization
- Performance characteristics
- Multi-PDF processing implementation
- Error handling mechanisms

**Start here if you want to understand or modify the code.**

## Quick Start

### For Users (Command-Line Tool)
1. Read the [User Guide](user-guide.md) to learn how to use the command-line tool
2. Install dependencies: `pip install -r requirements.txt`
3. Run the tool: `python extract_pdf_text.py your-file.pdf`

### For Users (API via Web Browser)
1. Ensure the API server is running:
   - Docker Compose: `docker-compose up -d` (access at http://localhost:8001/api/docs)
   - Local development: `python run_api.py` (access at http://localhost:8000/api/docs)
2. Open your browser to the appropriate URL
3. Follow the [How To Use API via Web Browser](how-to-use-api-browser.md) guide

### For Developers (API Integration)
1. Read the [API Documentation](api.md) for technical reference
2. Choose your integration method:
   - [Web Browser](how-to-use-api-browser.md) - For manual uploads
   - [Command Line](how-to-use-api-command-line.md) - For automation with curl
   - [Python](how-to-use-api-python.md) - For Python applications
3. Start the API server: `python run_api.py`

### For Developers (Code Modification)
1. Read the [Technical Documentation](technical.md) to understand the implementation
2. Review the code structure section
3. Check the memory optimization strategies for large file handling

## Tool Overview

The Compressor PDF to Excel Converter extracts compressor data from PDF files and converts it to Excel format. It supports:

- **Command-line tool**: Process PDFs directly from the terminal
- **REST API**: Upload ZIP files via web browser, command line, or Python scripts
- **Single file processing**: Convert one PDF to Excel
- **Multiple file processing**: Combine multiple PDFs into one Excel file
- **Directory processing**: Process all PDFs in a folder automatically
- **Memory-efficient**: Handles large PDFs (6000+ pages) efficiently
- **Error recovery**: Continues processing even if some files fail

## Output Format

Excel files are organized with **separate sheets for each compressor number** to handle Excel's row limit of 1,048,576 rows per sheet.

**Sheet Organization:**
- Each compressor number gets its own sheet (e.g., "Compressor 1", "Compressor 4")
- Multiple PDFs with the same compressor number are combined into the same sheet
- Each sheet contains three columns:
  - **Date**: Date and time of measurement (DD/MM/YYYY HH:MM:SS)
  - **Consumo**: Consumption value (numeric)
  - **Compressor**: Compressor identifier (extracted from filename)

## Getting Help

- **Command-line tool usage**: See [User Guide](user-guide.md) troubleshooting section
- **API usage questions**: See the relevant "How To" guide for your method:
  - [Web Browser](how-to-use-api-browser.md)
  - [Command Line](how-to-use-api-command-line.md)
  - [Python](how-to-use-api-python.md)
- **API technical reference**: See [API Documentation](api.md)
- **Code and implementation questions**: See [Technical Documentation](technical.md)
- **Code issues**: Check the code comments and function docstrings


# Compressor PDF to Excel Converter

A Python tool to extract compressor data from PDF files and convert it directly to Excel format. Optimized for processing large PDF files (6000+ pages) with memory-efficient batch processing.

## Features

- ✅ Extract Date and Consumo values from PDF pages
- ✅ Automatically identify compressor number from filename
- ✅ Process single PDF files or multiple PDFs at once
- ✅ Batch process all PDFs in a directory
- ✅ **REST API** - Upload ZIP files via web browser, command line, or Python
- ✅ Memory-efficient processing for large files
- ✅ Error recovery - continues processing even if some files fail
- ✅ Combine multiple PDFs into a single Excel file

## Quick Start

### Installation

**Local Installation:**
```bash
pip install -r requirements.txt
```

**Docker Installation (Recommended):**
```bash
# Using Docker Compose (default port: 8001)
docker-compose up -d

# Or using Docker directly (you can choose any port)
docker build -t compressor-api .
docker run -d -p 8000:8000 compressor-api
```

### Usage

**Command-Line Tool:**
```bash
# Process a single PDF file
python extract_pdf_text.py input.pdf

# Process multiple PDF files
python extract_pdf_text.py file1.pdf file2.pdf file3.pdf -o combined.xlsx

# Process all PDFs in a directory
python extract_pdf_text.py -d folder-name/ -o combined.xlsx
```

**REST API:**
```bash
# Local development
python run_api.py

# Docker deployment
docker-compose up -d

# Then access the API at http://localhost:8001/api/docs (Docker Compose)
# Or http://localhost:8000/api/docs (if using Docker directly)
# Or use curl, Python requests, or any HTTP client
```

## Output Format

Excel files are organized with **separate sheets for each compressor number** to handle Excel's row limit of 1,048,576 rows per sheet.

**Sheet Organization:**
- Each compressor number gets its own sheet (e.g., "Compressor 1", "Compressor 4", "Compressor 5")
- Multiple PDFs with the same compressor number are combined into the same sheet
- Each sheet contains three columns:
  - **Date**: Date and time (DD/MM/YYYY HH:MM:SS)
  - **Consumo**: Consumption value (numeric)
  - **Compressor**: Compressor identifier (e.g., "Compressor 4")

## Documentation

📚 **Full documentation is available in the [`docs/`](docs/) folder:**

- **[Documentation Index](docs/README.md)** - Overview of all documentation
- **[User Guide](docs/user-guide.md)** - Step-by-step instructions for the command-line tool
- **[API Documentation](docs/api.md)** - REST API reference for developers
- **[Docker Deployment Guide](docs/docker.md)** - Docker setup and deployment instructions
- **[How To Use API via Web Browser](docs/how-to-use-api-browser.md)** - Upload files through your browser
- **[How To Use API via Command Line](docs/how-to-use-api-command-line.md)** - Use curl to upload files
- **[How To Use API via Python](docs/how-to-use-api-python.md)** - Integrate the API into Python scripts
- **[Technical Documentation](docs/technical.md)** - Implementation details and architecture

## Requirements

- Python 3.7+
- PyMuPDF (fitz)
- openpyxl
- pandas
- FastAPI (for API server)
- uvicorn (for API server)

See `requirements.txt` for complete list.

## Project Structure

```
compressor-to-excel/
├── api/                     # REST API implementation
│   ├── __init__.py
│   ├── main.py             # FastAPI application
│   ├── config.py           # Configuration settings
│   ├── models.py           # Pydantic models
│   └── utils.py            # Utility functions
├── docs/                    # Documentation
│   ├── README.md           # Documentation index
│   ├── user-guide.md       # User instructions (CLI)
│   ├── api.md              # API technical reference
│   ├── how-to-use-api-*.md # API usage guides
│   └── technical.md        # Technical documentation
├── scripts/                 # Utility and testing scripts
│   └── compare_extractions.py  # PDF extraction comparison utility
├── tests/                   # Test files and data
│   └── data/               # Test PDF files
├── extract_pdf_text.py     # Main extraction script (CLI)
├── run_api.py              # API server startup script
├── requirements.txt        # Python dependencies
├── Dockerfile
└── docker-compose.yml
```

## License

See individual files for license information.


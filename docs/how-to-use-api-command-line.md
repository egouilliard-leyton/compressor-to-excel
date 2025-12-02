# How To Upload Compressor PDFs Using Command Line

This guide explains how to use the Compressor to Excel API from the command line to upload ZIP files and download Excel output files.

## Introduction

If you prefer using command-line tools or need to automate the process, you can use `curl` to interact with the API. This method is useful for scripting and automation tasks.

## Prerequisites

- A command-line terminal (Command Prompt on Windows, Terminal on Mac/Linux)
- `curl` installed on your computer (usually pre-installed on Mac/Linux, available for Windows)
- A ZIP file containing compressor PDF files
- The API server address (typically `http://localhost:8001` for Docker Compose, or `http://localhost:8000` for Docker direct/local development)

## Steps

### Basic Upload

1. Open your command-line terminal.
   - On Windows: Open Command Prompt or PowerShell
   - On Mac/Linux: Open Terminal

2. Navigate to the folder containing your ZIP file using the `cd` command.
   - Example: `cd C:\Users\YourName\Documents` (Windows)
   - Example: `cd ~/Documents` (Mac/Linux)

3. Type the following command, replacing the placeholders with your actual values:
   ```
   curl -X POST "http://localhost:8001/api/upload" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your-file.zip" \
     --output result.xlsx
   ```
   - Replace `your-file.zip` with your actual ZIP filename
   - Replace `result.xlsx` with your desired output filename
   - Replace `localhost:8001` with your server address if different (use `8000` if using Docker directly or local development)

4. Press Enter to run the command.

5. Wait for the command to complete.
   - You'll see progress information as the file uploads
   - Processing time depends on the size and number of PDFs

6. When finished, check that the Excel file was created.
   - Look for `result.xlsx` (or your chosen filename) in the current directory
   - The file should be larger than 0 bytes

### Checking API Health

Before uploading, you can verify the API is running:

1. Type the following command:
   ```
   curl http://localhost:8001/api/health
   ```
   (Use port 8000 if using Docker directly or local development)

2. Press Enter.

3. You should see a response like:
   ```
   {"status":"healthy","version":"1.0.0"}
   ```

4. If you see this response, the API is running and ready to accept uploads.

### Uploading to a Remote Server

If the API is running on a different computer:

1. Replace `localhost:8001` (or `localhost:8000`) with the server's address.
   - Example: `http://192.168.1.100:8001`
   - Example: `http://api.example.com:8001`

2. Use the same command format as above with the updated server address.

## Expected Results

After running the upload command successfully:
- The command will complete without errors
- An Excel file will be created in your current directory
- The file will contain separate sheets for each compressor number
- PDFs with the same compressor number will be combined into the same sheet
- Each sheet contains all compressor data from the corresponding PDFs

## Troubleshooting

- **"Connection refused" error**: The API server is not running or the address is incorrect. Verify the server is running and check the address/port

- **"File not found" error**: Make sure you're in the correct directory and the ZIP filename is spelled correctly. Use `ls` (Mac/Linux) or `dir` (Windows) to list files

- **"curl: command not found"**: `curl` is not installed. On Windows, download it from curl.se. On Mac/Linux, install it using your package manager

- **"400 Bad Request" error**: Your ZIP file may be invalid or doesn't contain PDFs. Check that your ZIP file is valid and contains PDF files

- **"413 Payload Too Large" error**: Your ZIP file is too large. The default limit is 500 MB. Split your files into smaller ZIPs or contact your administrator

- **"500 Internal Server Error"**: There was a problem processing your files. Check the server logs or contact your administrator

- **Empty Excel file**: The ZIP may not have contained valid PDF files, or the PDFs didn't have the expected format. Verify your PDF files are correct

## Additional Information

- You can use this command in scripts to automate processing
- The `--output` flag saves the Excel file with a specific name
- Without `--output`, the Excel content will be displayed in the terminal (not recommended)
- You can add `-v` flag for verbose output to see more details about the request
- For Windows Command Prompt, use `^` instead of `\` for line continuation, or put the entire command on one line

## Example Script

You can create a simple script to process multiple ZIP files:

**Windows (batch file):**
```batch
@echo off
for %%f in (*.zip) do (
    curl -X POST "http://localhost:8001/api/upload" -F "file=@%%f" --output %%~nf.xlsx
)
```

**Mac/Linux (bash script):**
```bash
#!/bin/bash
for file in *.zip; do
    curl -X POST "http://localhost:8001/api/upload" \
      -F "file=@$file" \
      --output "${file%.zip}.xlsx"
done
```


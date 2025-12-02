# How To Upload Compressor PDFs Using the Web Browser

This guide explains how to use the Compressor to Excel API through your web browser to upload ZIP files containing PDFs and download Excel files with combined compressor data.

## Introduction

The API provides a web interface that lets you upload ZIP files containing compressor PDFs and receive Excel files with all your data combined. You can use this without installing any software or using command-line tools.

## Prerequisites

- An internet connection
- A web browser (Chrome, Firefox, Safari, or Edge)
- A ZIP file containing one or more compressor PDF files
- The API server must be running (contact your administrator if you're not sure)

## Steps

1. Open your web browser and navigate to the API documentation page.
   - The URL is typically: `http://localhost:8001/api/docs` (for Docker Compose)
   - Or `http://localhost:8000/api/docs` (for Docker direct or local development)
   - If you're accessing a remote server, replace `localhost:8001` (or `localhost:8000`) with the server address provided by your administrator

2. You should see the API documentation page with a list of available endpoints.
   - Look for a section labeled "Upload" or "POST /api/upload"
   - Click on the "POST /api/upload" endpoint to expand it

3. Click the "Try it out" button in the endpoint section.
   - This enables the interactive testing interface

4. Click the "Choose File" or "Browse" button next to the "file" field.
   - A file selection dialog will open

5. Navigate to your ZIP file and select it.
   - Make sure your ZIP file contains PDF files with compressor data
   - PDF filenames should follow the pattern: `COMPRESOR4-ABR-JUN-25.PDF` (where the number can vary)

6. Click the "Execute" button at the bottom of the form.
   - The API will start processing your ZIP file
   - You may see a loading indicator while processing

7. Wait for the processing to complete.
   - Processing time depends on the number and size of PDFs in your ZIP file
   - For large files, this may take several minutes

8. When processing is complete, you will see a response section below the form.
   - If successful, you'll see a "Download file" link or button
   - The response code will be "200" for success

9. Click the "Download file" link or button to save the Excel file.
   - Your browser will prompt you to save the file
   - Choose a location on your computer and click "Save"

10. Open the downloaded Excel file to view your compressor data.
    - The file will contain separate sheets for each compressor number
    - Each sheet contains three columns: Date, Consumo, and Compressor
    - PDFs with the same compressor number are combined into the same sheet
    - This organization ensures each sheet stays within Excel's limit of 1,048,576 rows

## Expected Results

After completing these steps, you should have:
- An Excel file saved on your computer
- Separate sheets for each compressor number (e.g., "Compressor 1", "Compressor 4", "Compressor 5")
- All PDFs with the same compressor number combined into the same sheet
- Each sheet contains data organized in columns: Date, Consumo, and Compressor

## Troubleshooting

- **"File must be a ZIP file" error**: Make sure you're uploading a file with a `.zip` extension. If your file has a different extension, rename it to end with `.zip`

- **"No PDF files found in ZIP archive" error**: Check that your ZIP file actually contains PDF files. Open the ZIP file to verify it has `.pdf` files inside

- **"File too large" error**: Your ZIP file exceeds the size limit (default is 500 MB). Try splitting your files into smaller ZIP archives

- **"ZIP file is empty" error**: Your ZIP file doesn't contain any files. Make sure you've added PDF files to the ZIP before uploading

- **Connection error**: The API server may not be running. Contact your administrator to verify the server is available

- **Processing takes too long**: Large PDF files can take time to process. Wait patiently, or check with your administrator about processing time limits

- **Download doesn't start**: Check your browser's download settings. Some browsers block automatic downloads - look for a download notification in your browser

## Additional Information

- The API can process up to 100 PDF files in a single ZIP (this limit can be adjusted by administrators)
- Each PDF file can be up to 100 MB in size
- The Excel output file will be named based on your ZIP filename, or you can rename it after downloading
- You can upload multiple ZIP files one at a time to process different sets of compressor data
- The API preserves all data from your PDFs, so you won't lose any information during conversion


# How To Extract Compressor Data from PDFs to Excel

This guide explains how to use the PDF extraction tool to convert compressor data from PDF files into Excel spreadsheets that you can easily analyze and work with.

## What This Tool Does

The tool reads compressor data from PDF files and creates Excel files with three columns:
- **Date**: The date and time of each measurement
- **Consumo**: The consumption value recorded
- **Compressor**: Which compressor the data came from (extracted from the PDF filename)

## Prerequisites

- Python 3 installed on your computer
- The required Python packages installed (run `pip install -r requirements.txt`)
- PDF files containing compressor data
- Access to a command-line terminal (Command Prompt on Windows, Terminal on Mac/Linux)

## Steps

### Processing a Single PDF File

1. Open your command-line terminal.
2. Navigate to the folder containing the extraction tool using the `cd` command.
   - Example: `cd C:\Users\YourName\compressor-to-excel`
3. Type the following command, replacing `filename.pdf` with your actual PDF filename:
   ```
   python extract_pdf_text.py filename.pdf
   ```
4. Press Enter to run the command.
5. Wait for the processing to complete. You will see progress messages showing:
   - Which compressor was detected
   - How many pages are being processed
   - How many data rows have been extracted
   - Estimated time remaining
6. When finished, you will see a message confirming the Excel file was created.
7. The Excel file will be created in the same folder as your PDF, with the same name but a `.xlsx` extension.
   - Example: `COMPRESOR4-ABR-JUN-25.PDF` becomes `COMPRESOR4-ABR-JUN-25.xlsx`

### Processing Multiple PDF Files

1. Open your command-line terminal.
2. Navigate to the folder containing the extraction tool.
3. Type the following command, listing all PDF files you want to process and specifying an output filename:
   ```
   python extract_pdf_text.py file1.pdf file2.pdf file3.pdf -o combined.xlsx
   ```
   - Replace `file1.pdf`, `file2.pdf`, etc. with your actual PDF filenames
   - Replace `combined.xlsx` with your desired output filename
4. Press Enter to run the command.
5. The tool will process each PDF file one by one, showing progress for each file.
6. All data from all PDFs will be combined into a single Excel file, organized into separate sheets by compressor number.
7. When finished, you will see a summary showing:
   - How many PDFs were processed successfully
   - How many failed (if any)
   - Total number of data rows written
   - The location of the output file

### Processing All PDFs in a Folder

1. Open your command-line terminal.
2. Navigate to the folder containing the extraction tool.
3. Type the following command, replacing `folder-name` with the folder containing your PDFs:
   ```
   python extract_pdf_text.py -d folder-name -o combined.xlsx
   ```
   - Replace `folder-name` with your actual folder path (e.g., `tests/data`)
   - Replace `combined.xlsx` with your desired output filename
4. Press Enter to run the command.
5. The tool will automatically find all PDF files in the specified folder and process them.
6. All data will be combined into a single Excel file, organized into separate sheets by compressor number.
7. When finished, you will see a summary of the processing results.

## Expected Results

### Successful Processing

When processing completes successfully, you will see:
- A confirmation message showing the number of pages processed
- The number of data rows extracted
- The processing time
- The location of the created Excel file

The Excel file will contain:
- **Row 1**: Column headers (Date, Consumo, Compressor)
- **Row 2 onwards**: Your data rows with date/time, consumption values, and compressor identification

### Excel File Format

The Excel file is organized with **separate sheets for each compressor**. This ensures that each compressor's data stays within Excel's limit of 1,048,576 rows per sheet.

**Sheet Organization:**
- Each compressor number gets its own sheet (e.g., "Compressor 1", "Compressor 4", "Compressor 5")
- If you process multiple PDFs with the same compressor number, they are all combined into the same sheet
- Each sheet contains three columns:
  1. **Date**: Shows dates and times in the format `DD/MM/YYYY HH:MM:SS` (e.g., `01/04/2025 0:00:26`)
  2. **Consumo**: Shows numeric consumption values (e.g., `148`, `149`, `151`)
  3. **Compressor**: Shows which compressor the data came from (e.g., `Compressor 4`, `Compressor 1`)

**Example:**
If you process PDFs for Compressor 1, Compressor 4, and Compressor 5, your Excel file will have three sheets:
- Sheet "Compressor 1" - Contains all data from Compressor 1 PDFs
- Sheet "Compressor 4" - Contains all data from Compressor 4 PDFs
- Sheet "Compressor 5" - Contains all data from Compressor 5 PDFs

## Troubleshooting

### Error: "PDF file not found"

**Problem**: The tool cannot find the PDF file you specified.

**Solution**: 
- Check that you typed the filename correctly
- Make sure you're in the correct folder (use `cd` to navigate)
- Include the full path if the PDF is in a different folder
- Example: `python extract_pdf_text.py C:\Users\YourName\Documents\file.pdf`

### Error: "Could not extract compressor number from filename"

**Problem**: The PDF filename doesn't contain a recognizable compressor number pattern.

**Solution**:
- The filename should contain "COMPRESOR" followed by a number (e.g., `COMPRESOR4-ABR-JUN-25.PDF`)
- Rename your PDF file to include this pattern if needed
- The tool looks for patterns like `COMPRESOR1`, `COMPRESOR2`, `compresor4`, etc. (case-insensitive)

### Error: "Output file (-o/--output) is required when processing multiple PDFs"

**Problem**: You tried to process multiple PDFs without specifying an output filename.

**Solution**:
- Add `-o output.xlsx` to your command
- Example: `python extract_pdf_text.py file1.pdf file2.pdf -o combined.xlsx`

### Error: "No PDF files found in directory"

**Problem**: The directory you specified doesn't contain any PDF files.

**Solution**:
- Check that you typed the directory name correctly
- Verify that PDF files exist in that directory
- Make sure the files have `.pdf` or `.PDF` extension

### Processing Takes a Long Time

**Problem**: Large PDF files (thousands of pages) take time to process.

**Solution**:
- This is normal for large files
- The tool shows progress messages so you can see it's working
- Processing time depends on file size (typically 0.03-0.06 seconds per page)
- For a 6000-page PDF, expect 3-6 minutes of processing time

### Some PDFs Failed to Process

**Problem**: When processing multiple PDFs, some files failed but others succeeded.

**Solution**:
- The tool will continue processing remaining files even if one fails
- Check the error messages shown for each failed file
- Common causes:
  - Corrupted PDF file
  - PDF doesn't contain the expected data format
  - File permissions issue
- The Excel file will still be created with data from successfully processed PDFs

## Additional Information

### File Naming

- For single PDF processing, the output Excel file uses the same name as the PDF but with `.xlsx` extension
- For multiple PDFs, you must specify the output filename using `-o`
- The compressor number is automatically extracted from the PDF filename

### Data Format

- Dates are preserved exactly as they appear in the PDF
- Consumption values are stored as numbers (you can perform calculations in Excel)
- The Compressor column helps identify which PDF each row came from when combining multiple files

### Performance Tips

- Processing is optimized for large files (6000+ pages)
- The tool processes files in batches to manage memory efficiently
- You can process multiple PDFs in one run to combine all data into a single Excel file with separate sheets per compressor

### Next Steps

After creating your Excel file, you can:
- Open it in Microsoft Excel, Google Sheets, or any spreadsheet application
- Sort and filter the data
- Create charts and graphs
- Perform calculations and analysis
- Export to other formats if needed


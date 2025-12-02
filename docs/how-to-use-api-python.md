# How To Upload Compressor PDFs Using Python

This guide explains how to use the Compressor to Excel API from Python scripts to upload ZIP files and download Excel output files programmatically.

## Introduction

If you're writing Python scripts or applications, you can use the `requests` library to interact with the API. This allows you to automate the process and integrate it into your workflows.

## Prerequisites

- Python 3 installed on your computer
- The `requests` library installed (install with: `pip install requests`)
- A ZIP file containing compressor PDF files
- The API server address (typically `http://localhost:8001` for Docker Compose, or `http://localhost:8000` for Docker direct/local development)

## Steps

### Basic Upload Script

1. Open a text editor and create a new Python file.
   - Name it something like `upload_compressors.py`

2. Copy the following code into your file:
   ```python
   import requests
   
   # API endpoint (use port 8001 for Docker Compose, 8000 for Docker direct/local)
   api_url = "http://localhost:8001/api/upload"
   
   # Path to your ZIP file
   zip_file_path = "compressors.zip"
   
   # Open the ZIP file
   with open(zip_file_path, 'rb') as f:
       # Prepare the file for upload
       files = {'file': f}
       
       # Send the request
       response = requests.post(api_url, files=files)
       
       # Check if the request was successful
       if response.status_code == 200:
           # Save the Excel file
           output_filename = "output.xlsx"
           with open(output_filename, 'wb') as out:
               out.write(response.content)
           print(f"Success! Excel file saved as {output_filename}")
       else:
           # Print error information
           print(f"Error: {response.status_code}")
           try:
               error_detail = response.json()
               print(f"Details: {error_detail}")
           except:
               print(f"Response: {response.text}")
   ```

3. Update the `zip_file_path` variable with your actual ZIP file path.
   - Use the full path if the file is in a different folder
   - Example: `zip_file_path = "C:/Users/YourName/Documents/compressors.zip"`

4. Update the `api_url` if your server is at a different address.
   - Use `http://localhost:8001/api/upload` for Docker Compose
   - Use `http://localhost:8000/api/upload` for Docker direct or local development
   - Change it if the API is on a different computer

5. Save the file.

6. Open your command-line terminal and navigate to the folder containing your Python script.

7. Run the script:
   ```
   python upload_compressors.py
   ```

8. Wait for the script to complete.
   - You'll see a success message when the Excel file is saved
   - Or an error message if something went wrong

### Checking API Health First

Before uploading, you can check if the API is running:

1. Add this code before your upload code:
   ```python
   import requests
   
   # Check API health (use port 8001 for Docker Compose, 8000 for Docker direct/local)
   health_url = "http://localhost:8001/api/health"
   try:
       response = requests.get(health_url)
       if response.status_code == 200:
           health_data = response.json()
           print(f"API Status: {health_data['status']}")
           print(f"API Version: {health_data['version']}")
       else:
           print("API is not responding correctly")
   except requests.exceptions.ConnectionError:
       print("Cannot connect to API. Is the server running?")
   ```

### Processing Multiple ZIP Files

To process multiple ZIP files automatically:

1. Use this code:
   ```python
   import requests
   from pathlib import Path
   
   api_url = "http://localhost:8001/api/upload"  # Use 8001 for Docker Compose
   
   # Folder containing ZIP files
   zip_folder = Path("zip_files")
   
   # Process each ZIP file
   for zip_file in zip_folder.glob("*.zip"):
       print(f"Processing {zip_file.name}...")
       
       with open(zip_file, 'rb') as f:
           files = {'file': f}
           response = requests.post(api_url, files=files)
           
           if response.status_code == 200:
               # Save with same name but .xlsx extension
               output_file = zip_file.with_suffix('.xlsx')
               with open(output_file, 'wb') as out:
                   out.write(response.content)
               print(f"  ✓ Saved as {output_file.name}")
           else:
               print(f"  ✗ Error: {response.status_code}")
   ```

## Expected Results

After running your script successfully:
- The script will complete without errors
- An Excel file will be created in the specified location
- You'll see a success message confirming the file was saved
- The Excel file will contain separate sheets for each compressor number
- PDFs with the same compressor number will be combined into the same sheet
- Each sheet contains all compressor data from the corresponding PDFs

## Troubleshooting

- **"ModuleNotFoundError: No module named 'requests'"**: Install requests by running `pip install requests` in your terminal

- **"ConnectionError" or "Cannot connect"**: The API server is not running. Start the server or check the server address

- **"FileNotFoundError"**: The ZIP file path is incorrect. Check that the file exists and the path is spelled correctly

- **Status code 400**: Your ZIP file may be invalid or doesn't contain PDFs. Verify your ZIP file is correct

- **Status code 413**: Your ZIP file is too large. Split it into smaller files or check the size limit

- **Status code 500**: There was a server error processing your files. Check server logs or contact your administrator

- **Empty Excel file**: The response may have been an error message instead of a file. Check the response status code and error details

## Additional Information

- You can integrate this into larger Python applications
- The `requests` library handles file uploads automatically
- You can add progress bars using libraries like `tqdm` for better user experience
- Error handling can be customized based on your needs
- The API response includes headers that may contain useful information

## Example with Error Handling

Here's a more robust version with better error handling:

```python
import requests
import sys

def upload_zip_file(zip_path, api_url="http://localhost:8001/api/upload"):
    """Upload a ZIP file and return the Excel file content."""
    try:
        with open(zip_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(api_url, files=files, timeout=3600)
            
            if response.status_code == 200:
                return response.content, None
            else:
                try:
                    error_detail = response.json()
                    return None, f"Error {response.status_code}: {error_detail.get('detail', 'Unknown error')}"
                except:
                    return None, f"Error {response.status_code}: {response.text}"
                    
    except FileNotFoundError:
        return None, f"ZIP file not found: {zip_path}"
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to API server. Is it running?"
    except requests.exceptions.Timeout:
        return None, "Request timed out. The file may be too large."
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

# Usage
if __name__ == "__main__":
    zip_file = "compressors.zip"
    excel_data, error = upload_zip_file(zip_file)
    
    if error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    else:
        with open("output.xlsx", 'wb') as f:
            f.write(excel_data)
        print("Success! Excel file saved as output.xlsx")
```


# PDF Text Extraction Documentation

## Overview

This script extracts compressor data from PDF files (6000+ pages) using PyMuPDF library and converts it directly to Excel format. The extraction is optimized for memory efficiency and consistent performance throughout the entire document. The tool can process single PDFs or multiple PDFs, combining all data into a single Excel file with separate sheets for each compressor number.

## Current Configuration

- **Active Library**: PyMuPDF (fitz) only
- **Disabled Libraries**: pdfplumber and pdfminer (commented out, can be re-enabled if needed)
- **Output Format**: Excel file (.xlsx) with Date, Consumo, and Compressor columns
- **Processing Modes**: Single file, multiple files, or directory-based batch processing

## Why Incremental Processing Without Caching?

### The Problem: Memory Accumulation

When processing large PDFs (6000+ pages), traditional approaches can cause severe performance degradation:

1. **Page Object Caching**: PDF libraries often cache Page objects in memory
   - Each Page object contains layout information, character data, and metadata
   - With 6000+ pages, this can consume gigabytes of RAM
   - As memory fills up, the system starts swapping or garbage collecting aggressively
   - Result: Processing slows from ~0.05s/page to 50+ seconds/page after page 2000+

2. **Unbounded Data Structures**: Accumulating data in lists
   - Storing timing data for every page: `page_times.append(time)` 
   - After 6000 pages: ~150KB+ of unnecessary data
   - Each page's text held in memory before writing

3. **File I/O Overhead**: Opening/closing files repeatedly
   - Opening file for each batch write adds overhead
   - Calling `stat()` to check file size every 10 pages is expensive

### The Solution: Incremental Processing

Our implementation uses several strategies to prevent memory accumulation:

#### 1. Batched Writing (Every 100 Pages)
```python
BATCH_SIZE = 100
batch_buffer = []

# Collect pages in buffer
for page in pages:
    batch_buffer.append(page_text)
    
    # Write every 100 pages
    if len(batch_buffer) >= BATCH_SIZE:
        write_to_file(batch_buffer)
        batch_buffer = []  # Clear immediately
```

**Why**: Limits memory to ~100 pages worth of text at a time instead of 6000+

#### 2. Aggressive Cache Clearing (PyMuPDF)
```python
# Clear pdf._pages cache after each batch write
if len(batch_buffer) >= BATCH_SIZE:
    write_to_file(batch_buffer)
    if hasattr(pdf, '_pages') and len(pdf._pages) > BATCH_SIZE:
        pdf._pages = []  # Clear cached Page objects
        gc.collect()  # Force garbage collection
```

**Why**: Prevents Page objects from accumulating in memory. Even though we access pages one at a time, the library caches them internally.

#### 3. Incremental Statistics (No List Accumulation)
```python
# Instead of: page_times = []  # Grows unbounded
# We use:
total_time = 0.0
min_time = float('inf')
max_time = 0.0

# Update incrementally
total_time += page_time
if page_time > max_time:
    max_time = page_time
```

**Why**: Calculate statistics without storing all values. Reduces memory from ~150KB to constant ~50 bytes.

#### 4. File Handle Management
```python
# Open once, keep open
output_file = open(output_path, 'w', encoding='utf-8')

# Write multiple batches
for batch in batches:
    output_file.write(batch)
    output_file.flush()

output_file.close()  # Close at end
```

**Why**: Avoids overhead of opening/closing file repeatedly. Also cache file size manually instead of calling `stat()`.

#### 5. Page Cache Flushing
```python
page_text = page.extract_text()
page.flush_cache()  # Free page's internal cache immediately
```

**Why**: Each Page object caches layout/object information. Flushing after extraction frees this memory immediately.

## What TO Do

### ✅ Best Practices

1. **Use Batched Processing**
   - Always process in batches (100 pages recommended)
   - Clear buffers immediately after writing
   - Don't accumulate data in memory

2. **Clear Caches Regularly**
   - Clear `pdf._pages` cache every 100-500 pages
   - Flush individual page caches after extraction
   - Use `gc.collect()` hints after clearing large caches

3. **Keep File Handles Open**
   - Open output file once at the start
   - Write multiple batches to the same handle
   - Close only at the end

4. **Use Incremental Statistics**
   - Calculate running averages/min/max without storing all values
   - Only keep what you need for final statistics

5. **Monitor Memory Usage**
   - Watch for slowdowns (indicates memory pressure)
   - If slowdowns occur, reduce batch size or increase cache clearing frequency

### ✅ When to Modify

- **Change Batch Size**: If memory is tight, reduce `BATCH_SIZE` from 100 to 50
- **Adjust Cache Clearing**: If slowdowns occur, reduce `CACHE_CLEAR_INTERVAL` from 500 to 250
- **Enable Other Libraries**: Uncomment pdfplumber or pdfminer sections if needed for comparison

## What NOT To Do

### ❌ Common Mistakes

1. **Don't Access `pdf.pages` Property Directly**
   ```python
   # BAD: This caches ALL pages
   pages = pdf.pages  # Loads all 6000+ pages into memory!
   for page in pages:
       extract_text(page)
   
   # GOOD: Access by index with cache clearing
   for i in range(page_count):
       page = pdf.pages[i]  # Still caches, but we clear regularly
       extract_text(page)
       if i % 100 == 0:
           pdf._pages = []  # Clear cache
   ```

2. **Don't Accumulate Data in Lists**
   ```python
   # BAD: Unbounded growth
   page_times = []
   for page in pages:
       page_times.append(time)  # Grows to 6000+ entries
   
   # GOOD: Incremental calculation
   total_time = 0.0
   for page in pages:
       total_time += time  # Constant memory
   ```

3. **Don't Open/Close Files Repeatedly**
   ```python
   # BAD: Overhead on every batch
   for batch in batches:
       with open(file, 'a') as f:
           f.write(batch)  # Opens/closes each time
   
   # GOOD: Open once
   f = open(file, 'w')
   for batch in batches:
       f.write(batch)
   f.close()
   ```

4. **Don't Skip Cache Clearing**
   ```python
   # BAD: Pages accumulate
   for i in range(6000):
       page = pdf.pages[i]
       extract_text(page)
       # No cache clearing - memory fills up!
   
   # GOOD: Clear regularly
   for i in range(6000):
       page = pdf.pages[i]
       extract_text(page)
       if i % 100 == 0:
           pdf._pages = []
   ```

5. **Don't Call `len(pdf.pages)` Upfront**
   ```python
   # BAD: Triggers full page cache build
   page_count = len(pdf.pages)  # Builds all 6000+ pages!
   
   # GOOD: Get from metadata or detect dynamically
   page_count = pdf.doc.num_pages  # Doesn't cache pages
   ```

6. **Don't Read Entire File for Statistics**
   ```python
   # BAD: Loads entire file into memory
   with open(file, 'r') as f:
       full_text = f.read()  # Could be 100MB+
   
   # GOOD: Track size incrementally
   file_size_bytes += len(batch_text)
   ```

## Performance Characteristics

### Expected Performance
- **Speed**: ~0.03-0.06 seconds per page (consistent)
- **Memory**: ~10-50 MB process memory (stable)
- **File I/O**: Minimal overhead with batched writes

### Warning Signs
If you see these, memory is accumulating:
- Processing time increases: 0.05s → 0.1s → 1s → 10s+ per page
- Memory usage grows: 50MB → 200MB → 1GB+
- System becomes unresponsive

**Solution**: Reduce batch size, increase cache clearing frequency, or reduce `CACHE_CLEAR_INTERVAL`.

## Technical Details

### How pdfplumber Caching Works

```python
@property
def pages(self):
    if hasattr(self, "_pages"):
        return self._pages  # Return cached list
    
    # First access: Build ALL pages
    self._pages = []
    for page in all_pages:
        self._pages.append(Page(...))  # Caches everything!
    return self._pages
```

**Problem**: Even accessing `pdf.pages[0]` triggers building all pages and caching them.

**Solution**: Clear `pdf._pages = []` regularly to prevent accumulation.

### Memory Footprint Per Page

- **Page Object**: ~50-200 KB (layout, characters, metadata)
- **Extracted Text**: ~1-5 KB per page
- **100 Pages**: ~5-20 MB in memory
- **6000 Pages**: ~300 MB - 1.2 GB (without clearing!)

### Why Batch Size of 100?

- **Too Small (10)**: Excessive file I/O overhead
- **Too Large (1000)**: Memory pressure, slower cache clearing
- **Sweet Spot (100)**: Balance between I/O and memory

## Troubleshooting

### Issue: Slowdown After Page 2000+

**Symptoms**: Processing slows from 0.05s/page to 10s+/page

**Cause**: Page objects accumulating in `pdf._pages` cache

**Solution**: 
1. Reduce `CACHE_CLEAR_INTERVAL` from 500 to 100
2. Clear cache after every batch write (already implemented)
3. Add `gc.collect()` after cache clearing

### Issue: Out of Memory

**Symptoms**: Process killed or system becomes unresponsive

**Cause**: Too many pages cached or batch size too large

**Solution**:
1. Reduce `BATCH_SIZE` from 100 to 50
2. Clear cache more frequently (every 50 pages)
3. Process PDF in chunks (0-2000, then 2000-4000, etc.)

### Issue: File Not Growing

**Symptoms**: Output file stays at same size

**Cause**: File handle not flushed or batch not written

**Solution**:
1. Ensure `output_file.flush()` after each batch
2. Check that batch buffer is actually being written
3. Verify file handle is kept open between batches

## Code Structure

```
extract_pdf_text.py
├── extract_compressor_from_pdf_path()  # Extract compressor number from filename
├── parse_page_text()                  # Parse Date/Consumo from page text
├── _extract_pdf_pages()               # Core extraction logic (shared)
├── extract_pdf_to_worksheet()         # Process PDF to existing worksheet (multi-file)
├── extract_with_pymupdf()             # Single-file mode (creates workbook)
├── find_pdf_files()                   # Discover PDFs in directory
├── process_multiple_pdfs()             # Orchestrate multi-PDF processing
├── extract_with_pdfplumber()          # DISABLED - commented out
├── extract_with_pdfminer()            # DISABLED - commented out
└── main()                              # CLI interface and mode detection
```

## Multi-PDF Processing

The script supports three processing modes:

### Single File Mode
- Processes one PDF file
- Creates Excel file with same name as PDF
- Backward compatible with original functionality

### Multiple Files Mode
- Accepts multiple PDF file paths as arguments
- Combines all data into single Excel file with separate sheets per compressor
- Requires `-o` flag to specify output filename
- Continues processing even if individual files fail

### Directory Mode
- Processes all PDF files in a directory
- Uses `-d/--directory` flag
- Automatically discovers PDF files
- Combines all data into single Excel file with separate sheets per compressor

## Excel Output Format

The script creates Excel files with **separate sheets for each compressor number** to handle Excel's row limit of 1,048,576 rows per sheet.

**Sheet Organization:**
- Each compressor number gets its own sheet (e.g., "Compressor 1", "Compressor 4", "Compressor 5")
- Multiple PDFs with the same compressor number are automatically combined into the same sheet
- Sheet names are sanitized to comply with Excel's naming rules (max 31 characters, no special characters)

**Each sheet contains:**
- **Write-only mode**: Uses openpyxl's WriteOnlyWorksheet for memory efficiency
- **Headers**: First row contains "Date", "Consumo", "Compressor"
- **Data rows**: Each row contains date/time string, numeric consumo value, and compressor name
- **Batch writing**: Rows written in batches of 100 to manage memory

**Implementation Details:**
- Uses a dictionary (`worksheets`) to track worksheets by compressor name
- Extracts compressor name from PDF filename before processing
- Creates new worksheet with headers when encountering a new compressor
- Reuses existing worksheet when processing PDFs with the same compressor number

## Error Handling

- Individual PDF failures don't stop batch processing
- Failed files are tracked and reported in summary
- Partial Excel files are saved even if some PDFs fail
- Clear error messages for common issues (missing files, invalid filenames, etc.)

## Re-enabling Other Libraries

To enable pdfplumber or pdfminer:

1. Uncomment the extraction section in `main()`
2. Ensure the same optimizations are applied:
   - Batched writing
   - Cache clearing
   - Incremental statistics
   - File handle management

## Summary

**Key Principle**: Never accumulate data in memory. Process incrementally, write frequently, clear caches aggressively.

The optimizations in this script ensure consistent performance even for 6000+ page PDFs by:
- Limiting memory to ~100 pages at a time
- Clearing caches every 100-500 pages
- Using incremental calculations instead of lists
- Keeping file handles open
- Flushing page caches immediately
- Writing Excel rows in batches
- Using write-only Excel mode for memory efficiency

This approach trades a small amount of CPU overhead (cache rebuilding) for massive memory savings and consistent performance.

## Usage Examples

```bash
# Single PDF file
python extract_pdf_text.py COMPRESOR4-ABR-JUN-25.PDF

# Multiple PDFs
python extract_pdf_text.py file1.pdf file2.pdf file3.pdf -o combined.xlsx

# Directory processing
python extract_pdf_text.py -d tests/data/ -o combined.xlsx
```


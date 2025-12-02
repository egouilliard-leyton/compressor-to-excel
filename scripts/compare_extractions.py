#!/usr/bin/env python3
"""
PDF Text Extraction Comparison Utility

Compares the outputs from three different PDF extraction libraries:
- pdfplumber
- PyMuPDF (fitz)
- pdfminer.six
"""

import os
from pathlib import Path


def get_file_stats(file_path):
    """Get statistics about a text file."""
    if not file_path.exists():
        return None
    
    stat = file_path.stat()
    size_mb = stat.st_size / (1024 * 1024)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        char_count = len(content)
        line_count = len(content.splitlines())
        word_count = len(content.split())
        
        # Count non-empty lines
        non_empty_lines = len([line for line in content.splitlines() if line.strip()])
    
    return {
        'size_mb': size_mb,
        'char_count': char_count,
        'line_count': line_count,
        'word_count': word_count,
        'non_empty_lines': non_empty_lines
    }


def get_sample_text(file_path, num_lines=20, start_line=0):
    """Get a sample of text from a file."""
    if not file_path.exists():
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
        if start_line >= len(lines):
            start_line = 0
        
        end_line = min(start_line + num_lines, len(lines))
        sample = ''.join(lines[start_line:end_line])
    
    return sample


def compare_extractions():
    """Compare the three extraction outputs."""
    script_dir = Path(__file__).parent
    output_dir = script_dir.parent / "tests" / "data"
    
    files = {
        'pdfplumber': output_dir / "COMPRESOR4-ABR-JUN-25-pdfplumber.txt",
        'pymupdf': output_dir / "COMPRESOR4-ABR-JUN-25-pymupdf.txt",
        'pdfminer': output_dir / "COMPRESOR4-ABR-JUN-25-pdfminer.txt"
    }
    
    print("=" * 80)
    print("PDF TEXT EXTRACTION COMPARISON")
    print("=" * 80)
    print()
    
    # Check which files exist
    existing_files = {name: path for name, path in files.items() if path.exists()}
    
    if not existing_files:
        print("No extraction files found. Please run extract_pdf_text.py first.")
        return
    
    # File Statistics
    print("FILE STATISTICS")
    print("-" * 80)
    print(f"{'Library':<15} | {'Size (MB)':>12} | {'Chars':>15} | {'Lines':>12} | {'Words':>12} | {'Non-empty':>12}")
    print("-" * 80)
    
    stats = {}
    for name, path in existing_files.items():
        stat = get_file_stats(path)
        if stat:
            stats[name] = stat
            print(f"{name:<15} | {stat['size_mb']:>12.2f} | {stat['char_count']:>15,} | "
                  f"{stat['line_count']:>12,} | {stat['word_count']:>12,} | "
                  f"{stat['non_empty_lines']:>12,}")
    
    print()
    
    # Sample Text Comparison
    print("=" * 80)
    print("SAMPLE TEXT COMPARISON (First 20 lines)")
    print("=" * 80)
    print()
    
    for name, path in existing_files.items():
        print(f"{name.upper()}")
        print("-" * 80)
        sample = get_sample_text(path, num_lines=20, start_line=0)
        if sample:
            # Truncate if too long
            if len(sample) > 1000:
                sample = sample[:1000] + "\n... (truncated)"
            print(sample)
        else:
            print("(No content)")
        print()
    
    # Middle Sample
    print("=" * 80)
    print("SAMPLE TEXT COMPARISON (Middle section - around line 1000)")
    print("=" * 80)
    print()
    
    for name, path in existing_files.items():
        print(f"{name.upper()}")
        print("-" * 80)
        sample = get_sample_text(path, num_lines=20, start_line=1000)
        if sample:
            # Truncate if too long
            if len(sample) > 1000:
                sample = sample[:1000] + "\n... (truncated)"
            print(sample)
        else:
            print("(No content)")
        print()
    
    # Format Analysis
    print("=" * 80)
    print("FORMAT ANALYSIS")
    print("=" * 80)
    print()
    
    for name, path in existing_files.items():
        print(f"{name.upper()}:")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check for page markers
            page_markers = content.count('=== PAGE')
            has_page_markers = page_markers > 0
            
            # Check for form feed characters
            form_feeds = content.count('\f')
            
            # Check for common table indicators
            tabs = content.count('\t')
            multiple_spaces = content.count('  ')  # Double spaces
            
            print(f"  Page markers (=== PAGE): {page_markers}")
            print(f"  Form feed characters (\\f): {form_feeds}")
            print(f"  Tab characters: {tabs:,}")
            print(f"  Double spaces: {multiple_spaces:,}")
            print()
    
    # Recommendations
    print("=" * 80)
    print("RECOMMENDATIONS FOR TABLE EXTRACTION")
    print("=" * 80)
    print()
    print("For extracting tables from PDFs:")
    print()
    print("1. pdfplumber:")
    print("   - Best for structured table extraction")
    print("   - Can extract tables directly as DataFrames")
    print("   - Preserves table structure and cell boundaries")
    print("   - Recommended if tables are well-formatted")
    print()
    print("2. PyMuPDF (fitz):")
    print("   - Fast extraction")
    print("   - Good text quality")
    print("   - May require post-processing for table structure")
    print("   - Good for quick text extraction")
    print()
    print("3. pdfminer.six:")
    print("   - Low-level control")
    print("   - Can extract with layout information")
    print("   - More complex to use but very flexible")
    print("   - Good for complex or unusual layouts")
    print()


if __name__ == "__main__":
    compare_extractions()


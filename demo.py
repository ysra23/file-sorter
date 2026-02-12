#!/usr/bin/env python3
"""
Demo script to test the file sorter with sample files.
Creates sample files and runs the sorter on them.
"""

import os
from pathlib import Path

def create_sample_files():
    """Create sample files for testing the file sorter."""
    
    # Create test directory
    test_dir = Path("./files_to_sort")
    test_dir.mkdir(exist_ok=True)
    
    print("Creating sample files...")
    
    # Sample 1: Markdown with title
    with open(test_dir / "2024-01-15_document_001.md", "w") as f:
        f.write("""# Annual Report 2024

This is the annual report for the year 2024.
It contains important financial information.
""")
    
    # Sample 2: Text file with Title: prefix
    with open(test_dir / "random_file_name_123.txt", "w") as f:
        f.write("""Title: Meeting Notes - Q4 Review

Attendees: John, Sarah, Mike
Date: January 15, 2024

Key discussion points...
""")
    
    # Sample 3: HTML file
    with open(test_dir / "web_page_old.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Product Launch Strategy</title>
</head>
<body>
    <h1>Product Launch Strategy</h1>
    <p>Our plan for launching the new product...</p>
</body>
</html>
""")
    
    # Sample 4: File with underlined title
    with open(test_dir / "project_notes.txt", "w") as f:
        f.write("""Project Phoenix Documentation
==============================

This project aims to revolutionize...
""")
    
    # Sample 5: Simple text file (title from first line)
    with open(test_dir / "messy-file_name_2024.txt", "w") as f:
        f.write("""Customer Feedback Summary

We received positive feedback from 95% of customers.
The main suggestions for improvement were...
""")
    
    # Sample 6: File that will use filename as title
    with open(test_dir / "important_data_backup.txt", "w") as f:
        f.write("""[Binary-like content that doesn't have a clear title]
0x4A 0x8B 0x2C 0x9F
Data entries: 1, 2, 3, 4, 5
""")
    
    # Sample 7: Python file with docstring
    with open(test_dir / "script_v2_final.py", "w") as f:
        f.write("""#!/usr/bin/env python3
# Data Analysis Tool

def main():
    print("Analyzing data...")

if __name__ == "__main__":
    main()
""")
    
    print(f"✅ Created 7 sample files in {test_dir}")
    print("\nSample files created:")
    for file in sorted(test_dir.iterdir()):
        print(f"  - {file.name}")
    
    return test_dir

def run_demo():
    """Run the complete demo."""
    
    print("=" * 80)
    print("FILE SORTER DEMO")
    print("=" * 80)
    print() 
    
    # Create sample files
    test_dir = create_sample_files()
    
    print("\n" + "=" * 80)
    print("Now running the file sorter...")
    print("=" * 80)
    print() 
    
    # Import and run the file sorter
    import file_sorter
    
    # Run with renaming enabled
    file_sorter.RENAME_FILES = True
    file_sorter.main()
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE!")
    print("=" * 80)
    print("\nCheck the following:")
    print("  📂 sorted_files/        - Your organized files")
    print("  📄 file_sorting_report.txt - Detailed report")
    print() 

if __name__ == "__main__":
    run_demo()
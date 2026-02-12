#!/usr/bin/env python3
"""
File Sorting and Organization Script
Sorts files, extracts titles from content and filenames, optionally renames files,
and generates a detailed report.
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import mimetypes

# Configuration
RENAME_FILES = False  # Set to True to rename files based on extracted titles
SOURCE_DIRECTORY = "./files_to_sort"  # Directory containing files to process
OUTPUT_DIRECTORY = "./sorted_files"  # Where sorted files will be placed
REPORT_PATH = "./file_sorting_report.txt"  # Path for the generated report


class FileProcessor:
    """Handles file processing, title extraction, and organization."""
    
    def __init__(self, source_dir: str, output_dir: str, rename: bool = False):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.rename_files = rename
        self.file_data: List[Dict] = []
        
    def extract_title_from_content(self, filepath: Path) -> Optional[str]:
        """
        Extract title from file content.
        Supports text files, markdown, HTML, etc.
        """
        try:
            # Check if file is likely text-based
            mime_type, _ = mimetypes.guess_type(str(filepath))
            if mime_type and not mime_type.startswith('text'):
                return None
                
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(1000)  # Read first 1000 chars
                
            # Try different title extraction patterns
            patterns = [
                r'^#\s+(.+)$',  # Markdown H1
                r'^Title:\s*(.+)$',  # Title: prefix
                r'<title>(.+)</title>',  # HTML title
                r'<h1>(.+)</h1>',  # HTML H1
                r'^(.+)\n[=]+\n',  # Underlined title
            ]
            
            for pattern in patterns:
                match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
                if match:
                    return match.group(1).strip()
                    
            # If no pattern matches, try first non-empty line
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            if lines:
                # Return first line if it looks like a title (not too long)
                first_line = lines[0]
                if len(first_line) < 100 and not first_line.startswith(('/', '*', '#')):
                    return first_line
                    
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            
        return None
    
    def extract_title_from_filename(self, filepath: Path) -> str:
        """
        Extract a clean title from the filename.
        """
        # Remove extension and clean up
        name = filepath.stem
        
        # Replace common separators with spaces
        name = re.sub(r'[_\-\.]+', ' ', name)
        
        # Remove dates in common formats (YYYY-MM-DD, YYYYMMDD, etc.)
        name = re.sub(r'\d{4}[-_]??\d{2}[-_]??\d{2}', '', name)
        
        # Remove numbers at start/end
        name = re.sub(r'^\d+\s*', '', name)
        name = re.sub(r'\s*\d+$', '', name)
        
        # Clean up extra whitespace
        name = ' '.join(name.split())
        
        # Title case
        return name.title() if name else filepath.name
    
    def sanitize_filename(self, title: str, extension: str) -> str:
        """
        Convert a title into a valid filename.
        """
        # Remove invalid filename characters
        filename = re.sub(r'[<>:"/\\|?*]', '', title)
        
        # Replace spaces and multiple separators
        filename = re.sub(r'\s+', '_', filename)
        
        # Limit length
        max_length = 200
        if len(filename) > max_length:
            filename = filename[:max_length]
            
        # Ensure it doesn't end with a dot or space
        filename = filename.rstrip('. ')
        
        return f"{filename}{extension}"
    
    def process_files(self):
        """
        Process all files in the source directory.
        """
        if not self.source_dir.exists():
            raise FileNotFoundError(f"Source directory not found: {self.source_dir}")
            
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Get all files (not directories)
        files = [f for f in self.source_dir.rglob('*') if f.is_file()]
        
        print(f"Processing {len(files)} files...")
        
        for filepath in files:
            # Extract titles
            title_from_content = self.extract_title_from_content(filepath)
            title_from_filename = self.extract_title_from_filename(filepath)
            
            # Determine which title to use
            final_title = title_from_content or title_from_filename
            source = "content" if title_from_content else "filename"
            
            # Determine new filename
            if self.rename_files and final_title:
                new_filename = self.sanitize_filename(final_title, filepath.suffix)
            else:
                new_filename = filepath.name
                
            # Store file data
            file_info = {
                'original_path': filepath,
                'original_name': filepath.name,
                'title': final_title,
                'title_from_content': title_from_content,
                'title_from_filename': title_from_filename,
                'title_source': source,
                'new_filename': new_filename,
                'extension': filepath.suffix,
                'size': filepath.stat().st_size,
            }
            
            self.file_data.append(file_info)
            
            # Copy/move file to output directory
            output_path = self.output_dir / new_filename
            
            # Handle filename conflicts
            counter = 1
            while output_path.exists():
                stem = Path(new_filename).stem
                ext = Path(new_filename).suffix
                output_path = self.output_dir / f"{stem}_{counter}{ext}"
                counter += 1
                
            # Copy the file
            import shutil
            shutil.copy2(filepath, output_path)
            file_info['output_path'] = output_path
            
        print(f"Processed {len(self.file_data)} files successfully!")
        
    def generate_report(self, report_path: str):
        """
        Generate a detailed report of the sorting operation.
        """
        titles_from_content = sum(1 for f in self.file_data if f['title_from_content'])
        titles_from_filename = sum(1 for f in self.file_data if not f['title_from_content'])
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("📁 SORTED FILES REPORT\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Summary statistics
            f.write("SUMMARY\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Files:              {len(self.file_data)}\n")
            f.write(f"Titles from Content:      {titles_from_content}\n")
            f.write(f"Titles from Filename:     {titles_from_filename}\n")
            f.write(f"Files Renamed:            {'Yes' if self.rename_files else 'No'}\n")
            f.write(f"Source Directory:         {self.source_dir}\n")
            f.write(f"Output Directory:         {self.output_dir}\n")
            f.write("\n")
            
            # Detailed file list
            f.write("DETAILED FILE LIST\n")
            f.write("-" * 80 + "\n")
            f.write(f"{'Title':<40} {'Filename':<30} {'Source':<10}\n")
            f.write("-" * 80 + "\n")
            
            for file_info in self.file_data:
                title = file_info['title'][:37] + "..." if len(file_info['title']) > 40 else file_info['title']
                filename = file_info['new_filename'][:27] + "..." if len(file_info['new_filename']) > 30 else file_info['new_filename']
                source = file_info['title_source']
                
                f.write(f"{title:<40} {filename:<30} {source:<10}\n")
                
            f.write("-" * 80 + "\n")
            f.write(f"\nReport saved to: {report_path}\n")
            
        print(f"\nReport generated: {report_path}")


def main():
    """
    Main entry point for the file sorting script.
    """
    print("=" * 80)
    print("FILE SORTING SCRIPT")
    print("=" * 80)
    print() 
    
    # Create processor
    processor = FileProcessor(
        source_dir=SOURCE_DIRECTORY,
        output_dir=OUTPUT_DIRECTORY,
        rename=RENAME_FILES
    )
    
    try:
        # Process files
        processor.process_files()
        
        # Generate report
        processor.generate_report(REPORT_PATH)
        
        print("\n✅ File sorting completed successfully!")
        print(f"📂 Sorted files located in: {OUTPUT_DIRECTORY}")
        print(f"📄 Report available at: {REPORT_PATH}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
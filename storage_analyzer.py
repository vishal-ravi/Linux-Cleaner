import os
import psutil
from openpyxl import Workbook

# File categories based on extensions
CATEGORIES = {
    'Music': ['mp3', 'wav', 'flac'],
    'Videos': ['mp4', 'mkv', 'avi'],
    'Images': ['jpg', 'jpeg', 'png', 'gif'],
    'Documents': ['pdf', 'docx', 'xlsx', 'pptx'],
    'Archives': ['zip', 'tar', 'gz', 'rar'],
    'Programs': ['exe', 'bin', 'sh'],
    'Others': []
}

def get_disk_usage(path='/'):
    """Get the disk usage for a specific path."""
    usage = psutil.disk_usage(path)
    return {
        'total': usage.total // (2**30),  # Convert to GB
        'used': usage.used // (2**30),    # Convert to GB
        'free': usage.free // (2**30),    # Convert to GB
        'percent': usage.percent
    }

def analyze_directory(path='/'):
    """Analyze the directory to find all files and categorize them."""
    categorized_files = {category: [] for category in CATEGORIES.keys()}

    for root, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            size = os.path.getsize(full_path)
            ext = file.split('.')[-1].lower()

            # Determine the file category
            category = 'Others'
            for cat, extensions in CATEGORIES.items():
                if ext in extensions:
                    category = cat
                    break

            categorized_files[category].append((full_path, size))

    return categorized_files

def save_to_excel(categorized_files, disk_usage, file_path='storage_analysis.xlsx'):
    """Save the categorized files and disk usage into an Excel file."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Storage Analysis"

    # Header for disk usage
    ws.append(["Disk Usage"])
    ws.append(["Total (GB)", "Used (GB)", "Free (GB)", "Percent Used"])
    ws.append([disk_usage['total'], disk_usage['used'], disk_usage['free'], disk_usage['percent']])
    
    ws.append([])  # Empty row
    
    # Header for categorized files
    for category, files in categorized_files.items():
        if files:  # Check if the category has any files
            ws.append([f"{category} Files"])
            ws.append(["File Path", "Size (MB)"])
            for file, size in sorted(files, key=lambda x: x[1], reverse=True):
                ws.append([file, round(size / (2**20), 2)])  # Convert size to MB
            ws.append([])  # Empty row for separation

    wb.save(file_path)

def find_large_files(path='/', number_of_files=20):
    """Find the largest files in the system."""
    command = f'sudo find {path} -type f -exec du -h {{}} + | sort -rh | head -n {number_of_files}'
    output = check_output(command, shell=True).decode('utf-8')
    return output

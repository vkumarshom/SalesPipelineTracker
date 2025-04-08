import os
import re
from datetime import datetime

def get_file_type(filename):
    """Get the type of the file based on its extension."""
    ext = os.path.splitext(filename)[1].lower()
    
    if ext in ['.py']:
        return 'Python'
    elif ext in ['.html', '.htm']:
        return 'HTML'
    elif ext in ['.css']:
        return 'CSS'
    elif ext in ['.js']:
        return 'JavaScript'
    elif ext in ['.sql']:
        return 'SQL'
    elif ext in ['.md']:
        return 'Markdown'
    elif ext in ['.svg', '.png', '.jpg', '.jpeg', '.gif']:
        return 'Image'
    else:
        return 'Other'

def get_file_purpose(path, filename):
    """Get the purpose of the file based on its path and name."""
    if 'admin.py' in filename:
        return 'Django Admin Configuration'
    elif 'models.py' in filename:
        return 'Database Models'
    elif 'views.py' in filename:
        return 'View Controllers'
    elif 'forms.py' in filename:
        return 'Form Definitions'
    elif 'urls.py' in filename:
        return 'URL Routing'
    elif 'utils.py' in filename:
        return 'Utility Functions'
    elif 'settings.py' in filename:
        return 'Django Settings'
    elif 'wsgi.py' in filename or 'asgi.py' in filename:
        return 'Server Configuration'
    elif 'migrations' in path:
        return 'Database Migration'
    elif 'static/css' in path or 'staticfiles/css' in path:
        return 'Stylesheet'
    elif 'static/js' in path or 'staticfiles/js' in path:
        return 'JavaScript Function'
    elif 'static/assets' in path or 'staticfiles/assets' in path:
        return 'Static Asset'
    elif 'templates' in path and filename.endswith('.html'):
        return 'HTML Template'
    elif 'media' in path:
        return 'User Media'
    elif filename == 'manage.py':
        return 'Django Management Script'
    elif filename.endswith('.sql'):
        return 'SQL Schema/Data'
    elif filename == 'README.md':
        return 'Project Documentation'
    else:
        return 'Auxiliary File'

def count_lines(file_path):
    """Count the number of lines in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

def get_file_info(root_path, file_path):
    """Get comprehensive information about a file."""
    full_path = os.path.join(root_path, file_path)
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(full_path)
    file_type = get_file_type(file_name)
    try:
        modified_time = datetime.fromtimestamp(os.path.getmtime(full_path))
        modified = modified_time.strftime('%Y-%m-%d %H:%M:%S')
    except:
        modified = "Unknown"
    
    lines = 0
    if file_type in ['Python', 'HTML', 'CSS', 'JavaScript', 'SQL', 'Markdown', 'Text']:
        lines = count_lines(full_path)
    
    purpose = get_file_purpose(file_path, file_name)
    
    return {
        'path': file_path,
        'name': file_name,
        'type': file_type,
        'size': file_size,
        'lines': lines,
        'modified': modified,
        'purpose': purpose
    }

def format_size(size_bytes):
    """Format file size in a human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def generate_project_files_index(root_path='.', output_file='project_files.md'):
    """Generate a Markdown file with a comprehensive project file index."""
    # Define key project directories
    project_dirs = [
        'astrology',
        'metamystic',
        'templates',
        'static',
        'media'
    ]
    
    # Define ignore patterns
    ignore_patterns = [
        r'^\.git',
        r'^\.vscode',
        r'^__pycache__',
        r'\.pyc$',
        r'\.pyo$',
        r'\.pyd$',
        r'\.gitignore$',
        r'\.DS_Store$',
        r'\.env$',
        r'\.venv',
        r'node_modules',
        r'venv',
        r'\.idea',
        r'\.pythonlibs',
        r'\.cache',
        r'celestial_insights_astrology.zip'
    ]
    
    # Compile regex patterns
    ignore_regex = [re.compile(pattern) for pattern in ignore_patterns]
    
    file_info_list = []
    
    # Walk through directory structure
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Skip the directory if it's not in our project dirs or parent of project dirs
        is_in_project_dir = False
        for project_dir in project_dirs:
            if dirpath == os.path.join(root_path, project_dir) or dirpath.startswith(os.path.join(root_path, project_dir) + os.sep):
                is_in_project_dir = True
                break
        
        # Include root directory files
        if dirpath == root_path:
            is_in_project_dir = True
        
        if not is_in_project_dir:
            continue
        
        # Skip ignored directories
        dirnames[:] = [d for d in dirnames if not any(pattern.search(d) for pattern in ignore_regex)]
        
        # Process files in current directory
        for filename in filenames:
            # Skip ignored files
            if any(pattern.search(filename) for pattern in ignore_regex):
                continue
            
            # Get relative path from root
            rel_path = os.path.join(dirpath, filename)
            if rel_path.startswith(root_path):
                rel_path = rel_path[len(root_path):].lstrip(os.sep)
            
            file_info = get_file_info(root_path, rel_path)
            file_info_list.append(file_info)
    
    # Sort files by type and then by path
    file_info_list.sort(key=lambda x: (x['type'], x['path']))
    
    # Group files by type
    files_by_type = {}
    for file_info in file_info_list:
        file_type = file_info['type']
        if file_type not in files_by_type:
            files_by_type[file_type] = []
        files_by_type[file_type].append(file_info)
    
    # Generate Markdown output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# MetaMystic Project Files Index\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # File counts by type
        f.write("## File Statistics\n\n")
        f.write("| File Type | Count | Total Lines | Total Size |\n")
        f.write("|-----------|-------|-------------|------------|\n")
        
        grand_total_files = 0
        grand_total_lines = 0
        grand_total_size = 0
        
        for file_type, files in sorted(files_by_type.items()):
            type_count = len(files)
            type_lines = sum(file['lines'] for file in files)
            type_size = sum(file['size'] for file in files)
            
            grand_total_files += type_count
            grand_total_lines += type_lines
            grand_total_size += type_size
            
            f.write(f"| {file_type} | {type_count} | {type_lines} | {format_size(type_size)} |\n")
        
        f.write(f"| **TOTAL** | **{grand_total_files}** | **{grand_total_lines}** | **{format_size(grand_total_size)}** |\n")
        f.write("\n")
        
        # Files by type
        for file_type, files in sorted(files_by_type.items()):
            f.write(f"## {file_type} Files\n\n")
            f.write("| File | Purpose | Lines | Size | Last Modified |\n")
            f.write("|------|---------|-------|------|---------------|\n")
            
            for file_info in sorted(files, key=lambda x: x['path']):
                f.write(f"| `{file_info['path']}` | {file_info['purpose']} | {file_info['lines']} | {format_size(file_info['size'])} | {file_info['modified']} |\n")
            
            f.write("\n")
    
    print(f"Project files index generated: {output_file}")

if __name__ == "__main__":
    generate_project_files_index()
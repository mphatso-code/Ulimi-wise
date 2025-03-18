import re
import os
import uuid
import logging
from werkzeug.utils import secure_filename

def is_valid_email(email):
    """
    Validate an email address format
    
    Args:
        email (str): Email address to validate
    
    Returns:
        bool: True if the email format is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def allowed_file(filename, allowed_extensions=None):
    """
    Check if a file has an allowed extension
    
    Args:
        filename (str): Name of the file to check
        allowed_extensions (set): Set of allowed file extensions
    
    Returns:
        bool: True if the file extension is allowed, False otherwise
    """
    if allowed_extensions is None:
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'svg', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt'}
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_file(file, upload_folder, allowed_extensions=None):
    """
    Save an uploaded file with a secure filename
    
    Args:
        file: File object from request.files
        upload_folder (str): Folder where the file should be saved
        allowed_extensions (set): Set of allowed file extensions
    
    Returns:
        str: Filename of the saved file or None if file could not be saved
    """
    if file and allowed_file(file.filename, allowed_extensions):
        # Create a secure filename
        filename = secure_filename(file.filename)
        
        # Generate a unique filename to avoid overwriting
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # Ensure upload folder exists
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save the file
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        return unique_filename
    
    return None


def get_file_url(filename, upload_folder):
    """
    Get the URL for an uploaded file
    
    Args:
        filename (str): Name of the file
        upload_folder (str): Folder where the file is stored
    
    Returns:
        str: URL path to the file
    """
    if filename:
        return f"/{upload_folder}/{filename}"
    return None


def format_datetime(datetime_obj, format_str="%Y-%m-%d %H:%M"):
    """
    Format a datetime object to a string
    
    Args:
        datetime_obj: Datetime object to format
        format_str (str): Format string
    
    Returns:
        str: Formatted datetime string
    """
    if datetime_obj:
        return datetime_obj.strftime(format_str)
    return ""


def format_currency(amount, currency="$"):
    """
    Format a number as currency
    
    Args:
        amount (float): Amount to format
        currency (str): Currency symbol
    
    Returns:
        str: Formatted currency string
    """
    try:
        return f"{currency}{float(amount):.2f}"
    except (ValueError, TypeError):
        return f"{currency}0.00"


def truncate_text(text, max_length=100):
    """
    Truncate text to a specified maximum length
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length of the truncated text
    
    Returns:
        str: Truncated text with ellipsis if needed
    """
    if text and len(text) > max_length:
        return text[:max_length].rsplit(' ', 1)[0] + '...'
    return text


def get_pagination_range(page, total_pages, shown_pages=5):
    """
    Get the range of page numbers to display in pagination
    
    Args:
        page (int): Current page number
        total_pages (int): Total number of pages
        shown_pages (int): Number of page links to show
    
    Returns:
        list: Range of page numbers to display
    """
    # Ensure page and total_pages are integers
    page = int(page)
    total_pages = int(total_pages)
    
    # Handle cases where there are few pages
    if total_pages <= shown_pages:
        return range(1, total_pages + 1)
    
    # Calculate the pages to show
    half = shown_pages // 2
    
    if page <= half:
        # Near the beginning
        return range(1, shown_pages + 1)
    elif page + half >= total_pages:
        # Near the end
        return range(total_pages - shown_pages + 1, total_pages + 1)
    else:
        # In the middle
        return range(page - half, page + half + 1)

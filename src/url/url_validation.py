from urllib.parse import urlparse
import validators

def validate_and_extract_homepage(url: str) -> str | None:
    """
    Validates a URL (with or without protocol) and extracts its standardized homepage.
    Returns the homepage string if valid, or None if invalid.
    """
    clean_url = url.strip()
    
    # 1. Standardize format by prepending 'http://' if protocol is missing
    if not clean_url.startswith(('http://', 'https://', 'ftp://')):
        clean_url = f"http://{clean_url}"
        
    # 2. Validate the standardized URL
    if not validators.url(clean_url):
        return None  # Or raise an error, depending on your needs
        
    # 3. Parse and extract the netloc (domain)
    parsed = urlparse(clean_url)
    
    # 4. Return the standardized root homepage
    return f"https://{parsed.netloc}"

import platform
import os

def find_base_path():
    """Return appropriate paths based on the operating system"""
    system = platform.system().lower()
    
    if system == 'windows':
        return r"C:\sap-project\server\schools"
    
    else:  # Linux, macOS, etc.
        home_dir = os.path.expanduser("~")
        return os.path.join(home_dir, "sap-project", "server", "schools")

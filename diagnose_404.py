"""
EthioPrice Dashboard - 404 Error Diagnostic Tool

This script helps identify why you're getting a 404 error when trying to access
your dashboard. It checks file existence, permissions, and server configuration.

Usage:
    python diagnose_404.py
"""

import os
import sys
import subprocess
import socket
from pathlib import Path

# ANSI Colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_header(title):
    """Print section header"""
    print(f"\n{BOLD}{BLUE}{'=' * 70}{RESET}")
    print(f"{BOLD}{BLUE}{title}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 70}{RESET}\n")

def print_success(message):
    """Print success message"""
    print(f"{GREEN}✓ {message}{RESET}")

def print_warning(message):
    """Print warning message"""
    print(f"{YELLOW}⚠ {message}{RESET}")

def print_error(message):
    """Print error message"""
    print(f"{RED}✗ {message}{RESET}")

def print_info(message):
    """Print info message"""
    print(f"{BLUE}ℹ {message}{RESET}")

def check_python_version():
    """Check Python version"""
    print_header("Step 1: Python Environment")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"Python Version: {version_str}")
    
    if version.major >= 3:
        print_success(f"Python {version_str} is installed (compatible)")
        return True
    else:
        print_error(f"Python {version_str} detected. Need Python 3.x")
        return False

def check_web_directory():
    """Check if web directory exists and contains required files"""
    print_header("Step 2: Web Directory Check")
    
    # Get project root
    script_dir = Path(__file__).parent.absolute()
    web_dir = script_dir / 'web'
    
    print(f"Project Root: {script_dir}")
    print(f"Web Directory: {web_dir}")
    
    # Check if web directory exists
    if not web_dir.exists():
        print_error(f"Web directory not found at: {web_dir}")
        print_info("Create the directory or check the path")
        return False, None
    
    print_success(f"Web directory exists: {web_dir}")
    
    # Check for required files
    required_files = ['index.html', 'script.js']
    missing_files = []
    
    print("\nChecking required files:")
    for filename in required_files:
        filepath = web_dir / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print_success(f"{filename} exists ({size:,} bytes)")
        else:
            print_error(f"{filename} NOT FOUND")
            missing_files.append(filename)
    
    if missing_files:
        print_error(f"Missing files: {', '.join(missing_files)}")
        return False, web_dir
    
    return True, web_dir

def check_file_permissions(web_dir):
    """Check if files are readable"""
    print_header("Step 3: File Permissions")
    
    index_file = web_dir / 'index.html'
    script_file = web_dir / 'script.js'
    
    for filepath in [index_file, script_file]:
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read(100)  # Read first 100 chars
                print_success(f"{filepath.name} is readable")
            except PermissionError:
                print_error(f"{filepath.name} - Permission denied")
                return False
            except Exception as e:
                print_error(f"{filepath.name} - Error: {str(e)}")
                return False
    
    return True

def check_port_availability():
    """Check if port 8080 is available"""
    print_header("Step 4: Port Availability")
    
    ports_to_check = [8080, 8081, 5000]
    
    for port in ports_to_check:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            print_warning(f"Port {port} is IN USE (server may already be running)")
        else:
            print_success(f"Port {port} is AVAILABLE")

def provide_launch_commands(web_dir):
    """Provide exact commands to launch the server"""
    print_header("Step 5: Launch Commands")
    
    print(f"{BOLD}To start the HTTP server, run these commands:{RESET}\n")
    
    # Windows Command Prompt
    print(f"{BOLD}Windows Command Prompt (cmd):{RESET}")
    print(f"cd {web_dir}")
    print(f"python -m http.server 8080")
    
    print(f"\n{BOLD}Windows PowerShell:{RESET}")
    print(f"cd \"{web_dir}\"")
    print(f"python -m http.server 8080")
    
    print(f"\n{BOLD}Alternative (if 'python' doesn't work):{RESET}")
    print(f"cd {web_dir}")
    print(f"py -m http.server 8080")
    
    print(f"\n{BOLD}Then open in browser:{RESET}")
    print(f"http://localhost:8080/")
    print(f"http://localhost:8080/index.html")

def test_http_server(web_dir):
    """Try to start HTTP server and test it"""
    print_header("Step 6: HTTP Server Test (Optional)")
    
    print("Would you like to test the HTTP server now? (y/n): ", end='')
    response = input().strip().lower()
    
    if response != 'y':
        print("Skipping server test.")
        return
    
    print(f"\nStarting HTTP server on port 8080...")
    print(f"Server will run for 10 seconds...")
    print(f"Open browser to: http://localhost:8080/\n")
    
    try:
        # Change to web directory and start server
        os.chdir(web_dir)
        
        # Start server process
        if sys.platform == 'win32':
            cmd = ['python', '-m', 'http.server', '8080']
        else:
            cmd = ['python3', '-m', 'http.server', '8080']
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print_success("Server started! Check http://localhost:8080/ in your browser")
        print("Press Ctrl+C to stop the server...")
        
        try:
            # Wait for user to stop
            process.wait()
        except KeyboardInterrupt:
            print("\nStopping server...")
            process.terminate()
            process.wait()
            print_success("Server stopped")
            
    except FileNotFoundError:
        print_error("Python command not found. Try 'py' instead of 'python'")
    except Exception as e:
        print_error(f"Error starting server: {str(e)}")

def provide_troubleshooting_tips():
    """Provide additional troubleshooting tips"""
    print_header("Troubleshooting Tips")
    
    tips = [
        "If you get 404 error, make sure you're in the correct directory",
        "The server must be run from the 'web' directory, not the project root",
        "Check browser console (F12) for JavaScript errors",
        "Try clearing browser cache (Ctrl + Shift + Delete)",
        "Try opening in Incognito/Private window",
        "Make sure no firewall is blocking localhost connections",
        "If port 8080 is busy, try port 8081 or 9000",
        "The URL should be http://localhost:8080/ (not file:///)"
    ]
    
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")

def main():
    """Main diagnostic function"""
    print(f"\n{BOLD}{BLUE}{'*' * 70}{RESET}")
    print(f"{BOLD}{BLUE}EthioPrice Dashboard - 404 Error Diagnostic Tool{RESET}")
    print(f"{BOLD}{BLUE}{'*' * 70}{RESET}\n")
    
    # Run checks
    python_ok = check_python_version()
    dir_ok, web_dir = check_web_directory()
    
    if not python_ok or not dir_ok:
        print_error("\nCritical issues found. Fix the above problems and try again.")
        return
    
    perms_ok = check_file_permissions(web_dir)
    
    check_port_availability()
    provide_launch_commands(web_dir)
    
    # Optional: Test server
    test_http_server(web_dir)
    
    provide_troubleshooting_tips()
    
    # Summary
    print_header("Summary")
    
    if python_ok and dir_ok and perms_ok:
        print_success("All checks passed! Your setup looks good.")
        print_info("Follow the launch commands above to start the server.")
    else:
        print_error("Some checks failed. Review the output above.")
    
    print(f"\n{BOLD}For detailed help, see:{RESET}")
    print(f"  - web/LAUNCH_INSTRUCTIONS.md")
    print(f"  - web/SERVER_TROUBLESHOOTING.md")
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDiagnostic cancelled by user.")
    except Exception as e:
        print_error(f"\nUnexpected error: {str(e)}")
        import traceback
        traceback.print_exc()


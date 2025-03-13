# OS-Copilot for Windows

This document provides detailed instructions for installing and running OS-Copilot on Windows.

## Prerequisites

- Windows 10 or later
- Python 3.10 or later
- PowerShell (included by default in Windows 10 and later)

## Installation

### Option 1: Automated Installation (Recommended)

1. Clone the repository:
   ```
   git clone https://github.com/OS-Copilot/OS-Copilot.git
   cd OS-Copilot
   ```

2. Run the Windows compatibility checker:
   ```
   python windows_compatibility.py
   ```
   This script will:
   - Check your Python environment
   - Fix dependency issues
   - Check for path compatibility issues
   - Check for shell command compatibility issues
   - Check for OS-specific code issues
   - Fix NumPy import issues
   - Create a Windows-specific batch file to run the project

3. Apply the Windows-specific patches:
   ```
   python windows_patch.py
   ```
   This script will:
   - Patch OS-Copilot files for Windows compatibility
   - Create a PowerShell environment for Windows
   - Update import statements to include Windows-specific code
   - Create a Windows-specific batch file to run the project

4. Run OS-Copilot:
   ```
   run_windows.bat
   ```

### Option 2: Manual Installation

1. Clone the repository:
   ```
   git clone https://github.com/OS-Copilot/OS-Copilot.git
   cd OS-Copilot
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install numpy>=1.26.3
   pip install pydantic==1.10.8
   pip install langchain-core==0.0.13
   pip install langchain-community==0.0.1
   pip install langchain==0.0.349
   pip install langsmith==0.0.69
   pip install onnxruntime==1.17.0
   pip install pywin32==306
   pip install -e . --no-deps
   pip install -r requirements.txt --no-deps
   ```

4. Configure your OpenAI API key:
   ```
   copy .env_template .env
   ```
   Then edit the .env file to add your API key.

5. Run OS-Copilot:
   ```
   python quick_start.py
   ```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'numpy'**
   
   This error can occur if NumPy is not installed or not in the Python path. Try:
   ```
   pip install numpy>=1.26.3
   ```

2. **TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument: 'recursive_guard'**
   
   This error is related to Pydantic version compatibility. Fix it by installing Pydantic v1:
   ```
   pip install pydantic==1.10.8
   ```

3. **PowerShell Execution Policy**
   
   If you encounter issues with PowerShell scripts, you may need to change the execution policy:
   ```
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

4. **Path Issues**
   
   Windows uses backslashes (`\`) for paths, while Unix systems use forward slashes (`/`). If you encounter path-related errors, check if the code is using hardcoded Unix paths.

### Advanced Troubleshooting

If you continue to experience issues, try the following:

1. Run the Windows compatibility checker with verbose output:
   ```
   python windows_compatibility.py --verbose
   ```

2. Check the Python path:
   ```
   python -c "import sys; print(sys.path)"
   ```

3. Check if NumPy is installed and accessible:
   ```
   python -c "import numpy; print(numpy.__version__)"
   ```

4. Run with PYTHONPATH explicitly set:
   ```
   set PYTHONPATH=%CD%
   python quick_start.py
   ```

## Limitations

OS-Copilot was originally designed for Unix-like systems (macOS and Linux). While we've made efforts to make it compatible with Windows, some features may not work as expected. Specifically:

1. **AppleScript**: AppleScript is macOS-specific and has no Windows equivalent. We've added PowerShell as a Windows alternative, but some functionality may differ.

2. **Unix Commands**: Some Unix commands used in the codebase may not have direct Windows equivalents.

3. **File Paths**: Windows uses backslashes for file paths, while Unix systems use forward slashes. We've tried to make the code use OS-agnostic path handling, but some issues may remain.

## Contributing

If you encounter any Windows-specific issues or have suggestions for improving Windows compatibility, please open an issue or submit a pull request on GitHub. 
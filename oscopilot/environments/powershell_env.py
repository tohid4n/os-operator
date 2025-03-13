import os
import platform
import queue
import re
import subprocess
import threading
import time
import traceback
from oscopilot.environments import SubprocessEnv


class PowerShell(SubprocessEnv):
    """
    A class representing a PowerShell environment for executing PowerShell scripts on Windows.

    This class inherits from SubprocessEnv, which provides a general environment for executing code in subprocesses.
    """    
    file_extension = "ps1"
    name = "PowerShell"
    aliases = ["powershell", "ps1", "pwsh"]

    def __init__(
        self,
    ):
        """
        Initializes the PowerShell environment.

        Sets up the start command for executing PowerShell scripts.
        """        
        super().__init__()
        
        # Use PowerShell as the shell on Windows
        self.start_cmd = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass"]

    def preprocess_code(self, code):
        """
        Preprocesses the PowerShell script code before execution.

        Args:
            code (str): The PowerShell script code to preprocess.

        Returns:
            str: The preprocessed PowerShell script code.
        """        
        return preprocess_powershell(code)
        
    def line_postprocessor(self, line):
        """
        Processes a line of output from the PowerShell execution.

        Args:
            line (str): A line of output from the PowerShell execution.

        Returns:
            str: The processed line.
        """
        # Remove ANSI color codes
        line = re.sub(r'\x1b\[\d+m', '', line)
        return line

    def detect_active_line(self, line):
        """
        Detects the active line indicator in the output.

        Args:
            line (str): A line from the output.

        Returns:
            int: The line number indicated by the active line indicator, or None if not found.
        """
        if "##active_line" in line:
            return int(line.split("##active_line")[1].split("##")[0])
        return None

    def detect_end_of_execution(self, line):
        """
        Detects the end of execution marker in the output.

        Args:
            line (str): A line from the output.

        Returns:
            bool: True if the end of execution marker is found, False otherwise.
        """
        return "##end_of_execution##" in line


def preprocess_powershell(code):
    """
    Preprocesses PowerShell code for execution.

    Args:
        code (str): The PowerShell code to preprocess.

    Returns:
        str: The preprocessed PowerShell code.
    """
    # Add active line prints
    code = add_active_line_prints(code)
    
    # Add end of execution marker
    code += '\nWrite-Output "##end_of_execution##"'
    
    return code


def add_active_line_prints(code):
    """
    Adds Write-Output commands to indicate the active line of execution in the PowerShell script.

    Args:
        code (str): The PowerShell code to add active line indicators to.

    Returns:
        str: The modified PowerShell code with active line indicators.
    """
    lines = code.split("\n")
    modified_lines = []
    
    for i, line in enumerate(lines):
        if line.strip() and not line.strip().startswith("#"):
            # Add a line to print the active line number before each non-empty, non-comment line
            modified_lines.append(f'Write-Output "##active_line{i+1}##"')
        modified_lines.append(line)
    
    return "\n".join(modified_lines)


def has_multiline_commands(script_text):
    """
    Checks if the PowerShell script contains multiline commands.

    Args:
        script_text (str): The PowerShell script text to check.

    Returns:
        bool: True if the script contains multiline commands, False otherwise.
    """
    # Check for backtick continuation character
    if "`" in script_text:
        return True
    
    # Check for multiline blocks (if, for, etc.)
    if re.search(r'(if|for|foreach|while|switch|function|do)\s*\(', script_text, re.IGNORECASE):
        return True
    
    return False 
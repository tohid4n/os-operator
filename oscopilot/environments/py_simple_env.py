import os
import sys
import platform
import subprocess
import tempfile
from oscopilot.environments import BaseEnv

class PythonSimpleEnv(BaseEnv):
    """
    A simplified Python environment that doesn't require Jupyter.
    This is a fallback for Windows when zmq is not available.
    """
    file_extension = "py"
    name = "Python"
    aliases = ["python", "py"]
    
    def __init__(self):
        super().__init__()
    
    def step(self, code):
        """
        Execute Python code directly using subprocess.
        
        Args:
            code (str): The Python code to execute.
            
        Yields:
            dict: Output in the format {"type": "console", "format": "output", "content": output}
        """
        # Create a temporary file to store the code
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w', encoding='utf-8') as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Execute the code
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True
            )
            
            # Yield the output
            if result.stdout:
                yield {"type": "console", "format": "output", "content": result.stdout}
            
            # Yield the error, if any
            if result.stderr:
                yield {"type": "console", "format": "error", "content": result.stderr}
                
        except Exception as e:
            # Yield the exception
            yield {"type": "console", "format": "error", "content": str(e)}
        
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_file)
            except:
                pass
    
    def stop(self):
        """Stop execution (no-op for this simple environment)"""
        pass
    
    def terminate(self):
        """Terminate the environment (no-op for this simple environment)"""
        pass

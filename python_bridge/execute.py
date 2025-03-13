import sys
import os
import json
import subprocess
import importlib.util
import traceback

def run_command(cmd):
    """
    Execute a Python command and return the result as JSON.
    This function is designed to be called from the Electron app.
    """
    try:
        # First try to evaluate the command as an expression
        try:
            # Create a safe globals dictionary with limited builtins
            safe_globals = {
                '__builtins__': {
                    'print': print,
                    'str': str,
                    'int': int,
                    'float': float,
                    'bool': bool,
                    'list': list,
                    'dict': dict,
                    'tuple': tuple,
                    'set': set,
                    'len': len,
                    'range': range,
                    'enumerate': enumerate,
                    'zip': zip,
                    'min': min,
                    'max': max,
                    'sum': sum,
                    'sorted': sorted,
                    'round': round,
                    'abs': abs,
                    'all': all,
                    'any': any,
                    'isinstance': isinstance,
                    'issubclass': issubclass,
                    'hasattr': hasattr,
                    'getattr': getattr,
                    'setattr': setattr,
                    'delattr': delattr,
                    'dir': dir,
                    'vars': vars,
                    'type': type,
                    'id': id,
                    'hash': hash,
                    'repr': repr,
                    'chr': chr,
                    'ord': ord,
                    'hex': hex,
                    'oct': oct,
                    'bin': bin,
                    'pow': pow,
                    'divmod': divmod,
                    'complex': complex,
                    'bytes': bytes,
                    'bytearray': bytearray,
                    'memoryview': memoryview,
                    'slice': slice,
                    'iter': iter,
                    'next': next,
                    'reversed': reversed,
                    'map': map,
                    'filter': filter,
                    'format': format,
                    'frozenset': frozenset,
                    'property': property,
                    'classmethod': classmethod,
                    'staticmethod': staticmethod,
                    'super': super,
                    'object': object,
                    'open': open,
                    'Exception': Exception,
                    'BaseException': BaseException,
                    'ValueError': ValueError,
                    'TypeError': TypeError,
                    'IndexError': IndexError,
                    'KeyError': KeyError,
                    'AttributeError': AttributeError,
                    'NameError': NameError,
                    'ImportError': ImportError,
                    'SyntaxError': SyntaxError,
                    'RuntimeError': RuntimeError,
                    'StopIteration': StopIteration,
                    'FileNotFoundError': FileNotFoundError,
                    'PermissionError': PermissionError,
                    'OSError': OSError,
                    'IOError': IOError,
                    'ZeroDivisionError': ZeroDivisionError,
                    'OverflowError': OverflowError,
                    'FloatingPointError': FloatingPointError,
                    'ArithmeticError': ArithmeticError,
                    'AssertionError': AssertionError,
                    'BufferError': BufferError,
                    'EOFError': EOFError,
                    'LookupError': LookupError,
                    'MemoryError': MemoryError,
                    'NotImplementedError': NotImplementedError,
                    'RecursionError': RecursionError,
                    'ReferenceError': ReferenceError,
                    'SystemError': SystemError,
                    'SystemExit': SystemExit,
                    'UnicodeError': UnicodeError,
                    'UnicodeEncodeError': UnicodeEncodeError,
                    'UnicodeDecodeError': UnicodeDecodeError,
                    'UnicodeTranslateError': UnicodeTranslateError,
                    'Warning': Warning,
                    'DeprecationWarning': DeprecationWarning,
                    'PendingDeprecationWarning': PendingDeprecationWarning,
                    'RuntimeWarning': RuntimeWarning,
                    'SyntaxWarning': SyntaxWarning,
                    'UserWarning': UserWarning,
                    'FutureWarning': FutureWarning,
                    'ImportWarning': ImportWarning,
                    'UnicodeWarning': UnicodeWarning,
                    'BytesWarning': BytesWarning,
                    'ResourceWarning': ResourceWarning,
                }
            }
            
            # Add os module for system operations
            safe_globals['os'] = os
            
            # Add sys module for system operations
            safe_globals['sys'] = sys
            
            # Add subprocess module for executing commands
            safe_globals['subprocess'] = subprocess
            
            # Add json module for JSON operations
            safe_globals['json'] = json
            
            # Try to import oscopilot
            try:
                import oscopilot
                safe_globals['oscopilot'] = oscopilot
            except ImportError:
                pass
                
            # Execute the command
            result = eval(cmd, safe_globals)
            return json.dumps({"success": True, "result": str(result)})
        except SyntaxError:
            # If it's not a valid expression, try executing it as a statement
            # Create a temporary file with the command
            with open("temp_cmd.py", "w") as f:
                f.write(cmd)
            
            # Execute the file
            output = subprocess.check_output(["python", "temp_cmd.py"], stderr=subprocess.STDOUT)
            os.remove("temp_cmd.py")
            
            return json.dumps({"success": True, "result": output.decode('utf-8')})
    except Exception as e:
        error_traceback = traceback.format_exc()
        return json.dumps({
            "success": False, 
            "error": str(e),
            "traceback": error_traceback
        })

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(run_command(sys.argv[1]))
    else:
        print(json.dumps({"success": False, "error": "No command provided"})) 
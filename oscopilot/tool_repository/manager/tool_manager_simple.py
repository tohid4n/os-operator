import os
import json
import glob
import shutil
from typing import List, Dict, Any, Optional

# Constants
EMBED_MODEL_TYPE = "OpenAI"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_ORGANIZATION = os.environ.get("OPENAI_ORGANIZATION", "")
EMBED_MODEL_NAME = os.environ.get("EMBED_MODEL_NAME", "text-embedding-ada-002")

class ToolManager:
    """A simplified version of the ToolManager that doesn't rely on langchain."""
    
    def __init__(self, generated_tool_repo_dir=None):
        """Initialize the ToolManager."""
        # generated_tools: Store the mapping relationship between descriptions and tools (associated through task names)
        self.generated_tools = {}
        
        # Set the path to the generated tool repository
        if generated_tool_repo_dir is None:
            # Use the default path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.generated_tool_repo_dir = os.path.join(current_dir, "../../../generated_tool_repo")
        else:
            self.generated_tool_repo_dir = generated_tool_repo_dir
        
        # Create the necessary directories
        os.makedirs(self.generated_tool_repo_dir, exist_ok=True)
        os.makedirs(os.path.join(self.generated_tool_repo_dir, "tool_code"), exist_ok=True)
        os.makedirs(os.path.join(self.generated_tool_repo_dir, "tool_description"), exist_ok=True)
        
        # Load existing tools
        self._load_existing_tools()
    
    def _load_existing_tools(self):
        """Load existing tools from the generated tool repository."""
        # Get all tool description files
        description_files = glob.glob(os.path.join(self.generated_tool_repo_dir, "tool_description", "*.txt"))
        
        # Load each tool
        for desc_file in description_files:
            tool_name = os.path.basename(desc_file).replace(".txt", "")
            code_file = os.path.join(self.generated_tool_repo_dir, "tool_code", f"{tool_name}.py")
            
            if os.path.exists(code_file):
                # Load the description
                with open(desc_file, "r", encoding="utf-8") as f:
                    description = f.read()
                
                # Load the code
                with open(code_file, "r", encoding="utf-8") as f:
                    code = f.read()
                
                # Add the tool to the generated_tools dictionary
                self.generated_tools[tool_name] = {
                    "description": description,
                    "code": code
                }
    
    @property
    def programs(self) -> Dict[str, str]:
        """Get all tool programs."""
        return {name: info["code"] for name, info in self.generated_tools.items()}
    
    @property
    def descriptions(self) -> Dict[str, str]:
        """Get all tool descriptions."""
        return {name: info["description"] for name, info in self.generated_tools.items()}
    
    @property
    def tool_names(self) -> List[str]:
        """Get all tool names."""
        return list(self.generated_tools.keys())
    
    def get_tool_code(self, tool_name: str) -> Optional[str]:
        """Get the code for a specific tool."""
        if tool_name in self.generated_tools:
            return self.generated_tools[tool_name]["code"]
        return None
    
    def add_new_tool(self, info: Dict[str, Any]) -> bool:
        """Add a new tool to the repository."""
        tool_name = info.get("name")
        tool_description = info.get("description")
        tool_code = info.get("code")
        
        if not tool_name or not tool_description or not tool_code:
            print(f"Error: Missing required information for tool {tool_name}")
            return False
        
        # Check if the tool already exists
        if tool_name in self.generated_tools:
            print(f"Error: Tool {tool_name} already exists")
            return False
        
        # Save the tool description
        desc_file = os.path.join(self.generated_tool_repo_dir, "tool_description", f"{tool_name}.txt")
        with open(desc_file, "w", encoding="utf-8") as f:
            f.write(tool_description)
        
        # Save the tool code
        code_file = os.path.join(self.generated_tool_repo_dir, "tool_code", f"{tool_name}.py")
        with open(code_file, "w", encoding="utf-8") as f:
            f.write(tool_code)
        
        # Add the tool to the generated_tools dictionary
        self.generated_tools[tool_name] = {
            "description": tool_description,
            "code": tool_code
        }
        
        print(f"Added new tool: {tool_name}")
        return True
    
    def exist_tool(self, tool: str) -> bool:
        """Check if a tool exists."""
        return tool in self.generated_tools
    
    def retrieve_tool_name(self, query: str, k: int = 10) -> List[str]:
        """Retrieve tool names based on a query."""
        # Simple implementation: return all tool names
        # In a real implementation, this would use embeddings to find the most relevant tools
        return self.tool_names[:k]
    
    def retrieve_tool_description(self, tool_name: str) -> Optional[str]:
        """Retrieve the description for a specific tool."""
        # Handle case where tool_name is a list
        if isinstance(tool_name, list):
            # If it's a list, get the first item
            if tool_name:
                tool_name = tool_name[0]
            else:
                return None
        
        if tool_name in self.generated_tools:
            return self.generated_tools[tool_name]["description"]
        return None
    
    def retrieve_tool_code(self, tool_name: str) -> Optional[str]:
        """Retrieve the code for a specific tool."""
        # Handle case where tool_name is a list
        if isinstance(tool_name, list):
            # If it's a list, get the first item
            if tool_name:
                tool_name = tool_name[0]
            else:
                return None
        
        return self.get_tool_code(tool_name)
    
    def delete_tool(self, tool: str) -> bool:
        """Delete a tool from the repository."""
        if not self.exist_tool(tool):
            print(f"Error: Tool {tool} does not exist")
            return False
        
        # Remove the tool description file
        desc_file = os.path.join(self.generated_tool_repo_dir, "tool_description", f"{tool}.txt")
        if os.path.exists(desc_file):
            os.remove(desc_file)
        
        # Remove the tool code file
        code_file = os.path.join(self.generated_tool_repo_dir, "tool_code", f"{tool}.py")
        if os.path.exists(code_file):
            os.remove(code_file)
        
        # Remove the tool from the generated_tools dictionary
        del self.generated_tools[tool]
        
        print(f"Deleted tool: {tool}")
        return True

def print_error_and_exit(message: str) -> None:
    """Print an error message and exit."""
    print(f"Error: {message}")
    exit(1)

def add_tool(toolManager: ToolManager, tool_name: str, tool_path: str) -> None:
    """Add a tool to the repository."""
    if not os.path.exists(tool_path):
        print_error_and_exit(f"Tool file {tool_path} does not exist")
    
    # Read the tool file
    with open(tool_path, "r", encoding="utf-8") as f:
        tool_code = f.read()
    
    # Extract the tool description from the docstring
    tool_description = ""
    lines = tool_code.split("\n")
    for i, line in enumerate(lines):
        if '"""' in line or "'''" in line:
            start_idx = i
            for j in range(i + 1, len(lines)):
                if '"""' in lines[j] or "'''" in lines[j]:
                    end_idx = j
                    tool_description = "\n".join(lines[start_idx + 1:end_idx])
                    break
            break
    
    if not tool_description:
        print_error_and_exit(f"Could not extract description from {tool_path}")
    
    # Add the tool to the repository
    info = {
        "name": tool_name,
        "description": tool_description,
        "code": tool_code
    }
    
    if not toolManager.add_new_tool(info):
        print_error_and_exit(f"Failed to add tool {tool_name}")

def delete_tool(toolManager: ToolManager, tool_name: str) -> None:
    """Delete a tool from the repository."""
    if not toolManager.delete_tool(tool_name):
        print_error_and_exit(f"Failed to delete tool {tool_name}")

def get_open_api_doc_path() -> str:
    """Get the path to the OpenAPI documentation."""
    # Use absolute path instead of relative path
    return os.path.join(os.getcwd(), "open_api_docs")

def get_open_api_description_pair() -> Dict[str, str]:
    """Get the OpenAPI description pairs."""
    open_api_doc_path = get_open_api_doc_path()
    if not os.path.exists(open_api_doc_path):
        return {}
    
    result = {}
    for file_path in glob.glob(os.path.join(open_api_doc_path, "*.json")):
        file_name = os.path.basename(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if "info" in data and "description" in data["info"]:
                    result[file_name] = data["info"]["description"]
            except json.JSONDecodeError:
                print(f"Error: Could not parse {file_path} as JSON")
    
    return result

def main() -> None:
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Tool Manager")
    parser.add_argument("--add", help="Add a tool to the repository")
    parser.add_argument("--delete", help="Delete a tool from the repository")
    parser.add_argument("--path", help="Path to the tool file")
    
    args = parser.parse_args()
    
    toolManager = ToolManager()
    
    if args.add and args.path:
        add_tool(toolManager, args.add, args.path)
    elif args.delete:
        delete_tool(toolManager, args.delete)
    else:
        print("Available tools:")
        for tool_name in toolManager.tool_names:
            print(f"- {tool_name}")

if __name__ == "__main__":
    main() 
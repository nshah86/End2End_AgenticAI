"""
Environment variable loader utility.
"""
import os
from dotenv import load_dotenv
from pathlib import Path

def load_env_variables(env_file=None):
    """
    Load environment variables from .env file.
    
    Args:
        env_file: Path to the .env file. If None, will look for .env in the project root.
        
    Returns:
        bool: True if successfully loaded, False otherwise.
    """
    try:
        # If no env_file is specified, try to find .env in the project root
        if env_file is None:
            # Get the project root directory (3 levels up from this file)
            project_root = Path(__file__).parent.parent.parent.parent.absolute()
            env_file = project_root / '.env'
        
        # Load the .env file
        load_dotenv(dotenv_path=env_file)
        return True
    except Exception as e:
        print(f"Error loading environment variables: {e}")
        return False

def get_env_var(var_name, default=None):
    """
    Get an environment variable, with an optional default value.
    
    Args:
        var_name: Name of the environment variable.
        default: Default value if the variable is not set.
        
    Returns:
        The value of the environment variable, or the default value.
    """
    return os.environ.get(var_name, default) 
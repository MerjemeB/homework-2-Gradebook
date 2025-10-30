
import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

def load_data(file_path: str = "data/gradebook.json") -> Dict[str, Any]:
    """
    Load gradebook data from JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dictionary containing gradebook data
    """
    try:
        path = Path(file_path)
        if not path.exists():
            logger.info(f"Data file {file_path} not found, starting with empty data")
            return {"students": [], "courses": [], "enrollments": []}
        
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logger.info(f"Successfully loaded data from {file_path}")
            return data
            
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        print(f"Error: The data file {file_path} contains invalid JSON. Starting with empty data.")
        return {"students": [], "courses": [], "enrollments": []}
    except Exception as e:
        logger.error(f"Unexpected error loading {file_path}: {e}")
        print(f"Error loading data: {e}. Starting with empty data.")
        return {"students": [], "courses": [], "enrollments": []}


def save_data(data: Dict[str, Any], file_path: str = "data/gradebook.json") -> bool:
    """
    Save gradebook data to JSON file.
    
    Args:
        data: Gradebook data to save
        file_path: Path to the JSON file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
            logger.info(f"Successfully saved data to {file_path}")
            return True
            
    except Exception as e:
        logger.error(f"Error saving data to {file_path}: {e}")
        print(f"Error saving data: {e}")
        return False


def setup_logging():
    """Setup logging configuration."""
    log_path = Path("logs/app.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
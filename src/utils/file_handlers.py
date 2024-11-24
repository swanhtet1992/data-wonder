"""File handling utilities."""
import pandas as pd
from pathlib import Path
from typing import Union, Dict, Any
from datetime import datetime
import chardet
import json

def detect_encoding(file_content: bytes) -> str:
    """Detect the encoding of file content."""
    result = chardet.detect(file_content)
    return result['encoding'] or 'utf-8'

def load_file(file: Union[str, Path]) -> Union[pd.DataFrame, str]:
    """Load a file into appropriate format."""
    try:
        if isinstance(file, str):
            file_path = Path(file)
        else:
            file_path = Path(file.name)
            file_content = file.read()
            
            if file_path.suffix.lower() in ['.txt', '.md', '.rst']:
                encoding = detect_encoding(file_content)
                return file_content.decode(encoding)
            
            # Reset file pointer for pandas
            file.seek(0)
        
        # Handle different file types
        if file_path.suffix.lower() in ['.txt', '.md', '.rst']:
            with open(file_path, 'rb') as f:
                content = f.read()
                encoding = detect_encoding(content)
                return content.decode(encoding)
        elif file_path.suffix.lower() == '.csv':
            return pd.read_csv(file)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
            
    except Exception as e:
        raise ValueError(f"Error loading file: {str(e)}")

def save_processed_data(data: Dict[str, Any], filename: str) -> Path:
    """Save processed document data."""
    output_dir = Path("processed_documents")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = output_dir / f"{filename}_{timestamp}.json"
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    return file_path
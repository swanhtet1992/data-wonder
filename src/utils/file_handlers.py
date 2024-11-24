"""File handling utilities."""
import pandas as pd
from pathlib import Path
from typing import Union
from datetime import datetime
from ..config import OUTPUT_DIR

def load_file(file: Union[str, Path]) -> pd.DataFrame:
    """Load a file into a pandas DataFrame."""
    try:
        if isinstance(file, str):
            file_path = Path(file)
            if file_path.suffix == '.csv':
                return pd.read_csv(file_path)
            elif file_path.suffix == '.txt':
                return pd.read_csv(file_path, sep='\t')
        else:
            try:
                return pd.read_csv(file)
            except:
                return pd.read_csv(file, sep='\t')
    except Exception as e:
        raise ValueError(f"Error loading file: {str(e)}")

def save_dataset(data: pd.DataFrame, filename: str) -> Path:
    """Save a dataset to a file."""
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = output_dir / f"{filename}_{timestamp}.csv"
    data.to_csv(file_path, index=False)
    return file_path 
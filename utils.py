import pandas as pd
from pathlib import Path
from typing import Union
import streamlit as st

def load_file(file: Union[str, Path]) -> pd.DataFrame:
    """
    Load a file into a pandas DataFrame.
    
    Args:
        file: Path to the file or uploaded file object
        
    Returns:
        pd.DataFrame: Loaded data
        
    Raises:
        ValueError: If file format is not supported
    """
    if isinstance(file, str):
        file_path = Path(file)
        if file_path.suffix == '.csv':
            return pd.read_csv(file_path)
        elif file_path.suffix == '.txt':
            return pd.read_csv(file_path, sep='\t')
    else:
        # Handle uploaded file
        try:
            return pd.read_csv(file)
        except:
            return pd.read_csv(file, sep='\t')
    
    raise ValueError("Unsupported file format")

def save_dataset(data: pd.DataFrame, filename: str) -> Path:
    """
    Save a dataset to a file.
    
    Args:
        data: DataFrame to save
        filename: Name of the file to save to
        
    Returns:
        Path: Path to the saved file
    """
    output_dir = Path("generated_datasets")
    output_dir.mkdir(exist_ok=True)
    
    file_path = output_dir / filename
    data.to_csv(file_path, index=False)
    return file_path 
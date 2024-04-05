import re
import numpy as np
import pandas as pd
from typing import Dict, List

def transform_title(text: str) -> List[str]:
    """Dive a string based on character '-'.

    :param text: Text to be divided.
    :type text: str
    :return: Return a list of elements separated by character.
    :rtype: List[String]
    """
    new_text = text.strip()
    if "-" in text:
        new_text = text.split("-")[0]
    return new_text


def check_nan_columns(df: pd.DataFrame) -> Dict[str, int]:
    """Check data frame for nan columns.

    :param df: Pandas data frame to be checked.
    :type df: pd.DataFrame
    :return: Dictionary with empty columns as keys and number of empty values as values.
    :rtype: Dict[str, int]
    """
    empty_cols = {}
    for col in df.columns:
        num_empty = sum(df[col].isna())
        if num_empty > 0:
            empty_cols[col] = num_empty
    return empty_cols

def extract_nutritional_numerical(raw_text:str, pattern=r'(\d+\.?\d*)') -> float:
    """Extracts the numerical value from the raw text.
    
    :param raw_text: The raw text to extract the numerical value from.
    :type raw_text: str
    :param pattern:  The regular expression pattern to extract the numerical value, defaults to r'(\d+\.?\d*)'
    :type pattern: regexp, optional
    :return: The numerical value extracted from the raw text.
    :rtype: float
    """
    match = re.search(pattern, raw_text)
    if match:
        return float(match.group(1))
    else:
        return np.nan
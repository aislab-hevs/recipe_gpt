import re
import numpy as np
import pandas as pd
from typing import Dict, List
import glob
import json
import string

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
    
def remove_punctuation(text: str,punct_list: List[str]) -> str:
    """Remove the puntuation marks in a given text.

    :param text: Text to be modified. 
    :type text: str
    :param punct_list: List of characters to remove from the text.
    :type punct_list: List[str]
    :return: Modified text with characters in punt_list.
    :rtype: str
    """
    for punc in punct_list:
        if punc in text:
            text = text.replace(punc, '')
    return text.strip()

def get_files(file_pattern: str):
    list_files = glob.glob(file_pattern)
    filtered_files = [f for f in list_files if 'failed' not in f]
    print(f"Found files number: {len(filtered_files)}")
    return filtered_files

def load_files(list_files:List[str]) -> Dict[str, str]:
    answer_dict = {}
    for f in list_files:
        with open(f) as json_file:
            data = json.load(json_file)
        for values in data.values():
            answer_dict.update(values)
    return answer_dict

def replace_by_key(text: str, replace_dict: Dict[str, List[str]]) -> str:
    # preprocess text 
    lower_text = text.lower()
    # remove punctuation 
    lower_text = remove_punctuation(lower_text, list(string.punctuation)+['\n'])
    # splitter text 
    splitted = lower_text.split(' ')
    word_list = []
    for word in splitted:
        if word in replace_dict.keys():
            word_list.append(word)
        for key in replace_dict.keys():
            if word in replace_dict[key]:
                word_list.append(key)
    if len(word_list) == 0:
        return 'none'
    return ', '.join(set(word_list))


def check_pattern(text: str, pattern: str)-> bool:
    return re.search(pattern, text) is not None
    
def remove_pattern(text:str, pattern: str)->str:
    answer = re.sub(pattern, '', text)
    return answer.strip()
    
def extract_pattern(text: str, pattern: str)->str:
    match = re.search(pattern, text)
    #print(f'match {match}')
    if match is not None:
        return match.group(1)
    else:
        return text
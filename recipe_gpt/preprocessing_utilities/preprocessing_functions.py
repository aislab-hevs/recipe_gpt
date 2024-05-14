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

def get_files(file_pattern: str) -> List[str]:
    """Get the list of files that match the given pattern. 

    :param file_pattern: file pattern to search. 
    :type file_pattern: str
    :return: List of files that match the given pattern. 
    :rtype: List[str]
    """
    list_files = glob.glob(file_pattern)
    filtered_files = [f for f in list_files if 'failed' not in f]
    print(f"Found files number: {len(filtered_files)}")
    return filtered_files

def load_files(list_files:List[str]) -> Dict[str, str]:
    """Load raw files json into dictionary. 

    :param list_files: List of files path to load.
    :type list_files: List[str]
    :return: Dictionary 
    :rtype: Dict[str, str]
    """
    answer_dict = {}
    for f in list_files:
        with open(f) as json_file:
            data = json.load(json_file)
        for values in data.values():
            answer_dict.update(values)
    return answer_dict

def replace_by_key(text: str, replace_dict: Dict[str, List[str]]) -> str:
    """Replace words  in text using key-value pairs in replace_dict. 

    :param text: Text to be processed. 
    :type text: str
    :param replace_dict: Dictionary with words to be replaced.
    :type replace_dict: Dict[str, List[str]]
    :return: Processed text with words replaced. 
    :rtype: str
    """
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
    """Check if the string text matches the given pattern.

    :param text: Text to be checked. 
    :type text: str
    :param pattern: Pattern to check.
    :type pattern: str
    :return: Boolean value. True if the string matches the given pattern
    :rtype: bool
    """
    return re.search(pattern, text) is not None
    
def remove_pattern(text:str, pattern: str)->str:
    """Remove a pattern from text string.

    :param text: Text string to remove pattern form. 
    :type text: str
    :param pattern: Regular expression pattern to remove from text string. 
    :type pattern: str
    :return: Text without the pattern. 
    :rtype: str
    """
    answer = re.sub(pattern, '', text)
    return answer.strip()
    
def extract_pattern(text: str, pattern: str)->str:
    """Extracts a pattern from a text string.

    :param text: String to extract pattern from. 
    :type text: str
    :param pattern: Regular expression to extract pattern from text.
    :type pattern: str
    :return: Extracted pattern. 
    :rtype: str
    """
    match = re.search(pattern, text)
    #print(f'match {match}')
    if match is not None:
        return match.group(1)
    else:
        return text
    
def process_price(text: str) -> float:
    """Process text with price information. 

    :param text: text to process
    :type text: str
    :return: Price number or NaN if text is not a valid price.
    :rtype: float
    """
    if type(text) == float:
        return text
    else:
        # extract number 
        found_text = re.findall(r'\d+\.*\d*', text)
        if len(found_text) == 0:
            return np.nan
        # replace $ and,
        return float(found_text[0])
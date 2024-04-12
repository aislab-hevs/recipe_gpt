import pandas as pd
import numpy as np
from dotenv import load_dotenv
import datetime as dt
import os
import json
from typing import List
import argparse
from pathlib import Path
from default_queries import query_templates_dict
from gpt_utils.gpt_functions import GPTInteractionManager

def get_nutrition_plan(query: str, samples_to_generate: int, timeout: float=320.0, 
                       model: str = "gpt-3.5-turbo-1106", temperature: float = 0.8):
    # Load environment variables
    load_dotenv()
    # get api key from environment variable
    api_key = os.getenv("API_KEY")
    # create GPT handler object 
    gpt_handler = GPTInteractionManager(api_key=api_key, timeout=timeout)
    answers = gpt_handler.execute_query(text_query=query, 
                                        samples_to_generated=samples_to_generate,
                                        model=model,
                                        temperature=temperature)
    return answers

if __name__ == '__main__':
    # Create a parser object
    print("Starting...")
    # get additional data on recipes

    parser = argparse.ArgumentParser(
        description="Get diets and recipe suggestions.")
    
    query_template = query_templates_dict["nutrition_plan"]
    format = '%Y_%m_%d_%H_%M_%S'
    cwd_path = Path('.').parent
    target_path = os.path.join(cwd_path, 
                               f'output/raw_output/output_{dt.datetime.now().strftime(format)}.json')

    # Define command-line arguments
    parser.add_argument('-q', '--query', type=str, default='gpt-3.5-turbo-1106',
                        help='query to be executed in GPT chat')
    parser.add_argument('-c', '--choices', type=int, default=1,
                        help='Number of choices (different answers) to generate (default: 1)')
    parser.add_argument('-m', '--model', type=str, default='gpt-3.5-turbo-1106',
                        help='GPT model to query')
    parser.add_argument('-t', '--temperature', type=float, default=0.8,
                        help='Temperature parameter controls how much creative is. \
                            Value between 0 to 2, higher values imply more creative answers')
    parser.add_argument('-f', '--file_target', type=str, default=target_path,
                        help='Target file to save the answer.')
    
    # get data 
    args = parser.parse_args()
    
    query = args.query
    choices = args.choices
    model = args.model
    temperature = args.temperature
    file_target = args.file_target
    
    # process query 
    answer = get_nutrition_plan(query, 
                                samples_to_generate=choices, 
                                model=model, 
                                temperature=temperature)
    print(f'Answer: {answer}')
    
    with open(file_target, 'w', encoding='utf-8') as f: 
        json.dump(choices, f, ensure_ascii=False)
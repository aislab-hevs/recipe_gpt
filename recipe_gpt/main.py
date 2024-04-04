import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
import openai
import json
from typing import List
import argparse

from default_queries import query_templates_dict
from .gpt_utils.gpt_functions import GPTInteractionManager

def get_nutrition_plan():
    #TODO: Implement obtain information
    pass

if __name__ == '__main__':
    # Create a parser object
    print("Starting...")
    # get additional data on recipes

    parser = argparse.ArgumentParser(
        description="Enrich recipes with command-line arguments.")

    # Define command-line arguments
    parser.add_argument('--start_index', type=int, default=0,
                        help='Start index (default: 0)')
    parser.add_argument('--end_index', type=int, default=9000,
                        help='End index (default: 9000)')
    parser.add_argument('--chunk_size', type=int, default=500,
                        help='Chunk size (default: 500)')
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo-1106',
                        help='Model name (default: gpt-3.5-turbo-1106)')
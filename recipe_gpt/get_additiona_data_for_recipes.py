import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
import openai
import json
from typing import List
import argparse
from pathlib import Path

from default_queries import query_templates_dict
from gpt_utils.gpt_functions import GPTInteractionManager

def get_recipe_additional_information_from_dataframe(
    recipe_df: pd.DataFrame,
    title_colum: str,
    ingredients_col: str,
    target_file_name: str,
    type_query: str,
    model: str = "gpt-3.5-turbo-16k",
    max_recipes: int = -1,
    temperature: float = 0.8,
    timeout: float =220.0):
    """get additional data for a bunch of recipes. 

    :param recipe_df: Data frame with recipes title and ingredients to process.
    :type recipe_df: pd.DataFrame
    :param title_colum: Name of the title column in the data frame.
    :type title_colum: str
    :param ingredients_col: name of the ingredients column in the data frame.
    :type ingredients_col: str
    :param target_file_name: Path and name to store the outputs.
    :type target_file_name: str
    :param type_query: Type of data to obtain (e.g., carbs, fat, protein, etc).
    :type type_query: str
    :param model: OpenAI chat completion model to query, defaults to "gpt-3.5-turbo-16k"
    :type model: str, optional
    :param max_recipes: Maximum of recipes to process is used to try some recipes in test phases default -1 means process all recipes, defaults to -1
    :type max_recipes: int, optional
    :param temperature: Number between 0 and 2, higher values means more creative answers, defaults to 0.8
    :type temperature: float, optional
    :param timeout: Number of seconds passed before declare a time out default 120 seconds, defaults to 220.0
    :type timeout: float, optional
    :raises ValueError: Exception if query type is not in default query dictionary
    """
    # Load environment variables
    load_dotenv()
    # get api key from environment variable
    api_key = os.getenv("API_KEY")
    # create GPT handler object 
    gpt_handler = GPTInteractionManager(api_key=api_key, timeout=timeout)
    fail_recipes = []
    processed_recipes = {}
    sub_df = recipe_df.loc[:, [title_colum, ingredients_col]]
    print(f"sub shape: {sub_df.shape}")
    # choose the query template 
    if type_query in query_templates_dict.keys():
        query_template = query_templates_dict[type_query]
        print(f"Chosen query template: {type_query}")
    else:
        raise ValueError(f"{type_query} is not a valid query type")
    # Start processing the recipes dataset
    for i, idx in enumerate(sub_df.index):
        print(f"processing row {i} of {len(sub_df)}...")
        try:
            # make query
            recipe_title = sub_df.loc[idx, title_colum]
            ingredients = sub_df.loc[idx, ingredients_col]
            if max_recipes > 0 and i > max_recipes:
                break
            raw_response = gpt_handler.get_answers_for_batch_of_recipes(
                {f'{recipe_title}':
                 query_template.format(rec_title=recipe_title,
                                       ingredients_list=ingredients)},
                samples_to_generate=1,
                model=model,
                temperature=temperature
            )
            processed_recipes[recipe_title] = raw_response
        except Exception as e:
            print(f"Error during processing row{i}")
            print(f"error: {e}")
            fail_recipes.append(i)
            continue
    # save data
    with open(f"{target_file_name}.json", 'w', encoding='utf-8') as fp:
        json.dump(processed_recipes, fp, ensure_ascii=False)
    with open(f"{target_file_name}_failed.json", 'w') as fp:
        json.dump(fail_recipes, fp)

if __name__ == '__main__':
    # Create a parser object
    print("Starting...")
    # get additional data on recipes

    parser = argparse.ArgumentParser(
        description="Enrich recipes with command-line arguments.")

    # Define command-line arguments
    parser.add_argument("-s", "--source_file", 
                        type=Path, 
                        default=None,
                        help='Path to source csv file containing recipes')
    parser.add_argument("-d", "--delimiter",
                        type=str, 
                        default='|',
                        help='Delimiter in the csv source and target files (default:|)')
    parser.add_argument('--start_index', type=int, default=0,
                        help='Start index (default: 0)')
    parser.add_argument('--end_index', type=int, default=-1,
                        help='End index (default: -1)')
    parser.add_argument('--chunk_size', type=int, default=500,
                        help='Chunk size (default: 500)')
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo-1106',
                        help='Model name (default: gpt-3.5-turbo-1106)')
    parser.add_argument('--title_column', type=str, default='Title',
                        help='Title column name in the dataset')
    parser.add_argument('--ingredients_column', type=str, default='ingredients',
                        help='Ingredients column name in the dataset')
    parser.add_argument('--file_name', type=str, default='meal_type_new_recipes',
                        help='Target file name.')
    parser.add_argument('--query', type=str, default='',
                        help='Query to execute.')
    

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the parsed arguments
    start_index = args.start_index
    end_index = args.end_index
    chunk_size = args.chunk_size
    model = args.model
    title_col = args.title_column
    ingredients_col = args.ingredients_column
    target_file_name = args.file_name
    query_type = args.query
    source_file = args.source_file
    delimiter = args.delimiter

    data_loading = pd.read_csv(source_file,
                               sep=delimiter)
    print(f"size: {data_loading.shape}")
    if end_index == -1:
        end_index = data_loading.shape[0]
    # call the function
    for i in range(start_index, end_index, chunk_size):
        print(f"Processing batch: {i}... query: {query_type}")
        sub_df = data_loading.iloc[i:i+chunk_size, :]
        get_recipe_additional_information_from_dataframe(
            recipe_df=sub_df,
            title_colum=title_col,
            ingredients_col=ingredients_col,
            type_query=query_type,
            target_file_name=target_file_name+f"{i}_{i+chunk_size}",
            model=model)
    # # Define command-line arguments
    print("Finished")

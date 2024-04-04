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
from .gpt_utils.gpt_functions import GPTInteractionManager

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
    """_summary_

    :param recipe_df: _description_
    :type recipe_df: pd.DataFrame
    :param title_colum: _description_
    :type title_colum: str
    :param ingredients_col: _description_
    :type ingredients_col: str
    :param target_file_name: _description_
    :type target_file_name: str
    :param type_query: _description_
    :type type_query: str
    :param model: _description_, defaults to "gpt-3.5-turbo-16k"
    :type model: str, optional
    :param max_recipes: _description_, defaults to -1
    :type max_recipes: int, optional
    :param temperature: _description_, defaults to 0.8
    :type temperature: float, optional
    :param timeout: _description_, defaults to 220.0
    :type timeout: float, optional
    :raises ValueError: _description_
    """
    # Load environment variables
    load_dotenv()
    # get api key from environment variable
    api_key = os.getenv("API_KEY")
    # create GPT handler object 
    gpt_handler = GPTInteractionManager(api_key=api_key, model=model, timeout=timeout)
    # create a list of ingredients
    ingredients_list = recipe_df[ingredients_col].tolist()
    # create a list of titles
    title_list = recipe_df[title_colum].tolist()
    fail_recipes = []
    processed_recipes = {}
    sub_df = recipe_df.loc[:, [title_colum, ingredients_col]]
    # choose the query template 
    if type_query in query_templates_dict.keys():
        query_template = query_templates_dict[type_query]
        print(f"Chosen query template: {type_query}")
    else:
        raise ValueError(f"{type_query} is not a valid query type")
    # Start processing the recipes dataset
    for i in range(len(sub_df)):
        print(f"processing row {i} of {len(sub_df)}...")
        try:
            # make query
            recipe_title = sub_df.loc[i, title_colum]
            ingredients = sub_df.loc[i, ingredients_col]
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
            processed_recipes[recipe_title] = dict(raw_response[recipe_title][0]["message"]["content"])
        except Exception as e:
            print(f"Error during processing row{i}")
            print(f"error: {e}")
            fail_recipes.append(i)
            continue
    # save data
    with open(f"{target_file_name}.json", 'w') as fp:
        json.dump(processed_recipes, fp)
    with open(f"{target_file_name}_failed.json", 'w') as fp:
        json.dump(fail_recipes, fp)
        
def get_nutrition_plan(target_file_name):
    #TODO: Implement obtain information
    pass

if __name__ == '__main__':
    # Create a parser object
    print("Starting...")
    # get additional data on recipes

    parser = argparse.ArgumentParser(
        description="Enrich recipes with command-line arguments.")

    # Define command-line arguments
    parser.add_argument("-s", "--source", 
                        type=Path, 
                        default=None,
                        help='Path to source csv file containing recipes')
    parser.add_argument('--start_index', type=int, default=0,
                        help='Start index (default: 0)')
    parser.add_argument('--end_index', type=int, default=9000,
                        help='End index (default: 9000)')
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

    data_loading = pd.read_csv("/home/victor/Documents/Expectation_data_generation/src/meals_collection/df_ingredients_187_to_fix.csv",
                               sep="|",
                               index_col=0)
    print(f"size: {data_loading.shape}")
    # call the function
    for i in range(start_index, end_index, chunk_size):
        print(f"Processing batch: {i}... query: {query_type}")
        sub_df = data_loading.iloc[i:i+chunk_size, :]
        get_recipe_additional_information_from_dataframe(
            recipe_df=sub_df,
            title_colum=title_col,
            ingredients_col=ingredients_col,
            type_query=query_type,
            file_name=target_file_name+f"{i}_{i+chunk_size}",
            model=model)
    # # Define command-line arguments
    print("Finished")

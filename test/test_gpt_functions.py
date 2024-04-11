import os 
import sys
import pytest
from dotenv import load_dotenv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  

from recipe_gpt.gpt_utils.gpt_functions import GPTInteractionManager

@pytest.fixture
def create_gpt_interaction():
    load_dotenv(dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env')))
    api_key = os.getenv("API_KEY")
    print(f"Api key loaded: {api_key}")
    assert api_key is not None, "Please set the OPENAI_API_KEY environment variable"
    return GPTInteractionManager(api_key=api_key)

def test_gpt_interaction_query(create_gpt_interaction):
    gpt_handler = create_gpt_interaction
    answer = gpt_handler.execute_query(
        text_query="Please give me the name of a recipe with cheese.",
        samples_to_generated=1,
        model="gpt-3.5-turbo",
        temperature=1.3
    )
    assert answer is not None
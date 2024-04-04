import openai
from typing import List, Union, Dict, Any
import httpx


class GPTInteractionManager(object):
    """_summary_

    :param object: _description_
    :type object: _type_
    """
    def __init__(self, 
                 api_key: str,
                 max_retries: int=0, 
                 timeout: Union[float, httpx.Timeout] = 120.0
                 ) -> None:
        """_summary_

        :param api_key: _description_
        :type api_key: str
        :param max_retries: _description_, defaults to 0
        :type max_retries: int, optional
        :param timeout: _description_, defaults to 120.0
        :type timeout: Union[float, httpx.Timeout], optional
        """
        self.api_key = api_key
        self.max_retries = max_retries
        self.timeout = timeout
        self.client = openai.OpenAI(
            api_key=self.api_key,
            max_retries=self.max_retries,
            timeout=self.timeout
        )
        
    def get_openai_model_list(self) -> List[Any]:
        """_summary_

        :return: _description_
        :rtype: List[Any]
        """
        models = openai.Model.list()
        return models
    
    def execute_query(self, 
                      text_query: str,
                      samples_to_generated: int = 10,
                      model: str = "gpt-3.5-turbo",
                      temperature: float = 0.6) -> List[Any]:
        """_summary_

        :param text_query: _description_
        :type text_query: str
        :param samples_to_generated: _description_, defaults to 10
        :type samples_to_generated: int, optional
        :param model: _description_, defaults to "gpt-3.5-turbo"
        :type model: str, optional
        :param temperature: _description_, defaults to 0.6
        :type temperature: float, optional
        :return: _description_
        :rtype: List[Any]
        """
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert chef that know many recipes and their nutritional values."
                },
                {
                    "role": "user", 
                    "content": text_query
                }
            ],
            model=model,
            n=samples_to_generated,
            temperature= temperature
        )
        return response
    
    def get_answers_for_batch_of_recipes(self, 
                                         recipes_data_dict: Dict[str, Any],
                                         samples_to_generate = 1,
                                         model: str = "gpt-3.5-turbo",
                                         temperature: float = 0.6) -> Dict[str, str]:
        """_summary_

        :param recipes_data_dict: _description_
        :type recipes_data_dict: Dict[str, Any]
        :param samples_to_generate: _description_, defaults to 1
        :type samples_to_generate: int, optional
        :param model: _description_, defaults to "gpt-3.5-turbo"
        :type model: str, optional
        :param temperature: _description_, defaults to 0.6
        :type temperature: float, optional
        :return: _description_
        :rtype: Dict[str, str]
        """
        # Process element by element
        answers = {}
        for recipe in recipes_data_dict.keys():
            try:
                print(f"Processing recipe: {recipe}")
                processed_query =  recipes_data_dict[recipe]
                response = self.execute_query(
                    processed_query,
                    samples_to_generated=samples_to_generate,
                    model=model,
                    temperature=temperature)
                answers[recipe] = response["choices"]
            except Exception as e:
                print(f"Exception: {e} for recipe: {recipe}")
                answers[recipe] = ""
                continue
        return answers
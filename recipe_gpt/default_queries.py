# This file stores teh default text templates queries used to extract recipe information. 

query_templates_dict = {
    "taste": """
        Indicate the key taste profile between sweet, bitter, salty, sour and umami, in the following recipe. Answer with only one word.

        {ingredients_list}
        """,
        "price": """
        Indicate from 1 to 3 (with 3 being expensive) the estimated cost of the following recipe.
        Answer only with one number, given the following ingredients:

        {ingredients_list}
        """,
        "ingredients": """
        Please give me the list of ingredients with quantities for 2 portions for
        the following recipes: 
        
        Recipe name: {rec_title}
        """,
        "prep_time": """
        Indicate the preparation time in minutes of the following recipe. Answer with only the estimate time 
        in minutes in one number:
        
        Recipe name: {rec_title}
        
        Ingredients: {ingredients_list}
        """,
        "cooking_style": """
        Indicate the cooking style (Sauteed, Slow-cooked, backed, fired, etc) of 
        the following recipe. Answer with only one word:
        Recipe name: {rec_title}

        Ingredients: {ingredients_list}
        """,
        "cuisine": """
        Indicate the cuisine type of 
        the following recipe with name: {rec_title} and ingredient 
        list: {ingredients_list}. Please answer with only one word.
      """,
      "carbs": """
        Please give me an estimation of the total carbohydrates for a 
        recipe with these ingredients and quantities, please answer only with 
        the total number: 

        {ingredients_list}
        """,
        "preparation": """
        Please give me the preparation or cooking instructions for the recipe entitled: 
        {rec_title}, and with the following ingredients:
        {ingredients_list}
        """,
        "calories": """
        Indicate the total estimate calories 
        from the following recipe given the ingredients and quantities bellow.  
        Answer with only one total number. 

        {ingredients_list}
        """,
        "fiber": """
        Please give me an estimation of the total fiber for a recipe with these 
        ingredients and quantities, please answer only with the total number: 

        {ingredients_list}
        """,
        "fat": """
        Please give me an estimation of the total fat for a recipe with these ingredients and quantities, 
        please answer only with the total number: 

        {ingredients_list}
        """,
        "protein": """
        Please give me an estimation of the total protein for a recipe with these ingredients and quantities, 
        please answer only with the total number: 

        {ingredients_list}
        """,
        "allergens": """
        Classify the following recipe in one of the following allergy categories: 
        Milk, Eggs, Fish (e.g., bass, flounder, cod), 
        Crustacean shellfish (e.g., crab, lobster, shrimp),
        Tree nuts (e.g., almonds, walnuts, pecans), Peanuts,
        Wheat, Soybeans, Sesame, None. Please answer with one word. 

        {ingredients_list}
        """,
        "cultural_restriction": """
        Classify the following recipe in one of the following categories:
        veggie, vegetarian, halal, kosher, meat-based, 
        grain-based, etc. Please answer with only one word.  
        Recipe title: {rec_title} with ingredients: {ingredients_list}
        """
}
# RecipeGPT

<!-- trunk-ignore(markdownlint/MD033) -->
<p align="center">
<img src="images/logo/logo.png" alt="logo_dexire" width="100"/>
</p>

<!--- These are examples. See https://shields.io for others or to customize this set of shields. You might want to include dependencies, project status and license info here --->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project aims to provide recipes querying chatGPT models.

## Prerequisites

Before you begin, ensure you have met the following requirements:

<!--- These are just example requirements. Add, duplicate or remove as required --->

- You have a `<Windows/Linux/Mac>` machine.
- You have installed version of `python 3.9` or create an environment with python 3.9 version.
- It is recommended to create an environment with conda or venv to isolate the execution and avoid libraries version conflict.
- You have an API_KEY for querying the GPT models through API calls.

## Installing RecipeGPT

To install RecipeGPT, follow these steps:

Linux and macOS:

```
python -m pip install --upgrade setuptools
```

Windows:

```
python -m pip install --upgrade setuptools
```

In the root directory RecipeGPT execute the following command with the active environment  activated:

```
pip install .
```

Or in the main folder with the environment activated  execute the following command in the terminal:

```
python setup.py install
```

## Installing with wheels

The package can be compile to a wheel fire and the easy installed. To build a wheel execute the following command in the terminal and localized in the RecipeGPT main folder:

For Unix/Linux/macOS build:

```
python3 -m pip install --upgrade build
python3 -m build
```

For Windows:

```
py -m pip install --upgrade build
py -m build
```

The wheel installer will be appear in the dist subdirectory. Localize in the dist subdirectory execute the following command:

```
pip install recipe_gpt-0.0.1-py3-none-any.whl
```

The wheel installer (.whl file) cna be distributed to install in other environments.

## Using recipeGPT recipes database

This repository provide a database with 7000 recipes in csv format to load and use them in your project please follow the instructions bellow:

1. The recipes file is located inside `output` folder located at the root repository directory and with the following relative path:

    ```bash
    output/final_recipes/df_recipes.csv
    ```

2. The database can be loaded using pandas or other csv related libraries. Given that the database contains multiline text in ingredients and preparations columns the separator character is `|` so should be used to correctly load the recipes. An example of loading this database in Pyhton using Pandas library is shown bellow:

   ```python
   import pandas as pd

   df_recipes = pd.read_csv(path_to_recipes_dataset, 
   sep='|', 
   index_col=0)
   ```

column 0 is a numerical index for that reason is passed as parameter to read_csv function.

### Dataset structure

The recipe dataset is conformed for the following columns described in table bellow: 

| Column name          | Description                                                                                                                                               | Data Type            |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|
| recipeId             | Unique recipe Id                                                                                                                                          | String               |
| name                 | Recipe name                                                                                                                                               | String               |
| ingredients          | List of ingredients with quantities.                                                                                                                      | Multiline-text       |
| ingredients_list     | List of ingredients without quantities.                                                                                                                   | Multiline-text       |
| instructions         | Instructions to prepare the recipes.                                                                                                                      | Multiline-text       |
| carbohydrates        | Carbohydrate content of the recipe in grams.                                                                                                              | Float                |
| fat                  | Fat content of the recipe in grams.                                                                                                                       | Float                |
| fiber                | Fiber content of the recipe in grams.                                                                                                                     | Float                |
| protein              | Protein content of the recipe in grams.                                                                                                                   | Float                |
| calories             | Calories content of the recipe in kilocalories (kcal).                                                                                                    | Float                |
| taste                | Main Taste profile for the given recipe between the 5 main profiles.                                                                                      | String categorical   |
| cooking_style        | Cooking style for the recipe (e.g., slow-cooking, roasted, etc.)                                                                                          | String categorical   |
| prep_time            | Estimated total preparation time in minutes.                                                                                                              | Float                |
| allergens            | Possible allergens on the recipe, considering the most common food allergens.                                                                             | String categorical   |
| cultural_restriction | Describe if the recipe is associated with a cultural or religious diet (e.g., Halal, Kosher, Vegan, Vegetarian).                                          | String categorical   |
| cuisine              | Describes the recipe cuisine type.                                                                                                                        | String categorical   |
| price                | This column describes the estimated cost of the recipe employing an integer value between 1 and 3 where 1 means cheap recipe to 3 which means expensive.  | Integer, categorical |
| raw_text             | The original text extracted from query to OpenAI's GPT models                                                                                             | Multiline-text       |
|     thumbnail                 |    URL with recipe thumbnail.  |     URL                 |


## Using RecipeGPT to complete recipe information

To query gpt models and complement recipe information such as nutritional values, cuisine type and  from terminal in the project root directory execute the following steps:

1. Set your OpenAI's API key in the .env.example file and renamed to '.env' filename.
2. In the root directory of this project in the terminal:
   
```bash
python recipe_gpt/get_additiona_data_for_recipes.py -s source_file_path 
```


## Contributing to RecipeGPT

<!--- If your README is long or you have some specific process or steps you want contributors to follow, consider creating a separate CONTRIBUTING.md file--->

To contribute to RecipeGPT, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contributors

Thanks to the following people who have contributed to this project:

- [@victorc365](https://github.com/victorc365) 📖

## Acknowledge  

TODO: set a papaer to cite maybe one on chatGPT

## Contact

If you want to contact me you can reach me at <victorc365@gmail.com>.

## License

<!--- If you're not sure which open license to use see https://choosealicense.com/--->

This project uses the following license: [MIT](https://opensource.org/license/mit).
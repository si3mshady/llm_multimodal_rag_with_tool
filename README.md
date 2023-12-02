Certainly! Below is a basic README for your `GetNutritionDetails` tool:

---

# GetNutritionDetails Tool

This tool is designed to fetch nutritional details, including ingredients and serving size, for a specified food item using the USDA API.

## Requirements

- Python 3
- `llama_index` library
- `requests` library
- `dotenv` library
- OpenAI API key
- USDA API key

## Installation

1. Install the required dependencies:

    ```bash
    pip install llama_index requests python-dotenv
    ```

2. Set up your environment variables:

    Create a `.env` file in your project directory and add the following:

    ```plaintext
    USDA_API_KEY=your_usda_api_key
    OPENAI_API_KEY=your_openai_api_key
    ```

3. Run the tool:

    ```bash
    python your_script_name.py
    ```

## Usage

Instantiate the `GetNutritionDetails` class and call the `resolve_food_item` method with the desired food item:

```python
from llama_index.tools.tool_spec.base import BaseToolSpec
from llama_index.agent import OpenAIAgent
import requests
from dotenv import load_dotenv
import os, json

load_dotenv()

USDA_API_KEY = os.getenv("USDA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class GetNutritionDetails(BaseToolSpec):
    def __init__(self):
        self.headers = { "Content-Type": "application/json"}
        self.data = {"query": None}
        self.USDA_URL = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key={API_KEY}"

    def resolve_food_item(self, food):
        '''
         Given a food item this function will query the USDA API database for the same and return a document that 
         contains ingredients, serving size and food nutrients 

         args:
           food: (string: the food item to query) 
        '''
        self.data["query"] = food

        response = requests.post(url=self.USDA_URL.format(API_KEY=USDA_API_KEY), headers=self.headers,  data=json.dumps(self.data))
        res = response.json()

        food_dictionary = {
            "ingredients": res.get('foods')[0]['ingredients'],
            "servingSize": res.get('foods')[0]['servingSize'],
        }

        return food_dictionary

# Create an OpenAIAgent with the GetNutritionDetails tool
agent = OpenAIAgent.from_tools(
    GetNutritionDetails().to_tool_list(),
    verbose=True,
)

# Example usage
res = agent.chat("Is pepperoni pizza healthy? Give me a list of ingredients and serving size.")
print(res)
```

## Contributing

Feel free to contribute to enhance the functionality or fix any issues. Create a pull request and we'll review it together!

---

Make sure to replace `"your_script_name.py"` with the actual name of your script. Feel free to add more sections based on your project's specific needs.
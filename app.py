from llama_index.tools.tool_spec.base import BaseToolSpec
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
        self.USDA_URL =  "https://api.nal.usda.gov/fdc/v1/foods/search?api_key={API_KEY}"
       
       
    spec_functions = ["resolve_food_item"]
    
    def resolve_food_item(self,food):
        '''
         Given a food item this function will query the USDA API database for the same and return a document that 
         contains ingredients, serving size and food nutritients 
         args:
           food: (string: the food item to query) 
        '''
        self.data["query"] = food

        response = requests.post(url=self.USDA_URL.format(API_KEY=USDA_API_KEY), headers=self.headers,  data=json.dumps(self.data))
        res=response.json()

        food_dictionary = {
            "ingredients": res.get('foods')[0]['ingredients'],
            "servingSize":  res.get('foods')[0]['servingSize'],
            "foodNutrients":  res.get('foods')[0]['foodNutrients']
        }
        print(food_dictionary)

        return food_dictionary


tool = GetNutritionDetails()

tool.resolve_food_item("burger")

#servingSize 
# ingredients
# foodNutrients


# dict_keys(['fdcId', 'description', 'dataType', 'gtinUpc', 'publishedDate', 'brandOwner', 'brandName', 'ingredients', 'marketCountry', 'foodCategor
# y', 'modifiedDate', 'dataSource', 'servingSizeUnit', 'servingSize', 'tradeChannels', 'allHighlightFields', 'score', 'microbes', 'foodNutrients', '
# finalFoodInputFoods', 'foodMeasures', 'foodAttributes', 'foodAttributeTypes', 'foodVersionIds'])




    




# https://api.data.gov/docs/developer-manual/
# https://fdc.nal.usda.gov/api-key-signup.html
#https://fdc.nal.usda.gov/api-guide.html
#search -> https://app.swaggerhub.com/apis/fdcnal/food-data_central_api/1.0.1#/FDC/postFoodsSearch


#/v1/foods/search
#first use the search api endpoint to get the ID's we need to search


#try to resolve the ids you get back from the food search 

#give food to openAI to synthesize data into speech 
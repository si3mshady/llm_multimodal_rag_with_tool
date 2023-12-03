import re
from llama_index.multi_modal_llms import ReplicateMultiModal
from llama_index.multi_modal_llms.replicate_multi_modal import (
    REPLICATE_MULTI_MODAL_LLM_MODELS,
)
from app import GetNutritionDetails
from llama_index.agent import OpenAIAgent
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from llama_index.schema import ImageDocument
from io import BytesIO
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_KEY

agent = OpenAIAgent.from_tools(
    GetNutritionDetails().to_tool_list(),
    verbose=True,
)

def main():
    image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], key="uploaded_image")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:   
        # Determine the source of the image (upload or camera)
        if image_file is not None:
            image_data = BytesIO(image_file.getvalue())

            if image_data:
                if not os.path.exists("images"):
                    os.makedirs("images")
                # Display the uploaded image at a standard width.
                st.session_state['assistant_avatar'] = image_data
                st.image(image_data, caption='Uploaded Image.', use_column_width=True)

                img = Image.open(BytesIO(image_file.getvalue()))
                img.save(f"images/food.jpg")
                image_document = ImageDocument(image_path=f"images/food.jpg")

                # prompt = st.text_input()
                prompt = "Describe in great detail this image"


                try:
                ## Initialize the MultiModal LLM model
                    if prompt is not None:
                    
                        multi_modal_llm = ReplicateMultiModal(
                            model=REPLICATE_MULTI_MODAL_LLM_MODELS["llava-13b"],
                            max_new_tokens=100,
                            temperature=0.1,
                            num_input_files=1,
                            top_p=0.9,
                            num_beams=1,
                            repetition_penalty=1,
                        )

                        mm_resp = multi_modal_llm.complete(
                            prompt=prompt,
                            image_documents=[image_document],
                        )
                        
                        template = f"If the text in angled brackets is contains food  <<{mm_resp}>> identify what the food item, reduce the food down to just one item as it needs to be passed as an argument  \
                        an input to the agent/tool.  Please provide a list of ingredients and serving size for that food item along with a  very detailed description. If ingredient or serving size inforamtion is not available just be descriptive explaining the image, do not apologize in your response. \
                        args: 
                            food item (string)."
                            
                        agent_response = str(agent.chat(template))
                        print(type(agent_response))

                        
                        st.write(str(re.split("Agent Response:", agent_response)[0]))

                except Exception as e:                
                    print("Inference Failed due to: ", e)
            
if __name__ == "__main__":
    main()

# This is the main app


#get the response back from model for image eval
#check if the response is food
#if food create a template that you will feed into prompt

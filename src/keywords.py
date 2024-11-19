from idna.idnadata import scripts
from openai import AzureOpenAI
import os

def extract_keywords(text):

    admin_key = os.environ.get("ADMIN_KEY")

    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint="https://visma-flyt-3-ai.openai.azure.com/",
        api_key=admin_key,
        api_version="2024-05-01-preview"  # Use the latest stable API version
    )


    prompt = f"""Extract the 3-5 most relevant keywords from the text enclosed by triple backticks. 
    Provide them as a Python list in Norwegian, with each keyword being a single word. 
    Ensure the keywords are pertinent to HR contexts such as recruitment, employee relations, benefits, etc. 
    Format your response as: ["keyword1", "keyword2", "keyword3"].
    Your response should ONLY include the list of keywords.

    Here is the text:

    ```{text}```
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user",
             "content": prompt
             }
        ],
        temperature=0.2)

    return response.choices[0].message.content
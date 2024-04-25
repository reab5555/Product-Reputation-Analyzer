import time
import pandas as pd
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
import google.generativeai as genai
from tqdm import tqdm


def get_cluster_analysis(modified_csv_path, google_project, n_critics):
    # Load and prepare data for the LLM
    df = pd.read_csv(modified_csv_path)
    df_criticisms = df['criticism']
    keyword = df.loc[0, 'keyword']
    keyword = keyword.capitalize()

    # Initialize the LLM
    #genai.configure(api_key=GOOGLE_API_KEY)
    task = f'Please summarize {n_critics} problems, issues, or any other type of criticism toward {keyword} out of the texts provided. no need to give introductions or any explanations. simply list the main {n_critics} problems, issues, or any other type of criticism toward {keyword} only as follows: summarize it as short as possible with one line, a limit of 50 words only and with two sentences maximum. furthermore, no need to mention all descriptions from the texts summaries, only the top descriptions that best describe it so there is no need to repeat things that mean the same thing. also, dont write or include a note or notes. the output must be written only in this format for example - issue/problem/criticism name or topic: summary. here is an example - 1. Battery problems: significant battery errors, battery is draining fast. 2. Stuck at first level: the game got stuck in level 1 and just freeze.'
    texts = f'Texts: {df_criticisms}'

    attempt = 0
    while attempt < 2:  # Allow for a second attempt if the first fails
        try:
            vertexai.init(project=google_project, location="us-central1")
            model = GenerativeModel("gemini-1.5-pro-preview-0409")
            responses = model.generate_content(
                [f"""{task}
            input: {texts}
            """],
                generation_config={
            "temperature": 1,
            "top_p": 1
            }
            )

            content = responses.text
            print(f'Main {keyword} critics:')
            print(content)
            return content

        except Exception as e:
            print(f"Error occurred: {e}")
            if attempt == 0:  # Only wait and retry if it's the first attempt
                print("Waiting 30 seconds before retrying...")
                time.sleep(30)
        attempt += 1
    return None


from os import environ as env
from dotenv import load_dotenv
from google import genai

def call_llm_api(prompt: str) -> str:
    load_dotenv()
    GEMINI_API_KEY = env.get("GEMINI_API_KEY")
    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=[prompt])
    return response.text

def make_requirements_of_paster_json(requirement_txt: str) -> str:
    # 1. import prompt template: prompt_requirements_paster_txt
    prompt_requirements_paster_txt = f"```txt\n{requirement_txt}\n```\n\n"
    with open("prompts/prompt_requirement_paster.txt", "r", encoding="utf-8") as file:
        prompt_requirements_paster_txt += file.read()

    # 2. call LLM API
    response = call_llm_api(prompt_requirements_paster_txt)

    # 3. save response to 'utils/json/res_requirements_paster.json'
    json_url = "utils/json/res_requirements_paster.json"
    with open(json_url, "w", encoding="utf-8") as file:
        file.write(response)
    return json_url

def organize_requirements_of_team_wakeup(requirements_txt: str) -> str:
    # 1. import prompt template: prompt_requirements_team_wakeup_txt
    prompt_requirements_team_wakeup_txt = f"```txt\n{requirements_txt}\n```\n\n"
    with open("prompts/prompt_requirement_team_wakeup.txt", "r", encoding="utf-8") as file:
        prompt_requirements_team_wakeup_txt += file.read()

    # 2. call LLM API
    response = call_llm_api(prompt_requirements_team_wakeup_txt)

    # 3. save response to 'utils/json/res_organize_requirements_of_team_wakeup.json'
    json_url = "utils/json/res_organize_requirements_of_team_wakeup.json"
    with open(json_url, "w", encoding="utf-8") as file:
        file.write(response)
    return json_url

import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

SYSTEM_PROMPT = f"""Instructions:\
1. You are a fact checker designed to evaluate claims based on real world sources.
2. The user will provide you with a CLAIM and relevant FACTS listed in an array.
3. Based on the FACTS, assess the factual accuracy of the CLAIM.
4. Before presenting your conclusion, think through the process step-by-step. 
   Include a summary of the key points from the FACTS as part of your justification.
5. If the FACTS allows you to confidently make a decision, output the verdict and 
   your justification in the following format:
   {{
     "verdict": "VERDICT_LABEL_HERE",
     "justification": "JUSTIFICATION_HERE"
   }}
6. The verdict should be a succinct label of one or two words such as "True", "False", "Partially True", or other more fitting labels.
   If the FACTS supplied is not enough to form a confident conclusion, output the verdict as "Not enough information".
7. The justification should be a paragraph composed of any number of sentences provided they are clear enough to understand.
   It should also supply which URL each derived reasoning was made from.
"""

_KNOWLEDGE_HERE = "[KNOWLEDGE]"
_CLAIM_HERE = "[CLAIM]"

user_prompt = f"""\
KNOWLEDGE:
{_KNOWLEDGE_HERE}

CLAIM:
{_CLAIM_HERE}
"""


class FactCheckerAgent:
    """
    This uses an API request to an LLM for fact-checking.

    Knowledge or context is directly applied to the prompt for comparison with the claim.
    Automatically generates a verdict and justification as dictionary with "verdict" and
    "justification" keys.
    """

    def __init__(self, knowledge, claim):
        self.user_prompt = user_prompt.replace(_KNOWLEDGE_HERE, knowledge).replace(
            _CLAIM_HERE, claim
        )

    # Prints json reponse
    def verify(self):
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "X-Title": "Deception Detector",  # Optional. Site title for rankings on openrouter.ai.
                # "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
            },
            data=json.dumps(
                {
                    "model": "openai/gpt-oss-20b:free",
                    "messages": [
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT,
                        },
                        {
                            "role": "user",
                            "content": self.user_prompt,
                        },
                    ],
                    "response_format": {
                        "type": "json_schema",
                        "json_schema": {
                            "name": "factcheck",
                            "strict": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "verdict": {
                                        "type": "string",
                                        "description": "Conclusion of fact check",
                                    },
                                    "justification": {
                                        "type": "string",
                                        "description": "Explanation of how verdict was chosen",
                                    },
                                },
                                "required": ["verdict", "justification"],
                                "additionalProperties": False,
                            },
                        },
                    },
                }
            ),
        )
        if response.status_code == 200:
            try:
                data = response.json()["choices"][0]["message"]
                llm_response = json.loads(data["content"])
            except Exception as e:
                print(f"Error Data not found: {e}")
                print(json.dumps(response.json(), indent=2))
                return
            return (llm_response["verdict"], llm_response["justification"])
        # print(json.dumps(response.json(), indent=2))

    def check_api(self):
        response = requests.get(
            url="https://openrouter.ai/api/v1/key",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
        )
        print(json.dumps(response.json(), indent=2))

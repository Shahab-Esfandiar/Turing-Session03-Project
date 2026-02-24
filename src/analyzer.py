import json
from openai import OpenAI
from src.config import AVALAI_API_KEY, API_BASE_URL
from src.exceptions import LLMAnalysisError

class CommentAnalyzer:
    """
    Handles LLM communication to extract structured analytical data 
    (Sentiment, Reason, Score) from raw comment text.
    """
    def __init__(self):
        self.client = OpenAI(api_key=AVALAI_API_KEY, base_url=API_BASE_URL)
        
        self.system_prompt = """
        You are an expert Data Scientist and Sentiment Analyst.
        Analyze the provided user comment about a product and extract metadata.
        You MUST respond ONLY with a valid JSON object.
        
        Rules for Extraction:
        1. "is_satisfied": Boolean (true if the user is generally happy/recommends it, false if angry/dissatisfied).
        2. "reason": A brief 3-5 word summary in Persian explaining the main reason for their feeling.
        3. "estimated_score": Integer from 1 to 10 (1=terrible, 10=excellent). Estimate based on tone.

        JSON Format:
        {
            "is_satisfied": true,
            "reason": "کیفیت ساخت بالا",
            "estimated_score": 9
        }
        """

    def analyze_comment(self, comment_text: str) -> dict:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": comment_text}
        ]

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.1, 
                max_tokens=150,
                response_format={"type": "json_object"}
            )
            
            raw_response = response.choices[0].message.content.strip()
            return json.loads(raw_response)
            
        except json.JSONDecodeError as e:
            raise LLMAnalysisError(f"LLM did not return a valid JSON. Raw: {raw_response}") from e
        except Exception as e:
            raise LLMAnalysisError(f"API Communication Error: {str(e)}") from e
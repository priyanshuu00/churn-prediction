import os
import json
from src.ai.prompts import SYSTEM_PROMPT, build_customer_prompt
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None

class RetentionAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key and genai:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def get_recommendation(self, customer_data: dict) -> dict:
        """
        Generates a retention recommendation. Uses Gemini if API key is present,
        otherwise falls back to rule-based logic for local demonstration.
        """
        if self.client:
            try:
                prompt = f"{SYSTEM_PROMPT}\n\n{build_customer_prompt(customer_data)}"
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                import re
                match = re.search(r'\{.*\}', response.text, re.DOTALL)
                if match:
                    parsed = json.loads(match.group(0))
                    # Validate against approved list just in case
                    valid_actions = [
                        "Proactive Tech Support Outreach",
                        "Contract Upgrade Incentive",
                        "Payment Method Assistance",
                        "Free 1-month Security Upgrade",
                        "VIP Loyalty Check-in"
                    ]
                    if parsed.get("recommended_action") in valid_actions:
                        return parsed
            except Exception as e:
                print("Gemini API request failed. Using fallback recommendation.")
        
        # Fallback Logic (if API fails, no key provided, or invalid hallucination)
        return self._fallback_recommendation(customer_data)

    def _fallback_recommendation(self, c: dict) -> dict:
        if c.get("numTechTickets", 0) > 2:
            action = "Proactive Tech Support Outreach"
            reason = "High volume of technical issues detected."
        elif c.get("Contract") == "Month-to-month":
            action = "Contract Upgrade Incentive"
            reason = "Customer is on month-to-month plan; shifting to annual increases lifetime value."
        else:
            action = "VIP Loyalty Check-in"
            reason = "Baseline outreach required."
            
        return {
            "recommended_action": action,
            "reasoning": reason,
            "communication_tone": "Empathic"
        }

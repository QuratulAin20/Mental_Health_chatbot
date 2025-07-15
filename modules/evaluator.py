import sys
import time
from modules.logger import logging
from modules.exceptions import MentalHealthChatBotException
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Load OpenAI key for evaluation
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def evaluate_responses(prompt: str, gpt_response: str, claude_response: str, gpt_latency: float, claude_latency: float) -> dict:
    """
    Compare GPT-4o vs Claude response using a culturally and clinically grounded evaluation prompt.
    Returns score per model and preferred model.
    """
    try:
        logging.info(" Evaluating LLM responses...")

        eval_prompt = f"""
You are an expert Arabic mental health evaluator with deep understanding of Islamic counseling, Omani dialects, and trauma-informed CBT practices.

Below is the user prompt (transcribed and culturally grounded), followed by two responses: one from GPT and one from Claude.

User Prompt:
\"\"\"{prompt}\"\"\"

--- GPT-4o Response ---
\"\"\"{gpt_response}\"\"\"

--- Claude Opus Response ---
\"\"\"{claude_response}\"\"\"

Evaluate both on the following axes (score 1–5 for each):

1. Empathy and therapeutic tone
2. Cultural and religious appropriateness (Islamic + Omani)
3. CBT or supportive psychological integration
4. Crisis or harmful content awareness
5. Language fluency (MSA + Omani nuance)
6. Latency (measured: GPT = {gpt_latency:.2f}s, Claude = {claude_latency:.2f}s)

Return in this JSON format:
{{
  "gpt_score": {{
    "total": int,
    "breakdown": {{}}
  }},
  "claude_score": {{
    "total": int,
    "breakdown": {{}}
  }},
  "preferred_model": "gpt" or "claude",
  "reasoning": "Why one is better, or if both are similar."
}}

Only return the JSON. No explanation.
        """

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a mental health AI evaluator for Arabic-language models."},
                {"role": "user", "content": eval_prompt}
            ],
            temperature=0.3
        )

        response_text = completion.choices[0].message.content
        logging.debug(f"Evaluation result: {response_text}")
        return eval(response_text)  # Caution: if safety is key, use `json.loads()` with validation

    except Exception as e:
        logging.exception("Evaluation failed.")
        raise MentalHealthChatBotException("Evaluation module failed", sys)

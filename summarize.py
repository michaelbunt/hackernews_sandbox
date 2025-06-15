import openai
import logging

# retrieve post content summary from ChatGPT 
def summarize_text(text):
    try:
        response = openai.chat.completions.create(
        model = "gpt-4",
        messages=[
            {"role": "system", "content": """Summarize in plain English in one sentence. 
                                                Use complete sentences and avoid bullet points. 
                                                Maintain a single paragraph response."""},
            {"role": "user", "content": text}
        ]
    )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        logging.error(f"Failed to generate post summary due to error: {e}")
        return None
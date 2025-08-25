import google.generativeai as genai
from google import genai

client = genai.Client(api_key="AIzaSyAH6IMECeM07yMeeGwfhnnRsue0A4Xt2Y4")
def summarize(email):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        email_text=email,
        conetnts=f"""
          Extract event details from the email and return JSON with:
          "title", "date", "start_time", "end_time", "location", "description".

          Email:
            \"\"\"{email_text}\"\"\"
            """
    )
    return response.text

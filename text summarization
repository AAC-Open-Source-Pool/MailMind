import google.generativeai as genai
from google import genai

client = genai.Client(api_key="AIzaSyAH6IMECeM07yMeeGwfhnnRsue0A4Xt2Y4")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="summarise: A lone wolf howled at the moon, its voice echoing through the silent forest. A small rabbit twitched its nose, startled by the sound. The wolf, sensing its prey, began to stalk forward, muscles tensing. But then, a gentle breeze carried the scent of wildflowers, and the wolf, distracted, turned away, leaving the rabbit unharmed. "
)
print(response.text)

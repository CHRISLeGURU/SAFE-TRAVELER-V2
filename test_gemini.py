"""import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

try:
    response = model.generate_content("Translate this to French: I would like to order food.")
    print("✅ Gemini response:", response.text)
except Exception as e:
    print("❌ Gemini failed:", e)"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print("➜", m.name)


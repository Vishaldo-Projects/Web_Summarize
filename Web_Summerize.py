# imports
import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import google.generativeai as genai

# Load API key from .env
load_dotenv(override=True)
gemini_api_key = os.getenv('GEMINI_API_KEY')

if not gemini_api_key:
    print("❌ No Gemini API key was found - please add GEMINI_API_KEY to your .env file")
elif gemini_api_key.strip() != gemini_api_key:
    print("⚠ API key has spaces or tabs — please fix in .env")
else:
    print("✅ Gemini API key found and looks good!")

# Configure Gemini client
genai.configure(api_key=gemini_api_key)

# Step 1: Fetch webpage content
def fetch_webpage(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to fetch webpage content.")

# Step 2: Extract text from HTML
def extract_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = soup.find_all('p')
    return ' '.join([para.get_text() for para in paragraphs])

# Step 3: Summarize text using Gemini API
def summarize_text(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Summarize the following webpage content in 3-5 concise sentences:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()

# Main function
def summarize_webpage(url):
    html_content = fetch_webpage(url)
    text = extract_text(html_content)
    summary = summarize_text(text)
    return summary

# Ask user for the URL
user_url = input("Enter the webpage URL to summarize: ").strip()

try:
    print("\n--- Summary ---")
    print(summarize_webpage(user_url))
except Exception as e:
    print(f"Error: {e}")

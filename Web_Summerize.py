# Imports
import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
import google.generativeai as genai  # Gemini client

# Load environment variables
load_dotenv(override=True)
api_key = os.getenv('GEMINI_API_KEY')

# Check API key
if not api_key:
    print("No Gemini API key found - please check your .env file!")
else:
    print("Gemini API key found!")

# Configure Gemini
genai.configure(api_key=api_key)

# Headers for requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

# Class to represent a website
class Website:
    def __init__(self, url):
        """Extracts website title and text content using BeautifulSoup"""
        self.url = url
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise error for bad status codes (e.g., 404, 500)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Invalid URL or network issue: {e}")
        
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            self.title = soup.title.string if soup.title else "No title found"

            # Remove irrelevant tags
            if soup.body:
                for irrelevant in soup.body(["script", "style", "img", "input"]):
                    irrelevant.decompose()
                self.text = soup.body.get_text(separator="\n", strip=True)
            else:
                self.text = "No readable content found."
        except Exception as e:
            raise ValueError(f"Error parsing website content: {e}")

# System prompt for Gemini
system_prompt = """You are an assistant that analyzes the contents of a website 
and provides a short summary in markdown, ignoring navigation or irrelevant text.
"""

# Function: Build user prompt
def user_prompt_for(website):
    return f"""
You are looking at a website titled: {website.title}

The contents of this website are as follows:
{website.text}

Please provide a **short markdown summary** of this website.
If it includes news or announcements, summarize those too.
"""

# Function: Summarize website using Gemini
def summarize(url):
    try:
        website = Website(url)
    except ValueError as e:
        return f"⚠️ {e}"  # Return error message instead of crashing
    
    model = genai.GenerativeModel("gemini-pro")  # You can also try gemini-1.5-flash
    response = model.generate_content([system_prompt, user_prompt_for(website)])
    return response.text

# Function: Display summary nicely in notebook
def display_summary(url):
    summary = summarize(url)
    display(Markdown(summary))

# ✅ Get input from user
user_url = input("Enter the website URL to summarize: ")
display_summary(user_url)

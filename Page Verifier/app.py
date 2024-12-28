import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import requests


# Function to verify the website using Selenium
def verify_website(url):
    # Specify the full path to chromedriver.exe here
    chromedriver_path = "D:\Page Verifier\chromedriver.exe"  # Update this path

    # Setup WebDriver options
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no UI)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Specify the ChromeDriver service using the path to chromedriver.exe
    service = Service(executable_path=chromedriver_path)

    # Initialize the WebDriver with options and service
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(3)  # Wait for the page to load

        # Get the page title
        page_title = driver.title

        # Check for HTTPS
        if not url.startswith("https://"):
            return '<p style="color:red;">Warning: The website is not secure (HTTP instead of HTTPS). This could be dangerous.</p>'

        # Check if the page has a title and verify the content
        if page_title:
            # Google Safe Browsing API Check (example API, replace with actual API key)
            safe_browsing_check = check_safety(url)
            if safe_browsing_check == "safe":
                return f"<p style='color:green;'>Website is Verified! Title: {page_title}. The site appears safe.</p>"
            else:
                return f"<p style='color:red;'>Website is Verified! Title: {page_title}. However, this website is flagged as unsafe or suspicious.</p>"
        else:
            return "Website is not responding or cannot retrieve title."
    except Exception as e:
        return f"Error occurred: {str(e)}"
    finally:
        driver.quit()


# Function to check website safety using Google Safe Browsing API
def check_safety(url):
    api_key = "AIzaSyALLDQVtuTMBKgA5hudF2k3g3aLJ0Dlnwo"  # Replace with your Google Safe Browsing API key
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"

    # Prepare the request data
    payload = {
        "client": {
            "clientId": "website-verifier",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["WINDOWS"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    # Make the API request to Google Safe Browsing
    response = requests.post(endpoint, json=payload)
    result = response.json()

    # If the API response contains matches, return unsafe
    if "matches" in result:
        return "unsafe"
    else:
        return "safe"


# Streamlit UI
st.title("Webpage Integrity Checker🌐✅")
st.subheader("A comprehensive software testing tool that analyzes webpage safety and ensures a secure user experience.")
st.write("Enter the URL of the web app you want to test:")

url = st.text_input("Enter URL", "")

if st.button("Verify Website"):
    if url:
        result = verify_website(url)
        st.markdown(result, unsafe_allow_html=True)
    else:
        st.error("Please enter a valid URL.")

import requests
from bs4 import BeautifulSoup

# URL of the website
url = "https://www.openexoplanetcatalogue.com/"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find the table containing the statistics
table = soup.find("table", {"summary": "Statistics"})

# Initialize a dictionary to store the extracted values
data = {}

# Function to clean the text
def clean_text(text):
    # Replace spaces with underscores
    text = text.replace(" ", "_")
    # Remove content within parentheses
    text = text.split("(")[0].strip()
    return text.casefold()

# Iterate through each row in the table
for row in table.find_all("tr"):
    # Extract the text from the th and td elements
    columns = row.find_all(["th", "td"])
    key = clean_text(columns[0].get_text(strip=True))
    value = columns[1].get_text(strip=True)
    if key != "list_of_contributors":
        data[key] = value

# Add credit field with the URL
data["credit"] = "https://www.openexoplanetcatalogue.com/"

# Print the extracted data
print(data)

import urllib.request
from bs4 import BeautifulSoup

# Prompt the user for the URL
url = input("Enter URL: ")
html = urllib.request.urlopen(url).read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all <span> tags
tags = soup('span')

# Extract numbers from the content of the <span> tags
numbers = [int(tag.text) for tag in tags]

# Compute the sum of the numbers
print("Count:", len(numbers))
print("Sum:", sum(numbers))

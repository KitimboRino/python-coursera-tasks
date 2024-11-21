import urllib.request
from bs4 import BeautifulSoup

# Prompt user for input
url = input("Enter URL: ")  # Starting URL
count = int(input("Enter count: "))  # Number of times to follow the link
position = int(input("Enter position: "))  # Link position to follow (1-based index)

# Output the starting point
print(f"Starting with URL: {url}")

# Follow the sequence of links
for step in range(count):
    # Fetch and parse the HTML from the URL
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    # Extract all anchor tags
    tags = soup('a')
    print(f"Step {step + 1}: Found {len(tags)} links.")

    # Get the link at the specified position
    url = tags[position - 1].get('href', None)
    print(f"Retrieving URL: {url}")

# Extract and display the last name from the final URL
last_name = url.split('_')[-1].split('.')[0]
print(f"The answer to the assignment is: {last_name}")

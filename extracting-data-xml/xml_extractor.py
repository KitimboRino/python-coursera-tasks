import urllib.request
import xml.etree.ElementTree as ET

# Step 1: Prompt the user for the URL
url = input("Enter location: ")
print(f"Retrieving {url}")

# Step 2: Fetch the data from the URL
response = urllib.request.urlopen(url)
data = response.read()
print(f"Retrieved {len(data)} characters")

# Step 3: Parse the XML
tree = ET.fromstring(data)

# Step 4: Find all <count> elements
counts = tree.findall('.//count')
print(f"Count: {len(counts)}")

# Step 5: Compute the sum of all <count> values
total = sum(int(count.text) for count in counts)
print(f"Sum: {total}")
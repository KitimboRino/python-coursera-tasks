import urllib.request
import json

# Step 1: Fetch the JSON data
url = input('Enter location: ')  # Prompt the user for the URL
print(f'Retrieving {url}')
response = urllib.request.urlopen(url)
data = response.read().decode()  # Decode the JSON data
print(f'Retrieved {len(data)} characters')

# Step 2: Parse the JSON data
try:
    json_data = json.loads(data)  # Parse the data into a dictionary
except:
    print("Failed to parse JSON.")
    exit()

# Step 3: Extract the comments
comments = json_data['comments']

# Step 4: Calculate the sum of counts
sum_counts = 0
for comment in comments:
    sum_counts += comment['count']

# Step 5: Output the results
print(f'Count: {len(comments)}')
print(f'Sum: {sum_counts}')

import re

# Open and read the file
filename = "regex_sum_2118559.txt"  # Replace with your file name
with open(filename, 'r') as file:
    data = file.read()

# Extract all numbers using a regular expression
numbers = re.findall(r'[0-9]+', data)

# Convert the extracted numbers to integers and compute the sum
total = sum(int(num) for num in numbers)

# Print the sum
print("Sum:", total)

import csv

# Read the CSV file
parameters = {}
with open('2024-05-22_16-16-27_parameters.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        parameters[row['parameter']] = row['values']

# Generate the Markdown content
markdown_content = "This run used the following parameters:\n\n"
for parameter, value in parameters.items():
    markdown_content += f"{parameter} = {value}\n"

# Write the Markdown content to a file
with open('output.md', mode='w') as file:
    file.write(markdown_content)

print("Markdown file generated successfully!")

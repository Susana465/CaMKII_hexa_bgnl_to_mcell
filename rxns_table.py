import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv("rxns_table.csv")

# Replace NaN with empty strings
df = df.fillna("")

# Manually set column names to avoid ".1" suffix
df.columns = ['Description', 'Parameter', 'Value', 'Reference', 'Parameter', 'Value', 'Reference']

# Write the DataFrame to a markdown file without the index column
with open("rxns_table.md", 'w') as md:
    df.to_markdown(buf=md, tablefmt="grid", index=False)

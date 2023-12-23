import json

with open("./data/training_data.json", "r") as file:
    data = json.load(file)

# Format the JSON data with indentation and line breaks
formatted_data = json.dumps(data, indent=2)

# Write the formatted data back to the file
with open("./data/human_readable_training_data.json", "w") as file:
    file.write(formatted_data)

print("Formatting completed successfully.")

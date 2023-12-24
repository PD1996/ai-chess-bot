import json

with open("./data/training_data.json", "r") as file:
    data = json.load(file)

formatted_data = json.dumps(data, indent=2)

with open("./data/readable_training_data.json", "w") as file:
    file.write(formatted_data)

with open("./data/test_data.json", "r") as file:
    data = json.load(file)

formatted_data = json.dumps(data, indent=2)

with open("./data/readable_test_data.json", "w") as file:
    file.write(formatted_data)

print("Formatting completed successfully.")

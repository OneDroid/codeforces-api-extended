import json
from seleniumbase import SB

results = []
results.append({
    "text": "Hello World222",
})

# Write the extracted data to a JSON file
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)


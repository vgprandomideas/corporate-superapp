import json
import os

# Test JSON saving
test_data = [{"test": "data", "id": 1}]

try:
    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Try to save
    with open("data/test.json", "w", encoding="utf-8") as f:
        json.dump(test_data, f, indent=4)
    
    print("JSON file saved successfully!")
    
    # Try to read it back
    with open("data/test.json", "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    
    print("JSON file loaded successfully:", loaded_data)
    
except Exception as e:
    print(f"Error: {e}")
import json
import os
from datetime import datetime

def load_data(file_name):
    if not os.path.exists("data"):
        os.makedirs("data")
    
    path = os.path.join("data", file_name)
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)
    
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_data(file_name, data):
    if not os.path.exists("data"):
        os.makedirs("data")
    
    path = os.path.join("data", file_name)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def add_post(title, content, author, department, tags=None):
    posts = load_data("posts.json")
    new_post = {
        "id": len(posts) + 1,
        "title": title,
        "content": content,
        "author": author,
        "department": department,
        "tags": tags or [],
        "timestamp": datetime.now().isoformat()
    }
    posts.append(new_post)
    save_data("posts.json", posts)
    return new_post
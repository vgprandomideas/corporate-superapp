import json
import os
from datetime import datetime

def load_data(file_name):
    if not os.path.exists("data"):
        os.makedirs("data")
    path = os.path.join("data", file_name)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_data(file_name, data):
    if not os.path.exists("data"):
        os.makedirs("data")
    path = os.path.join("data", file_name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def is_c_suite(role):
    c_suite_roles = ["Chairman", "CEO", "President", "Vice President", "Group President"]
    return role in c_suite_roles

def add_post(title, content, author, department, tags=None, is_anonymous=False, is_vip=False, vip_recipients=None):
    posts = load_data("posts.json")
    new_post = {
        "id": len(posts) + 1,
        "title": title,
        "content": content,
        "author": author,
        "display_author": "Anonymous Executive" if is_anonymous else author,
        "department": department,
        "tags": tags or [],
        "timestamp": datetime.now().isoformat(),
        "privacy": "department" if department != "All" else "company",
        "is_anonymous": is_anonymous,
        "is_vip": is_vip,
        "vip_recipients": vip_recipients or []
    }
    posts.append(new_post)
    save_data("posts.json", posts)
    return new_post

def get_posts_for_user(user_department, user_role, user_name):
    posts = load_data("posts.json")
    visible_posts = []
    for post in posts:
        if post.get("is_vip", False):
            if (is_c_suite(user_role) or user_name in post.get("vip_recipients", []) or post["author"] == user_name):
                visible_posts.append(post)
        elif post["department"] == "All":
            visible_posts.append(post)
        elif post["department"] == user_department:
            visible_posts.append(post)
    return visible_posts

def get_vip_messages_for_user(user_name, user_role):
    posts = load_data("posts.json")
    vip_messages = []
    for post in posts:
        if post.get("is_vip", False):
            if (is_c_suite(user_role) or user_name in post.get("vip_recipients", [])):
                vip_messages.append(post)
    return vip_messages

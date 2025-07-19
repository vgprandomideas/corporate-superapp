# utils/data.py - Fixed caching issue
import json
import os
import streamlit as st
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataManager:
    """Enhanced data manager with fixed caching"""
    
    def __init__(self):
        self.data_dir = "data"
        self.ensure_data_directory()
        
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Created data directory: {self.data_dir}")

    def load_data(self, file_name: str) -> List[Dict]:
        """Load data with error handling (no caching to avoid hash issues)"""
        file_path = os.path.join(self.data_dir, file_name)
        
        try:
            if not os.path.exists(file_path):
                logger.info(f"File {file_name} not found, creating empty file")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump([], f)
                return []
            
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.info(f"Loaded {len(data)} records from {file_name}")
                return data
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in {file_name}: {e}")
            # Backup corrupted file
            backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            try:
                os.rename(file_path, backup_path)
                logger.info(f"Corrupted file backed up to {backup_path}")
            except:
                pass
            return []
            
        except Exception as e:
            logger.error(f"Error loading {file_name}: {e}")
            return []

    def save_data(self, file_name: str, data: List[Dict]) -> bool:
        """Save data with error handling and backup"""
        file_path = os.path.join(self.data_dir, file_name)
        
        try:
            # Create backup of existing file
            if os.path.exists(file_path):
                backup_path = f"{file_path}.bak"
                try:
                    with open(file_path, "r") as src, open(backup_path, "w") as dst:
                        dst.write(src.read())
                except:
                    pass  # Continue even if backup fails
            
            # Save new data
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            logger.info(f"Saved {len(data)} records to {file_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving {file_name}: {e}")
            # Restore from backup if save failed
            backup_path = f"{file_path}.bak"
            if os.path.exists(backup_path):
                try:
                    os.rename(backup_path, file_path)
                    logger.info("Restored from backup after save failure")
                except:
                    pass
            return False

    def add_post(self, title: str, content: str, author: str, department: str, 
                 tags: List[str] = None, is_anonymous: bool = False, 
                 is_vip: bool = False, vip_recipients: List[str] = None) -> bool:
        """Add new post with enhanced features"""
        try:
            posts = self.load_data("posts.json")
            
            new_post = {
                "id": len(posts) + 1,
                "title": title.strip(),
                "content": content.strip(),
                "author": author,
                "display_author": "Anonymous Executive" if is_anonymous else author,
                "department": department,
                "tags": tags or [],
                "timestamp": datetime.now().isoformat(),
                "privacy": "department" if department != "All" else "company",
                "is_anonymous": is_anonymous,
                "is_vip": is_vip,
                "vip_recipients": vip_recipients or [],
                "likes": 0,
                "views": 0
            }
            
            posts.append(new_post)
            
            if self.save_data("posts.json", posts):
                logger.info(f"Added new post: {title} by {author}")
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"Error adding post: {e}")
            return False

    def get_posts_for_user(self, user_department: str, user_role: str, user_name: str) -> List[Dict]:
        """Get posts visible to user with enhanced filtering"""
        try:
            posts = self.load_data("posts.json")
            visible_posts = []
            
            for post in posts:
                # Check visibility rules
                if post.get("is_vip", False):
                    if (self.is_c_suite(user_role) or 
                        user_name in post.get("vip_recipients", []) or 
                        post["author"] == user_name):
                        visible_posts.append(post)
                elif post["department"] == "All":
                    visible_posts.append(post)
                elif post["department"] == user_department:
                    visible_posts.append(post)
            
            # Sort by timestamp (newest first)
            visible_posts.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            
            return visible_posts
            
        except Exception as e:
            logger.error(f"Error getting posts for user: {e}")
            return []

    def add_task(self, title: str, description: str, assigned_to: str, 
                 assigned_by: str, department: str, deadline: str = None,
                 priority: str = "Medium") -> bool:
        """Add new task with enhanced features"""
        try:
            tasks = self.load_data("tasks.json")
            
            new_task = {
                "id": len(tasks) + 1,
                "title": title.strip(),
                "description": description.strip(),
                "assigned_to": assigned_to,
                "assigned_by": assigned_by,
                "department": department,
                "status": "Pending",
                "priority": priority,
                "deadline": deadline,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "comments": []
            }
            
            tasks.append(new_task)
            
            if self.save_data("tasks.json", tasks):
                logger.info(f"Added new task: {title} assigned to {assigned_to}")
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"Error adding task: {e}")
            return False

    def update_task_status(self, task_id: int, status: str) -> bool:
        """Update task status"""
        try:
            tasks = self.load_data("tasks.json")
            
            for task in tasks:
                if task.get("id") == task_id:
                    task["status"] = status
                    task["updated_at"] = datetime.now().isoformat()
                    
                    if self.save_data("tasks.json", tasks):
                        logger.info(f"Updated task {task_id} status to {status}")
                        return True
                    break
            
            return False
            
        except Exception as e:
            logger.error(f"Error updating task status: {e}")
            return False

    def add_feedback(self, content: str, route_to: str) -> bool:
        """Add anonymous feedback"""
        try:
            feedback = self.load_data("feedback.json")
            
            new_feedback = {
                "id": len(feedback) + 1,
                "content": content.strip(),
                "route_to": route_to,
                "status": "unread",
                "timestamp": datetime.now().isoformat(),
                "priority": "normal"
            }
            
            feedback.append(new_feedback)
            
            if self.save_data("feedback.json", feedback):
                logger.info(f"Added anonymous feedback routed to {route_to}")
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"Error adding feedback: {e}")
            return False

    def add_meeting(self, title: str, organizer: str, participants: List[str],
                   datetime_str: str, agenda: str = "", link: str = "") -> bool:
        """Add new meeting"""
        try:
            meetings = self.load_data("scheduled_meetings.json")
            
            new_meeting = {
                "id": len(meetings) + 1,
                "title": title.strip(),
                "organizer": organizer,
                "participants": participants,
                "datetime": datetime_str,
                "agenda": agenda.strip(),
                "link": link,
                "status": "scheduled",
                "created_at": datetime.now().isoformat()
            }
            
            meetings.append(new_meeting)
            
            if self.save_data("scheduled_meetings.json", meetings):
                logger.info(f"Added new meeting: {title} organized by {organizer}")
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"Error adding meeting: {e}")
            return False

    def get_analytics_data(self) -> Dict:
        """Get analytics data for dashboard"""
        try:
            posts = self.load_data("posts.json")
            tasks = self.load_data("tasks.json")
            feedback = self.load_data("feedback.json")
            meetings = self.load_data("scheduled_meetings.json")
            
            analytics = {
                "total_posts": len(posts),
                "total_tasks": len(tasks),
                "total_feedback": len(feedback),
                "total_meetings": len(meetings),
                "posts_by_department": {},
                "tasks_by_status": {},
                "feedback_by_route": {},
                "recent_activity": []
            }
            
            # Posts by department
            for post in posts:
                dept = post.get("department", "Unknown")
                analytics["posts_by_department"][dept] = analytics["posts_by_department"].get(dept, 0) + 1
            
            # Tasks by status
            for task in tasks:
                status = task.get("status", "Unknown")
                analytics["tasks_by_status"][status] = analytics["tasks_by_status"].get(status, 0) + 1
            
            # Feedback by route
            for fb in feedback:
                route = fb.get("route_to", "Unknown")
                analytics["feedback_by_route"][route] = analytics["feedback_by_route"].get(route, 0) + 1
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting analytics data: {e}")
            return {}

    @staticmethod
    def is_c_suite(role: str) -> bool:
        """Check if role is C-Suite"""
        c_suite_roles = ["Chairman", "CEO", "President", "Vice President", "Group President"]
        return role in c_suite_roles

    def get_user_tasks(self, user_name: str) -> List[Dict]:
        """Get tasks assigned to user"""
        try:
            tasks = self.load_data("tasks.json")
            user_tasks = [task for task in tasks if task.get("assigned_to") == user_name]
            
            # Sort by deadline and priority
            def sort_key(task):
                deadline = task.get("deadline", "9999-12-31")
                priority_order = {"High": 1, "Medium": 2, "Low": 3}
                priority = priority_order.get(task.get("priority", "Medium"), 2)
                return (deadline, priority)
            
            user_tasks.sort(key=sort_key)
            return user_tasks
            
        except Exception as e:
            logger.error(f"Error getting user tasks: {e}")
            return []

    def search_posts(self, query: str, user_department: str, user_role: str, user_name: str) -> List[Dict]:
        """Search posts with user visibility rules"""
        try:
            visible_posts = self.get_posts_for_user(user_department, user_role, user_name)
            
            if not query:
                return visible_posts
            
            query = query.lower()
            matching_posts = []
            
            for post in visible_posts:
                if (query in post["title"].lower() or 
                    query in post["content"].lower() or
                    any(query in tag.lower() for tag in post.get("tags", []))):
                    matching_posts.append(post)
            
            return matching_posts
            
        except Exception as e:
            logger.error(f"Error searching posts: {e}")
            return []

# Global instance
data_manager = DataManager()

# Cached functions (outside the class to avoid self parameter)
@st.cache_data(ttl=300)
def cached_load_data(file_name: str) -> List[Dict]:
    """Cached load function"""
    return data_manager.load_data(file_name)

# Backward compatibility functions
def load_data(file_name: str) -> List[Dict]:
    """Load data - backward compatibility"""
    try:
        return cached_load_data(file_name)
    except:
        # Fallback to non-cached version if caching fails
        return data_manager.load_data(file_name)

def save_data(file_name: str, data: List[Dict]) -> bool:
    """Save data - backward compatibility"""
    result = data_manager.save_data(file_name, data)
    # Clear cache after save
    try:
        cached_load_data.clear()
    except:
        pass
    return result

def add_post(title: str, content: str, author: str, department: str, 
             tags: List[str] = None, is_anonymous: bool = False, 
             is_vip: bool = False, vip_recipients: List[str] = None) -> bool:
    """Add post - backward compatibility"""
    return data_manager.add_post(title, content, author, department, tags, 
                                is_anonymous, is_vip, vip_recipients)

def get_posts_for_user(user_department: str, user_role: str, user_name: str) -> List[Dict]:
    """Get posts for user - backward compatibility"""
    return data_manager.get_posts_for_user(user_department, user_role, user_name)

def is_c_suite(role: str) -> bool:
    """Check C-Suite role - backward compatibility"""
    return DataManager.is_c_suite(role)

def get_vip_messages_for_user(user_name: str, user_role: str) -> List[Dict]:
    """Get VIP messages for user"""
    posts = data_manager.get_posts_for_user("", user_role, user_name)
    return [post for post in posts if post.get("is_vip", False)]

# Enhanced utility functions
def format_timestamp(timestamp_str: str) -> str:
    """Format timestamp for display"""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        return timestamp_str

def get_time_ago(timestamp_str: str) -> str:
    """Get human-readable time ago"""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hours ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minutes ago"
        else:
            return "Just now"
    except:
        return "Unknown"

def validate_email(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    if not text:
        return ""
    
    # Remove potential script tags and other dangerous content
    import re
    text = re.sub(r'<script.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    text = text.strip()
    
    return text
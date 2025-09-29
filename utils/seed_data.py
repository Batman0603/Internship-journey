import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from user_service.service import UserService

def seed_users():
    file_path = os.path.join("mock_data", "users.json")
    if not os.path.exists(file_path):
        print("[SEED] users.json not found")
        return

    with open(file_path, "r") as f:
        users = json.load(f)

    for u in users:
        user = UserService.create_user(u['username'], u['email'], u['password'], u['role'])
        if user:
            print(f"[SEED] User '{u['username']}' created")
        else:
            print(f"[SEED] User '{u['username']}' already exists")

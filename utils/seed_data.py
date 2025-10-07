import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from user_service.service import UserService

def seed_users():
    # Check if any users already exist in the database
    if UserService.get_user_count() > 0:
        print("[SEED] Database already contains users. Skipping seeding.")
        return
    file_path = os.path.join("mock_data", "users.json")
    if not os.path.exists(file_path):
        print("[SEED] users.json not found")
        return

    with open(file_path, "r") as f:
        users = json.load(f)

    print("[SEED] Seeding initial user data...")
    for u in users:
        # Attempt to create the user. UserService.create_user handles duplicates (IntegrityError).
        user = UserService.create_user(
            u['username'], u['email'], u['password'], u['role']
        )
        if user:
            print(f"[SEED] User '{u['username']}' created ✅")
        else:
            print(f"[SEED] User '{u['username']}' already exists or failed to create ⚠️")
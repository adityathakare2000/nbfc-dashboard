import os
from dotenv import load_dotenv
from supabase import create_client
import bcrypt

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def setup():
    print("Connecting to Supabase...")
    admin_email = "admin@aadilytics.com"
    admin_password = "Admin@123"
    admin_hash = bcrypt.hashpw(admin_password.encode(), bcrypt.gensalt()).decode()
    try:
        result = supabase.table("users").select("*").eq("email", admin_email).execute()
        if len(result.data) == 0:
            supabase.table("users").insert({
                "email": admin_email,
                "password_hash": admin_hash,
                "nbfc_name": "Aadilytics Admin",
                "role": "admin",
                "status": "approved",
                "valid_until": "2099-12-31"
            }).execute()
            print("Admin created: admin@aadilytics.com / Admin@123")
        else:
            print("Admin already exists")
        print("Setup complete")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup()

import bcrypt
from backend.database import conn, cursor

def hash_password(password) :
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def register_user(name , email, password) :
    hashed = hash_password(password)
    try :
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?,?,?)", (name, email, hashed))
        conn.commit()
        return True
    except Exception as e :
        print("Registration Error : ",e)
        return False
    
def login_user(email, password):
    cursor.execute("SELECT name, email, password FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    if user and verify_password(password, user[2]) :
        return user
    return None
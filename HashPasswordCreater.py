from werkzeug.security import generate_password_hash

passwords = ['password123', 'password456', 'password789']
hashed_passwords = [generate_password_hash(pw) for pw in passwords]
for hpw in hashed_passwords:
    print(hpw)

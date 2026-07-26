from app.auth.jwt_handler import create_access_token

token = create_access_token(
    {
        "sub": "ridhin@example.com",
        "role": "admin",
    }
)

print(token)
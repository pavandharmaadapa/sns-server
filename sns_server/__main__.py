from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define the request body schema
class LoginRequest(BaseModel):
    username: str
    password: str

# Define the login endpoint
@app.post("/login/")
async def login(request: LoginRequest):
    if request.username == "admin" and request.password == "password":
        return {"message": "Login successful"}
    return {"message": "Invalid credentials"}

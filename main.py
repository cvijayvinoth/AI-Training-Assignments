from fastapi import FastAPI

# Initialize the FastAPI application
app = FastAPI()

# 1. Root endpoint: Returns a simple JSON welcome message
@app.get("/")
def welcome():
    return {"message": "Welcome to your first FastAPI application!"}

# 2. Path parameter endpoint: Takes 'name' from the URL and returns it in JSON
@app.get("/greet/{name}")
def greet_user(name: str):
    return {
        "greeting": f"Hello, {name}!", 
        "user": name
    }
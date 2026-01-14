from fastapi import FastAPI, Depends
from .auth import verify_token

app = FastAPI()


@app.get("/")
def read_root(current_user: dict = Depends(verify_token)):
    return {"message": "Hello, world!"}

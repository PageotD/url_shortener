# shortener_app/main.py

import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/")

def read_root():

    return "Welcome to the URL shortener API :)"

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
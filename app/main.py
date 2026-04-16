from fastapi import FastAPI

app = FastAPI()

@app.get("/",
         summary="Welcome message",
         description="Simple endpoint to verify the API is running.",
         tags=["meta"]
         )
def root():
    return {"message": "Welcome in Personal Notes"}
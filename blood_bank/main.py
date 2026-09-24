from fastapi import FastAPI


app = FastAPI(title="Blood Bank API")

@app.get("/")
def root():
    return{"message": "the blood bank api is running"}
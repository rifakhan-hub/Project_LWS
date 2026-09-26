from fastapi import FastAPI

from bloodbank import router as bloodbank_router
from bloodbank.database import Base, engine

app = FastAPI(title="Blood Bank API")

Base.metadata.create_all(bind=engine)

app.include_router(bloodbank_router)

@app.get("/")
def root():
    return{"message": "the blood bank api is running"}
from fastapi import FastAPI
from backend.routers.market import router as market_router
from backend.routers.upload import router as upload_router

app = FastAPI(
    title = "A-PQRP API",
    version = "1.0.0"
)    

app.include_router(market_router)
app.include_router(upload_router)

@app.get("/")
def root():
   return{
    "message":"Welcome to A-PQRP API"
    }

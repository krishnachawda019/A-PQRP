from fastapi import FastAPI
from routers.market import router as market_router
from routers.upload import router as upload_router
from routers import profile

app = FastAPI(
    title = "A-PQRP API",
    version = "1.0.0"
)    

app.include_router(market_router)
app.include_router(upload_router)
app.include_router(profile.router)

@app.get("/")
def root():
   return{
    "message":"Welcome to A-PQRP API"
    }

@app.get("/health")
def health():
    return{
        "status" : "Backend is running"
    }




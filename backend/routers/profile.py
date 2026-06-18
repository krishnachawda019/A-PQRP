from fastapi import APIRouter
from backend.services.upload_service import get_dataframe
from backend.services.profile_service import generate_profile

router = APIRouter()

@router.get("/profile")
def profile():
    df = get_dataframe()

    if df is None:
        return{
            "status" : "error",
            "message" : "No dataset uploaded."
        }
    report = generate_profile(df)
    return{
        "status" : "success",
        "profile" : report
    }
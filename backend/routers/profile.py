from fastapi import APIRouter
from backend.services.profile_service import generate_profile
import pandas as pd
import glob
import os

router = APIRouter()


@router.get("/profile")
def profile():

    files = glob.glob("data/*.csv") + glob.glob("data/*.xlsx")

    if not files:
        return {
            "status": "error",
            "message": "No dataset uploaded."
        }

    latest_file = max(files, key=os.path.getmtime)

    if latest_file.endswith(".csv"):
        df = pd.read_csv(latest_file)
    else:
        df = pd.read_excel(latest_file)

    report = generate_profile(df)

    return {
        "status": "success",
        "profile": report
    }

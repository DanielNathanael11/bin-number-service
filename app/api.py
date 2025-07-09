from fastapi import APIRouter, HTTPException
from app.bin_data import BinDataCache

router = APIRouter()

# Shared BIN cache instance
bin_cache = BinDataCache(csv_file="bin_data.csv")

@router.on_event("startup")
def load_data():
    bin_cache.load()

@router.post("/lookup")
def lookup_bins(bins: list[str]):
    """
    Accepts a list of BIN numbers and returns their info.
    """
    results = []
    for bin_number in bins:
        info = bin_cache.get_bin_info(bin_number)
        if info:
            results.append({"bin": bin_number, **info})
        else:
            results.append({"bin": bin_number, "error": "BIN not found"})

    return {"results": results}
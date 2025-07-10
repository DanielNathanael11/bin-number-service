from fastapi import APIRouter, HTTPException
from app.bin_data import BinDataCache

router = APIRouter()

# Shared BIN cache instance
bin_cache = BinDataCache(csv_file="bin_data.csv")

@router.on_event("startup")
def load_data():
    bin_cache.load()

@router.post("/lookup")
def lookup_bin(bin: str):
    """
    Accepts a single BIN number and returns its info with BIN as top-level key.
    """
    result = bin_cache.get_bin_info(bin)
    if result:
        return {
            bin: result  # BIN as top-level key
        }
    else:
        raise HTTPException(status_code=404, detail="BIN not found")

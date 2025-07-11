import pandas as pd

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Paper/Downloads/data-team-production-e09c9a8d87e4.json"  # change this 

from google.cloud import storage
import io

class BinDataCache:
    def __init__(self, gcs_bucket: str, gcs_blob: str):
        self.gcs_bucket = gcs_bucket
        self.gcs_blob = gcs_blob
        self.bin_dict = {}

    def load(self):
        print(f"Loading BIN data from gs://{self.gcs_bucket}/{self.gcs_blob}...")
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.gcs_bucket)
        blob = bucket.blob(self.gcs_blob)

        csv_data = blob.download_as_bytes()  # Download as bytes

        df = pd.read_csv(io.BytesIO(csv_data), dtype={"bin": str})
        df = df.drop_duplicates(subset="bin", keep="first")

        self.bin_dict = df.set_index("bin").to_dict(orient="index")
        print(f"Loaded {len(self.bin_dict)} unique BIN records into memory.")

    def get_bin_info(self, bin_number: str):
        """Return BIN info dict or None if not found"""
        return self.bin_dict.get(bin_number)
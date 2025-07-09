import pandas as pd

class BinDataCache:
    def __init__(self, csv_file: str):
        self.csv_file = csv_file
        self.bin_dict = {}

    def load(self):
        print(f"Loading BIN data from {self.csv_file}...")
        df = pd.read_csv(self.csv_file, dtype={"bin": str})  # 👈 force BIN as string
        df = df.drop_duplicates(subset="bin", keep="first")
        self.bin_dict = df.set_index("bin").to_dict(orient="index")
        print(f"Loaded {len(self.bin_dict)} unique BIN records into memory.")

    def get_bin_info(self, bin_number: str):
        """Return BIN info dict or None if not found"""
        return self.bin_dict.get(bin_number)
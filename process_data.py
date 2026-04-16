import pandas as pd
import glob

files = glob.glob("data/daily_sales_data_*.csv")

dfs = [pd.read_csv(f) for f in files]
df = pd.concat(dfs, ignore_index=True)

df = df[df["product"] == "pink morsel"].copy()

df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)
df["sales"] = df["quantity"] * df["price"]

output = df[["sales", "date", "region"]]

output.to_csv("data/output.csv", index=False)
print(f"Done. {len(output)} rows written to data/output.csv")

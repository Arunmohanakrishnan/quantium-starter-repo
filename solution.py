import pandas as pd
import os

data_folder = "data"
files = [
    os.path.join(data_folder, "daily_sales_data_0.csv"),
    os.path.join(data_folder, "daily_sales_data_1.csv"),
    os.path.join(data_folder, "daily_sales_data_2.csv"),
]

dataframes = [pd.read_csv(f) for f in files]
df = pd.concat(dataframes, ignore_index=True)

df = df[df["product"] == "pink morsel"]

df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)
df["sales"] = df["price"] * df["quantity"]

result = df[["sales", "date", "region"]]

result.to_csv("output.csv", index=False)

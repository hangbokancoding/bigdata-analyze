import pandas as pd

df = pd.read_csv("./output.csv", encoding="utf-8")

jsc = 0

max_len = len(df["code"])
for i in range(0, max_len):
    name = df.iloc[i, 0]
    if name.endswith(".js"):
        jsc += 1

print(f"{jsc}/{max_len}, {jsc/max_len*100}%")

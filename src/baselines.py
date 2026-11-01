import pandas as pd

df = pd.read_csv("data/raw/erco_demand_2025.csv")
df["period"] = pd.to_datetime(df["period"], format="%Y-%m-%dT%H")
df = df.sort_values("period").set_index("period")

real = df["value"]

tabla = pd.DataFrame({
    "real": real,
    "naive_diario": real.shift(24),
    "naive_semanal": real.shift(168),
}).dropna()


def mae(y_real, y_pred):
    return (y_real - y_pred).abs().mean()


def wape(y_real, y_pred):
    return (y_real - y_pred).abs().sum() / y_real.sum() * 100


for nombre in ["naive_diario", "naive_semanal"]:
    print(
        nombre,
        "| MAE:", round(mae(tabla["real"], tabla[nombre])), "MWh",
        "| WAPE:", round(wape(tabla["real"], tabla[nombre]), 2), "%",
    )

errores = tabla[["naive_diario", "naive_semanal"]].sub(tabla["real"], axis=0).abs()
print(errores.groupby(errores.index.month).mean().round(0))
import pandas as pd

df = pd.read_csv("data/raw/erco_demand_2025.csv")
df["period"] = pd.to_datetime(df["period"], format="%Y-%m-%dT%H")
df = df.sort_values("period").set_index("period")
real = df["value"]

tabla = pd.DataFrame({
    "real": real,
    "naive_diario": real.shift(24),
    "naive_semanal": real.shift(168),
})

# Hipótesis: sábado, domingo y lunes se parecen más a su mismo día de la semana pasada
usa_semana = tabla.index.dayofweek.isin([0, 5, 6])  # 0 = lunes
tabla["naive_mixto"] = tabla["naive_diario"].where(~usa_semana, tabla["naive_semanal"])
tabla = tabla.dropna()


def mae(y_real, y_pred):
    return (y_real - y_pred).abs().mean()


def wape(y_real, y_pred):
    return (y_real - y_pred).abs().sum() / y_real.sum() * 100


modelos = ["naive_diario", "naive_semanal", "naive_mixto"]
for nombre in modelos:
    print(
        nombre,
        "| MAE:", round(mae(tabla["real"], tabla[nombre])), "MWh",
        "| WAPE:", round(wape(tabla["real"], tabla[nombre]), 2), "%",
    )

errores = tabla[modelos].sub(tabla["real"], axis=0).abs()
errores.index = errores.index.dayofweek
print(errores.groupby(level=0).mean().round(0))
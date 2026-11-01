import pandas as pd

df = pd.read_csv("data/raw/erco_demand_2025.csv")

# 1. Convertir period de texto a fecha real
df["period"] = pd.to_datetime(df["period"], format="%Y-%m-%dT%H")
df = df.sort_values("period").reset_index(drop=True)

# 2. Calidad básica
print("Filas:", len(df))
print("Duplicados en period:", df["period"].duplicated().sum())
print("Nulos por columna:")
print(df.isna().sum())

# 3. Horas faltantes
esperado = pd.date_range(df["period"].min(), df["period"].max(), freq="h")
faltantes = esperado.difference(df["period"])
print("Horas esperadas:", len(esperado), "| faltantes:", len(faltantes))

# 4. Valores raros
print(df["value"].describe())
print("Valores <= 0:", (df["value"] <= 0).sum())

# 5. Perfil horario: ¿a qué hora baja más la demanda?
perfil = df.groupby(df["period"].dt.hour)["value"].mean().round(0)
print(perfil)
print("Hora de menor demanda promedio:", perfil.idxmin())
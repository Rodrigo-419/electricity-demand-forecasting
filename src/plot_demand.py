import os

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/raw/erco_demand_2025.csv")
df["period"] = pd.to_datetime(df["period"], format="%Y-%m-%dT%H")
df = df.sort_values("period").set_index("period")

fig, axes = plt.subplots(3, 1, figsize=(12, 10))

# 1. Una semana de invierno (lunes 13 a domingo 19 de enero)
semana_invierno = df.loc["2025-01-13":"2025-01-19", "value"]
axes[0].plot(semana_invierno.index, semana_invierno.values)
axes[0].set_title("Una semana de enero")

# 2. Una semana de verano (lunes 14 a domingo 20 de julio)
semana_verano = df.loc["2025-07-14":"2025-07-20", "value"]
axes[1].plot(semana_verano.index, semana_verano.values)
axes[1].set_title("Una semana de julio")

# 3. Demanda promedio por mes
mensual = df["value"].resample("MS").mean()
axes[2].bar(mensual.index.strftime("%b"), mensual.values)
axes[2].set_title("Demanda promedio por mes")

for ax in axes:
    ax.set_ylabel("MWh")

plt.tight_layout()
os.makedirs("reports/figures", exist_ok=True)
plt.savefig("reports/figures/erco_demand_overview.png", dpi=150)
plt.show()
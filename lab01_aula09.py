# AULA 09 — LAB 01
# Sistema Fuzzy de Controle de Ventilador
# ==============================================================================

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import os
from IPython.display import display, Image

# ------------------------------------------------------------------------------
# 1) VARIÁVEIS LINGUÍSTICAS
# ------------------------------------------------------------------------------

temperatura = ctrl.Antecedent(
    np.arange(0, 41, 1),
    "temperatura"
)

velocidade = ctrl.Consequent(
    np.arange(0, 101, 1),
    "velocidade"
)

# ------------------------------------------------------------------------------
# 2) FUNÇÕES DE PERTINÊNCIA
# ------------------------------------------------------------------------------

# Temperatura
temperatura["frio"] = fuzz.trapmf(
    temperatura.universe,
    [0, 0, 15, 25]
)

temperatura["morno"] = fuzz.trimf(
    temperatura.universe,
    [15, 25, 35]
)

temperatura["quente"] = fuzz.trapmf(
    temperatura.universe,
    [25, 35, 40, 40]
)

# Velocidade do ventilador
velocidade["baixa"] = fuzz.trimf(
    velocidade.universe,
    [0, 0, 50]
)

velocidade["media"] = fuzz.trimf(
    velocidade.universe,
    [0, 50, 100]
)

velocidade["alta"] = fuzz.trimf(
    velocidade.universe,
    [50, 100, 100]
)

# ------------------------------------------------------------------------------
# 3) REGRAS FUZZY
# ------------------------------------------------------------------------------

regras = [
    ctrl.Rule(
        temperatura["frio"],
        velocidade["baixa"]
    ),

    ctrl.Rule(
        temperatura["morno"],
        velocidade["media"]
    ),

    ctrl.Rule(
        temperatura["quente"],
        velocidade["alta"]
    )
]

# ------------------------------------------------------------------------------
# 4) SISTEMA DE CONTROLE
# ------------------------------------------------------------------------------

sistema = ctrl.ControlSystem(regras)
ventilador = ctrl.ControlSystemSimulation(sistema)

# ------------------------------------------------------------------------------
# 5) TESTES
# ------------------------------------------------------------------------------

temperaturas_teste = [10, 20, 25, 30, 38]

print("RESULTADOS DO LABORATÓRIO 01")
print("-" * 40)

for temp in temperaturas_teste:

    ventilador.input["temperatura"] = temp
    ventilador.compute()

    resultado = ventilador.output["velocidade"]

    print(
        f"{temp}°C -> ventilador a "
        f"{resultado:.2f}%"
    )

# ------------------------------------------------------------------------------
# 6) GRÁFICOS
# ------------------------------------------------------------------------------

# Garante que a pasta 'imagens' exista
os.makedirs("imagens", exist_ok=True)

temperatura.view()
plt.savefig(
    "imagens/lab01_temperatura.png",
    dpi=150,
    bbox_inches="tight"
)
plt.close()

velocidade.view()
plt.savefig(
    "imagens/lab01_velocidade.png",
    dpi=150,
    bbox_inches="tight"
)
plt.close()

print("\nGráficos salvos em imagens/")

# Exibir imagens diretamente no notebook
print("\n--- EXIBIÇÃO DOS GRÁFICOS ---")
display(Image(filename="imagens/lab01_temperatura.png"))
display(Image(filename="imagens/lab01_velocidade.png"))

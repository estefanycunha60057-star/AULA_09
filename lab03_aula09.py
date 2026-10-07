# AULA 09 — LAB 03
# Sistema Fuzzy para Controle da Potência de um Aquecedor
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ------------------------------------------------------------------------------
# 1) VARIÁVEIS LINGUÍSTICAS
# ------------------------------------------------------------------------------

temperatura = ctrl.Antecedent(
    np.arange(0, 51, 1),
    "temperatura"
)

vazao = ctrl.Antecedent(
    np.arange(0, 21, 1),
    "vazao"
)

potencia = ctrl.Consequent(
    np.arange(0, 101, 1),
    "potencia"
)

# ------------------------------------------------------------------------------
# 2) FUNÇÕES DE PERTINÊNCIA
# ------------------------------------------------------------------------------

# Temperatura da água
temperatura["fria"] = fuzz.trapmf(
    temperatura.universe,
    [0, 0, 10, 20]
)

temperatura["morna"] = fuzz.trimf(
    temperatura.universe,
    [15, 25, 35]
)

temperatura["quente"] = fuzz.trapmf(
    temperatura.universe,
    [30, 40, 50, 50]
)

# Vazão
vazao["baixa"] = fuzz.trapmf(
    vazao.universe,
    [0, 0, 4, 8]
)

vazao["media"] = fuzz.trimf(
    vazao.universe,
    [5, 10, 15]
)

vazao["alta"] = fuzz.trapmf(
    vazao.universe,
    [12, 16, 20, 20]
)

# Potência
potencia["baixa"] = fuzz.trimf(
    potencia.universe,
    [0, 0, 50]
)

potencia["media"] = fuzz.trimf(
    potencia.universe,
    [0, 50, 100]
)

potencia["alta"] = fuzz.trimf(
    potencia.universe,
    [50, 100, 100]
)

# ------------------------------------------------------------------------------
# 3) REGRAS FUZZY
# ------------------------------------------------------------------------------

regras = [

    ctrl.Rule(
        temperatura["fria"] & vazao["baixa"],
        potencia["media"]
    ),

    ctrl.Rule(
        temperatura["fria"] & vazao["media"],
        potencia["alta"]
    ),

    ctrl.Rule(
        temperatura["fria"] & vazao["alta"],
        potencia["alta"]
    ),

    ctrl.Rule(
        temperatura["morna"] & vazao["baixa"],
        potencia["baixa"]
    ),

    ctrl.Rule(
        temperatura["morna"] & vazao["media"],
        potencia["media"]
    ),

    ctrl.Rule(
        temperatura["morna"] & vazao["alta"],
        potencia["alta"]
    ),

    ctrl.Rule(
        temperatura["quente"] | vazao["baixa"],
        potencia["baixa"]
    ),

    ctrl.Rule(
        temperatura["quente"] & vazao["media"],
        potencia["baixa"]
    ),

    ctrl.Rule(
        temperatura["quente"] & vazao["alta"],
        potencia["media"]
    )
]

# ------------------------------------------------------------------------------
# 4) SISTEMA DE CONTROLE
# ------------------------------------------------------------------------------

sistema = ctrl.ControlSystem(regras)
aquecedor = ctrl.ControlSystemSimulation(sistema)

# ------------------------------------------------------------------------------
# 5) TESTES
# ------------------------------------------------------------------------------

testes = [
    (10, 5),
    (20, 10),
    (30, 10),
    (40, 15),
    (5, 18)
]

print("=" * 60)
print("LAB 03 - CONTROLE FUZZY DO AQUECEDOR")
print("=" * 60)

resultados = []

for temperatura_teste, vazao_teste in testes:

    aquecedor.input["temperatura"] = temperatura_teste
    aquecedor.input["vazao"] = vazao_teste

    aquecedor.compute()

    resultado = aquecedor.output["potencia"]

    resultados.append(
        (
            temperatura_teste,
            vazao_teste,
            resultado
        )
    )

    print(
        f"Temperatura: {temperatura_teste:2d}°C | "
        f"Vazão: {vazao_teste:2d} L/min | "
        f"Potência: {resultado:6.2f}%"
    )

# ------------------------------------------------------------------------------
# 6) GRÁFICOS
# ------------------------------------------------------------------------------

temperatura.view()
plt.savefig(
    "imagens/lab03_temperatura.png",
    dpi=150,
    bbox_inches="tight"
)
plt.close()

vazao.view()
plt.savefig(
    "imagens/lab03_vazao.png",
    dpi=150,
    bbox_inches="tight"
)
plt.close()

potencia.view()
plt.savefig(
    "imagens/lab03_potencia.png",
    dpi=150,
    bbox_inches="tight"
)
plt.close()

print("\nGráficos salvos em AULA_09/imagens/")

# AULA 09 — LAB 02
# Sistema Fuzzy de Gorjeta
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import os
from IPython.display import display, Image

# ------------------------------------------------------------------------------
# 1) VARIÁVEIS LINGUÍSTICAS
# ------------------------------------------------------------------------------

servico = ctrl.Antecedent(
    np.arange(0, 10.01, 0.1),
    "servico"
)

comida = ctrl.Antecedent(
    np.arange(0, 10.01, 0.1),
    "comida"
)

gorjeta = ctrl.Consequent(
    np.arange(0, 25.01, 0.5),
    "gorjeta"
)

# ------------------------------------------------------------------------------
# 2) FUNÇÕES DE PERTINÊNCIA
# ------------------------------------------------------------------------------

for var in (servico, comida):

    var["ruim"] = fuzz.trimf(
        var.universe,
        [0, 0, 5]
    )

    var["medio"] = fuzz.trimf(
        var.universe,
        [0, 5, 10]
    )

    var["bom"] = fuzz.trimf(
        var.universe,
        [5, 10, 10]
    )

gorjeta["baixa"] = fuzz.trimf(
    gorjeta.universe,
    [0, 0, 13]
)

gorjeta["media"] = fuzz.trimf(
    gorjeta.universe,
    [0, 13, 25]
)

gorjeta["alta"] = fuzz.trimf(
    gorjeta.universe,
    [13, 25, 25]
)

# ------------------------------------------------------------------------------
# 3) REGRAS FUZZY
# ------------------------------------------------------------------------------

regras = [

    ctrl.Rule(
        servico["ruim"] | comida["ruim"],
        gorjeta["baixa"]
    ),

    ctrl.Rule(
        servico["medio"],
        gorjeta["media"]
    ),

    ctrl.Rule(
        servico["bom"] | comida["bom"],
        gorjeta["alta"]
    )
]

# ------------------------------------------------------------------------------
# 4) SISTEMA
# ------------------------------------------------------------------------------

sistema = ctrl.ControlSystem(regras)
sim = ctrl.ControlSystemSimulation(sistema)

# ------------------------------------------------------------------------------
# 5) ENTRADAS
# ------------------------------------------------------------------------------

def pedir_nota(texto, padrao):

    resposta = input(
        f"{texto} (0-10) [{padrao}]: "
    ).strip()

    if resposta == "":
        return padrao

    valor = float(
        resposta.replace(",", ".")
    )

    if valor < 0 or valor > 10:
        raise ValueError(
            "A nota deve estar entre 0 e 10."
        )

    return valor


servico_valor = pedir_nota(
    "Nota do serviço",
    7
)

comida_valor = pedir_nota(
    "Nota da comida",
    3
)

sim.input["servico"] = servico_valor
sim.input["comida"] = comida_valor

sim.compute()

resultado = sim.output["gorjeta"]

print()
print(
    f"Serviço: {servico_valor:.1f}"
)
print(
    f"Comida: {comida_valor:.1f}"
)
print(
    f"=> Gorjeta sugerida: {resultado:.2f}%"
)

# ------------------------------------------------------------------------------
# 6) GRÁFICOS
# ------------------------------------------------------------------------------

# Garante que a pasta 'imagens' exista
os.makedirs("imagens", exist_ok=True)

servico.view()
plt.savefig(
    "imagens/lab02_servico.png",
    dpi=150,
    bbox_inches="tight"
)
plt.close()

comida.view()
plt.savefig(
    "imagens/lab02_comida.png",
    dpi=150,
    bbox_inches="tight"
)
plt.close()

gorjeta.view(sim=sim)
plt.savefig(
    "imagens/lab02_gorjeta.png",
    dpi=150,
    bbox_inches="tight"
)
plt.close()

print("\nGráficos salvos em imagens/")

# Exibir imagens diretamente no notebook
print("\n--- EXIBIÇÃO DOS GRÁFICOS ---")
display(Image(filename="imagens/lab02_servico.png"))
display(Image(filename="imagens/lab02_comida.png"))
display(Image(filename="imagens/lab02_gorjeta.png"))

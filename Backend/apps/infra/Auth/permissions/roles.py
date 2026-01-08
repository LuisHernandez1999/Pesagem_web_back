"""
Defina aqui, de forma declarativa, o que cada grupo pode fazer.
Operações válidas: "view", "add", "change", "delete".
Modelos no formato "<app_label>.<ModelName>".

Ajuste os nomes dos modelos abaixo conforme existirem no seu app:
  - pesagem_.Pesagem
  - pesagem_.Soltura
  - pesagem_.Vistoria
"""

ROLES = {
    "admin": {
        "*": ["view", "add", "change", "delete"], 
    },
    "sac": {
        "pesagem_.Pesagem":  ["view", "add", "change"],  
        "pesagem_.Soltura":  ["view"],                   
        "pesagem_.Apoio":  ["view"],
        "pesagem_.Averiguacao":  ["view"], 
        "pesagem_.Colaborador":  ["view", "add", "change"], 
        "pesagem_.Cooperativa":  ["view", "add", "change"], 
        "pesagem_.MetaBatida":  ["view", "add", "change"], 
        "pesagem_.Rota":  ["view"], 
        "pesagem_.Setor":  ["view"], 
        "pesagem_.SubstituicaoVeiculo":  ["view"], 
        "pesagem_.Veiculo":  ["view", "add", "change"],  
    },
    "torre": {
        "pesagem_.Soltura":  ["view", "add", "change"],               
        "pesagem_.Apoio":  ["view", "add", "change"],
        "pesagem_.Averiguacao":  ["view"], 
        "pesagem_.Colaborador":  ["view", "add", "change"], 
        "pesagem_.Rota":  ["view", "add", "change"], 
        "pesagem_.Setor":  ["view", "add", "change"], 
        "pesagem_.SubstituicaoVeiculo":  ["view", "add", "change"], 
        "pesagem_.Veiculo":  ["view", "add", "change"],  
    },
    "default": {
        "pesagem_.Soltura":  ["view"],                   
    },
}

# Opcional: dar "view_*" para todos os outros apps (além de pesagem_) a certos grupos
GIVE_VIEW_ON_OTHER_APPS_TO = {"admin", "sac", "torre"}  # "default" fica restrito
SYSTEM_APPS = {"admin", "auth", "contenttypes", "sessions", "messages", "staticfiles"}
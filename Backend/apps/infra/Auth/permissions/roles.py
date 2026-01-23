ROLES = {
    "admin": {
        "*": ["view", "add", "change", "delete"],
    },
    "default": {
        "veiculo.veiculo": ["view", "add", "change", "delete"],
        "cooperativa.cooperativa": ["view", "add", "change", "delete"],
        "colaborador.colaborador": ["view", "add", "change", "delete"],
        "pesagem.pesagem": ["view", "add", "change", "delete"],
        "os.ordemservico": ["view", "add", "change", "delete"],
        "movimentacao.movimentacao": ["view", "add", "change", "delete"],
         
    },
}

GIVE_VIEW_ON_OTHER_APPS_TO = {"admin"}
SYSTEM_APPS = {
    "admin",
    "auth",
    "contenttypes",
    "sessions",
    "messages",
    "staticfiles",
}

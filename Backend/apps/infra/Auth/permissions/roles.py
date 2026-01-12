ROLES = {
    "admin": {
        "*": ["view", "add", "change", "delete"],
    },
    "default": {
        "pesagem.veiculo": ["view", "add", "change", "delete"],
         "pesagem.cooperativa": ["view", "add", "change", "delete"],
         "pesagem.colaborador": ["view", "add", "change", "delete"],
         "pesagem.pesagem": ["view", "add", "change", "delete"],
         
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

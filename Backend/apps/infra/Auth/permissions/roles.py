ROLES = {
    "admin": {
        "*": ["view", "add", "change", "delete"],
    },
    "default": {
        "pesagem.veiculo": ["view"],
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

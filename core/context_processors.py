import os


# Váriaveis padrões dos templates
def default_context(request):
    return {
        "css": [],
        "js": [],
        "py_vars": {},
        "jsVars": {},
        "plugins": {},
        "forms": {},
    }


# Menu da aplicação
def menu_options(request):
    menu = {
        "home": {
            "label": "Página Inicial",
            "url": "internal_home",
            "icon": "fas fa-home",
            "permission": None,
        },
        "colaboradores": {
            "label": "Colaboradores",
            "url": "colaborador_web:colaborador-list",
            "icon": "fas fa-users",
            "permission": ["colaboradores.view_colaborador"],
        },
        "framework": {
            "label": "Framework",
            "url": "admin:index",
            "icon": "fas fa-code",
            "permission": "is_staff",
        },
    }

    def has_permission(user, perm):
        if perm == "is_staff":
            return user.is_staff
        elif isinstance(perm, list):
            return any(user.has_perm(p) for p in perm)
        elif perm is None:
            return True
        else:
            return user.has_perm(perm)

    # Verifica as permissões
    for key, item in menu.items():
        item["permission"] = has_permission(request.user, item.get("permission"))

        if "children" in item:
            for child in item["children"]:
                child["permission"] = has_permission(
                    request.user, child.get("permission")
                )

    return {"menu_options": menu}


def env_vars(_):
    return {"SENTRY_JS_URL": os.getenv("SENTRY_JS_URL", "")}

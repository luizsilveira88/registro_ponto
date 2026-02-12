# Django
from django.contrib.auth import get_permission_codename


class BasePolicy:
    """
    Classe base para policies Django.
    - Cria métodos `can_<action>` dinamicamente a partir das permissões do modelo.
    - Permite sobrescrita manual (ex: `can_change` customizado).
    - Inclui método `get_actions()` para listar permissões disponíveis dinamicamente.
    """

    def __init__(self, user, obj=None):
        self.user = user
        self.obj = obj
        self.model = self.Meta.model
        self.app_label = self.model._meta.app_label
        self.model_name = self.model._meta.model_name

    # Permissões dinâmicas
    def has_perm(self, codename):
        """
        Checa permissão completa (ex: app_label.codename).
        """
        return self.user.has_perm(f"{self.app_label}.{codename}")

    def __getattr__(self, name):
        """
        Gera dinamicamente métodos can_<action>()
        com base nas permissões reais do modelo.
        """
        if name.startswith("can_"):
            action = name.replace("can_", "")
            perms = self._get_model_permissions()

            target_codename = f"{action}_{self.model_name}"
            if target_codename in perms:
                # Cria dinamicamente o método
                def method(codename=target_codename):
                    return self.has_perm(codename)

                return method

        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )

    def _get_model_permissions(self):
        """
        Retorna os codenames das permissões do modelo, incluindo as padrão e customizadas.
        """
        opts = self.model._meta
        default = [
            get_permission_codename(a, opts)
            for a in ["add", "change", "delete", "view"]
        ]
        custom = [p[0] for p in getattr(opts, "permissions", [])]
        return set(default + custom)

    # Listagem dinâmica de ações disponíveis
    def get_actions(self):
        """
        Retorna uma lista com os nomes das ações (`can_*`)
        que o usuário tem permissão para executar.
        """
        actions = []
        perms = self._get_model_permissions()

        # Cria lista de possíveis métodos (ex: can_view, can_add, can_manage)
        possible_methods = [f"can_{perm.split('_')[0]}" for perm in perms]

        # Verifica dinamicamente cada método
        for method_name in possible_methods:
            method = getattr(self, method_name, None)
            if callable(method):
                try:
                    if method():  # executa a checagem
                        actions.append(f"{method_name}_{self.model_name}")
                except Exception:
                    # Evita quebrar caso a policy customizada exija obj específico
                    continue

        return actions

    class Meta:
        model = None

from rest_framework import status


class ColaboradorException(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "Erro no colaborador"

    def __init__(self, message=None):
        self.message = message or self.default_message


class ColaboradorNotFound(ColaboradorException):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = "Colaborador não encontrado"


class CNPJServiceError(ColaboradorException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_message = "Erro ao consultar CNPJ"

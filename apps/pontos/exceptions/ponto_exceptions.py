from rest_framework import status


class PontoException(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "Erro no ponto"

    def __init__(self, message=None):
        self.message = message or self.default_message


class PontoNotFound(PontoException):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = "Ponto não encontrado"

from rest_framework import status


class BiometriaException(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "Erro na biometria"

    def __init__(self, message=None):
        self.message = message or self.default_message


class BiometriaNoFace(BiometriaException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "Nenhuma rosto detectado"


class BiometriaMultipleFaces(BiometriaException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "Mais de um rosto detectado"


class BiometriaEncodingError(BiometriaException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "Não foi possível gerar o encoding facial"

# Python
import uuid
import face_recognition
import numpy as np

# Django
from django.contrib.contenttypes.models import ContentType

# Models
from ..models.biometria import Biometria

# Services
from core.services.auditoria_svc import create_auditoria

from trabalhador.models import biometria


class BiometriaException(Exception):
    pass


def create_biometria(colaborador_id: int, file) -> None:
    """
    Cadastro biométrico do usuário
    """
    image = face_recognition.load_image_file(file)
    face_locations = face_recognition.face_locations(image, model="hog")

    if not face_locations:
        raise BiometriaException("Nenhum rosto detectado na imagem")

    if len(face_locations) > 1:
        raise BiometriaException("Mais de um rosto detectado")

    encodings = face_recognition.face_encodings(image, face_locations)
    if not encodings:
        raise BiometriaException("Não foi possível gerar o encoding facial")

    encoding = encodings[0]

    # Inativar outras biometrias do usuário
    Biometria.objects.filter(colaborador__id=colaborador_id).update(
        posicao=Biometria.Posicao.INATIVO
    )

    # Salvar nova biometria
    biometria = Biometria.objects.create(
        colaborador__id=colaborador_id,
        encoding=encoding.tobytes(),
    )

    return biometria


def check_biometria(colaborador_id: int, file, tolerance: float = 0.48) -> dict:
    """
    Verifica biometria e retorna score
    """
    biometria = Biometria.objects.get(
        colaborador__id=colaborador_id,
        posicao=Biometria.Posicao.ATIVO,
    )

    known_encoding = np.frombuffer(biometria.encoding, dtype=np.float64)

    candidate_image = face_recognition.load_image_file(file)
    candidate_face_locations = face_recognition.face_locations(candidate_image)

    if not candidate_face_locations:
        raise BiometriaException("Nenhum rosto detectado na imagem")

    if len(candidate_face_locations) > 1:
        raise BiometriaException("Mais de um rosto detectado")

    candidate_encodings = face_recognition.face_encodings(
        candidate_image, known_face_locations=candidate_face_locations
    )

    if not candidate_encodings:
        raise BiometriaException("Não foi possível gerar o encoding facial")

    candidate_encoding = candidate_encodings[0]

    distance = face_recognition.face_distance([known_encoding], candidate_encoding)[0]

    return {
        "match": distance <= tolerance,
        "distance": float(distance),
        "tolerance": tolerance,
    }

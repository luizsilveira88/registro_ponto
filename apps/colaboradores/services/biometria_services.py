# Python
import face_recognition
import numpy as np

# Models
from ..models.biometria import Biometria
from ..models.colaborador import Colaborador

# Exception
from ..exceptions.biometria_exceptions import (
    BiometriaMultipleFaces,
    BiometriaNoFace,
    BiometriaEncodingError,
)


def create_biometria(colaborador: Colaborador, file) -> None:
    """
    Cadastro biométrico do usuário
    """
    image = face_recognition.load_image_file(file)
    face_locations = face_recognition.face_locations(image, model="hog")

    if not face_locations:
        raise BiometriaNoFace

    if len(face_locations) > 1:
        raise BiometriaMultipleFaces

    encodings = face_recognition.face_encodings(image, face_locations)
    if not encodings:
        raise BiometriaEncodingError

    encoding = encodings[0]

    # Inativar outras biometrias do usuário
    Biometria.objects.filter(colaborador=colaborador).update(
        posicao=Biometria.Posicao.INATIVO
    )

    # Salvar nova biometria
    biometria = Biometria.objects.create(
        colaborador=colaborador,
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
        raise BiometriaNoFace

    if len(candidate_face_locations) > 1:
        raise BiometriaMultipleFaces

    candidate_encodings = face_recognition.face_encodings(
        candidate_image, known_face_locations=candidate_face_locations
    )

    if not candidate_encodings:
        raise BiometriaEncodingError

    candidate_encoding = candidate_encodings[0]

    distance = face_recognition.face_distance([known_encoding], candidate_encoding)[0]

    return {
        "match": distance <= tolerance,
        "distance": float(distance),
        "tolerance": tolerance,
    }

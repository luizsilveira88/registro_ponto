# Python
import datetime

# Django
from django.conf import settings


# Recupera os arquivos necessários para um plugin
def get_plugins_files(plugin_list):
    return {
        name: settings.TEMPLATES_PLUGINS[name]
        for name in plugin_list
        if name in settings.TEMPLATES_PLUGINS
    }


def get_month_range(year, month):
    """
    Retorna um intervalo de datas de um mês, baseado no ano e mês informados.
    o Retorno será o primeiro dia do mês e o primeiro dia do próximo mês.
    Deve ser utilizado em combinação com gte e lt no filtro de datas.
    """
    begin = datetime.date(year, month, 1)
    if month == 12:
        end = datetime.date(year + 1, 1, 1)
    else:
        end = datetime.date(year, month + 1, 1)
    return begin, end


def validate_year_month(year, month):
    """
    Valida os parâmetros year e month.
    Retorna uma tupla (year, month) como inteiros.
    Lança ValueError se inválido.
    """
    if year is None or month is None:
        raise ValueError("Parâmetros 'year' e 'month' são obrigatórios")

    try:
        year = int(year)
        month = int(month)
    except (ValueError, TypeError):
        raise ValueError("Parâmetros devem ser números inteiros")

    if month < 1 or month > 12:
        raise ValueError("Mês inválido")

    return year, month

from django.db import models


class Mensagem(models.Model):
    """ Modelo de uma Mensagem no banco de dados

    Attributes:
        id: uma UUID que identifica unicamente uma mensagem.
        data: data em formato YYYY-mm-dd
        status: o status da mensagem
        texto: o texto da mensagem

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = models.DateField()
    status = models.CharField(max_length=200)
    texto = models.TextField()


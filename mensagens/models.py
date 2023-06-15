import uuid
import json
import jsonschema
from datetime import date
from jsonschema import Draft202012Validator
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

    def fromJSON(jsonData):
        """Deserializa uma string JSON em uma Mensagem

            Args:
                jsonData: uma mensagen serializada como string JSON.
            Returns:
                Uma instância de Mensagem deserializada da string JSON.
            Raises:
                ValueError: caso a string JSON fornecida não seja uma mensagem
                válida.
                Exception: caso ocorra um erro ao deserializar a string JSON.
        """
        mensagemSchema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": {
                "data": {"type": "string", "format": "date"},
                "status": {"type": "string"},
                "texto": {"type": "string"},
                "id": {"type": "number"},
            },
            "required": ["data", "status", "texto"],
        }
        try:
            message = json.loads(jsonData)
            jsonschema.validate(
                message, mensagemSchema,
                format_checker=Draft202012Validator.FORMAT_CHECKER)
        except jsonschema.exceptions.ValidationError as error:
            raise ValueError(
                "Os dados JSON não são uma mensagem válida: {} ".format(
                    error.message))
        except Exception as error:
            raise Exception(
                "A tentativa de validar os dados JSON falhou: {}".format(
                    error))
        messageDate = date.fromisoformat(message["data"])
        newMessage = Mensagem(
            data=messageDate, status=message["status"],
            texto=message["texto"])
        if "id" in message:
            newMessage.id = uuid.UUID(int=message["id"])
        return newMessage

    def toJSON(self):
        """Serializa a mensagem para formato de string JSON"""

        mensagem = {
            "id": self.id.int,
            "data": self.data.strftime("%Y-%m-%d"),
            "status": self.status,
            "texto": self.texto
        }
        return json.dumps(mensagem)

    def __str__(self):
        return self.toJSON()

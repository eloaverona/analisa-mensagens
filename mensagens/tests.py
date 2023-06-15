from django.test import TestCase
import json
from .models import Mensagem
from datetime import date
from jsonschema.exceptions import ValidationError


class MensagemModelTests(TestCase):
    def test_mensagem_deserializes_well_formed_json(self):
        """Verifica se o método Mensagem.fromJSON deserializa corretamente
        uma string JSON formatada corretamente.
        """
        dados = """{"data": "2001-02-11", "status": "Em espera", "texto":
                "Estou bem chateado. Você poderia nos mandar seus dados?"}"""
        mensagem = Mensagem.fromJSON(dados)
        self.assertEqual(mensagem.data, date.fromisoformat("2001-02-11"))
        self.assertEqual(mensagem.status, "Em espera")
        self.assertEqual(
            mensagem.texto,
            "Estou bem chateado. Você poderia nos mandar seus dados?")

    def test_mensagem_raises_error_bad_formed_json(self):
        """Verifica que o método Mensagem.fromJSON levanta um erro caso
        o input é uma string JSON mal formatada
        """
        dados = """{"data": "Não sou uma data", "status":
            "Em espera", "texto":
            "Estou bem chateado. Você poderia nos mandar seus dados?"}"""
        try:
            Mensagem.fromJSON(dados)
        except ValidationError:
            pass
        except ValueError:
            pass
        except Exception:
            pass
        else:
            self.fail("Erro inesperado aconteceu")

    def test_mensagem_serializes_well_formed_json(self):
        """Verifica se o método toJSON serializa corretamente
        uma string.
        """
        mensagem = Mensagem(
            data=date.fromisoformat("2001-02-11"), status="Em Espera",
            texto="Estou bem chateado. Gostaria de fazer um pedido.")
        dadosJSON = mensagem.toJSON()
        mensagemJSON = json.loads(dadosJSON)
        self.assertEqual(
            mensagemJSON["data"], "2001-02-11")
        self.assertEqual(mensagemJSON["status"], "Em Espera")
        self.assertEqual(
            mensagemJSON["texto"],
            "Estou bem chateado. Gostaria de fazer um pedido.")

    def test_mensagem_serializes_deserializes(self):
        """Verifica que uma mensagem serializado método toJSON, pode ser
        deserializada pelo método fromJSON.
        """
        mensagemOriginal = Mensagem(
            data=date.fromisoformat("2001-02-11"), status="Em Espera",
            texto="Estou bem chateado. Gostaria de fazer um pedido.")
        dadosJSON = mensagemOriginal.toJSON()
        mensagemDeserializada = Mensagem.fromJSON(dadosJSON)
        self.assertEqual(
            mensagemOriginal, mensagemDeserializada)


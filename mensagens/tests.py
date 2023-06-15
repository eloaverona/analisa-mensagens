from django.test import TestCase
import json
from .models import Mensagem
from datetime import date
from jsonschema.exceptions import ValidationError
import mensagens.database_handler as dbHandler


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


class DatabaseHandlerTests(TestCase):
    def test_insert_mensagem_success(self):
        """Verifica que é possível adicionar uma mensagem no banco de dados
        com sucesso
        """
        dados = """{"data": "2001-02-11", "status": "Em espera", "texto":
                "Estou bem chateado. Você poderia nos mandar seus dados?"}"""
        dbHandler.insertMessage(dados)
        mensagens = list(Mensagem.objects.all())
        self.assertEqual(1, len(mensagens))
        mensagem = mensagens[0]
        self.assertEqual(mensagem.data, date.fromisoformat("2001-02-11"))
        self.assertEqual(mensagem.status, "Em espera")
        self.assertEqual(
            mensagem.texto,
            "Estou bem chateado. Você poderia nos mandar seus dados?")

    def test_fetch_mensagem_success(self):
        """Verifica que o método fetchMessage retorna a mensagem esperada"""
        self.seed_mock_data_to_database()
        mensagens = list(Mensagem.objects.all())
        self.assertEqual(3, len(mensagens))
        mensagemID = mensagens[0].id
        mensagemJSON = dbHandler.fetchMessage(mensagemID)
        mensagem = json.loads(mensagemJSON)
        self.assertEqual(mensagem["id"], mensagens[0].id.int)
        self.assertEqual(
            mensagem["data"],
            mensagens[0].data.strftime("%Y-%m-%d"))
        self.assertEqual(mensagem["status"], mensagens[0].status)
        self.assertEqual(mensagem["texto"], mensagens[0].texto)

    def test_fetch_mensagem_wrong_id(self):
        """Verifica que o método fetchMessage retorna um erro se uma id que não
            existe no banco de dados for fornecida
        """
        self.seed_mock_data_to_database()
        mensagens = list(Mensagem.objects.all())
        self.assertEqual(3, len(mensagens))
        try:
            dbHandler.fetchMessage(14545)
        except Exception:
            pass
        else:
            self.fail("Erro inesperado aconteceu")

    def test_list_mensagens_success(self):
        """Verifica que o método listMessages retorna uma lista de mensagens
        em formato string de JSON
        """
        self.seed_mock_data_to_database()
        mensagens = list(Mensagem.objects.all())
        self.assertEqual(3, len(mensagens))
        mensagensJSON = dbHandler.listMessages()
        mensagensDB = json.loads(mensagensJSON)
        self.assertEqual(3, len(mensagensDB))

        self.assertEqual(mensagensDB[0]["id"], mensagens[0].id.int)
        self.assertEqual(
            mensagensDB[0]["data"],
            mensagens[0].data.strftime("%Y-%m-%d"))
        self.assertEqual(
            mensagensDB[0]["status"],
            mensagens[0].status)
        self.assertEqual(
            mensagensDB[0]["texto"],
            mensagens[0].texto)

        self.assertEqual(mensagensDB[1]["id"], mensagens[1].id.int)
        self.assertEqual(
            mensagensDB[1]["data"],
            mensagens[1].data.strftime("%Y-%m-%d"))
        self.assertEqual(
            mensagensDB[1]["status"],
            mensagens[1].status)
        self.assertEqual(
            mensagensDB[1]["texto"],
            mensagens[1].texto)

        self.assertEqual(mensagensDB[2]["id"], mensagens[2].id.int)
        self.assertEqual(
            mensagensDB[2]["data"],
            mensagens[2].data.strftime("%Y-%m-%d"))
        self.assertEqual(
            mensagensDB[2]["status"],
            mensagens[2].status)
        self.assertEqual(
            mensagensDB[2]["texto"],
            mensagens[2].texto)

    def test_update_mensagem_success(self):
        """Verifica que o método updateMessage atualiza a mensagem esperada"""
        self.seed_mock_data_to_database()
        mensagens = list(Mensagem.objects.all())
        self.assertEqual(3, len(mensagens))
        mensagemID = mensagens[0].id
        newStatus = "Atualizado"
        newText = "Mensagem atualizada"
        updatedMessage = Mensagem(
            id=mensagemID,
            data=mensagens[0].data,
            status=newStatus,
            texto=newText)
        jsonMessage = updatedMessage.toJSON()
        dbHandler.updateMessage(mensagemID, jsonMessage)

        mensagem = Mensagem.objects.get(pk=mensagemID)
        self.assertEqual(mensagem.id, mensagens[0].id)
        self.assertEqual(mensagem.data, mensagens[0].data)
        self.assertNotEqual(mensagem.status, mensagens[0].status)
        self.assertNotEqual(mensagem.texto, mensagens[0].texto)

        self.assertEqual(mensagem.status, newStatus)
        self.assertEqual(mensagem.texto, newText)

    def test_delete_mensagem_success(self):
        """Verifica que o método deleteMessage deleta a mensagem esperada"""
        self.seed_mock_data_to_database()
        mensagens = list(Mensagem.objects.all())
        self.assertEqual(3, len(mensagens))
        mensagemID = mensagens[0].id
        mensagemJSON = dbHandler.deleteMessage(mensagemID)
        self.assertEqual(2, len(list(Mensagem.objects.all())))
        mensagem = json.loads(mensagemJSON)
        self.assertEqual(mensagem["id"], mensagens[0].id.int)
        self.assertEqual(
            mensagem["data"],
            mensagens[0].data.strftime("%Y-%m-%d"))
        self.assertEqual(mensagem["status"], mensagens[0].status)
        self.assertEqual(mensagem["texto"], mensagens[0].texto)

    def seed_mock_data_to_database(self):
        mensagem1 = Mensagem(
            data="2022-01-24", status="Em Espera",
            texto="Estou bem chateado. Gostaria de fazer um pedido.")

        mensagem2 = Mensagem(
            data="2021-02-23", status="Aberto",
            texto="""Gostaria de fazer um pedido. Preciso que resolvam um
            problema.""")

        mensagem3 = Mensagem(
            data="2020-05-19", status="Fechado",
            texto="ótima empresa. Olá, como vai?")

        mensagem1.save()
        mensagem2.save()
        mensagem3.save()

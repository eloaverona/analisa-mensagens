from django.test import TestCase
from django.urls import reverse
import json
from .models import Mensagem
from datetime import date
from jsonschema.exceptions import ValidationError
import mensagens.database_handler as dbHandler
from mensagens.message_processor import MessageProcessor


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
    def setUp(self):
        Mensagem.objects.all().delete()

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

    def test_insert_mensagem_success(self):
        """Verifica que é possível adicionar uma mensagem no banco de dados
        com sucesso
        """
        messagesCount = len(list(Mensagem.objects.all()))
        dados = """{"data": "2001-02-11", "status": "Em espera", "texto":
                "Estou bem chateado. Você poderia nos mandar seus dados?"}"""
        dbHandler.insertMessage(dados)
        mensagens = list(Mensagem.objects.all())
        self.assertEqual(messagesCount+1, len(mensagens))
        mensagem = mensagens[messagesCount]
        self.assertEqual(mensagem.data, date.fromisoformat("2001-02-11"))
        self.assertEqual(mensagem.status, "Em espera")
        self.assertEqual(
            mensagem.texto,
            "Estou bem chateado. Você poderia nos mandar seus dados?")

    def test_fetch_mensagem_success(self):
        """Verifica que o método fetchMessage retorna a mensagem esperada"""
        mensagens = list(Mensagem.objects.all())
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
        mensagens = list(Mensagem.objects.all())
        mensagensJSON = dbHandler.listMessages()
        mensagensDB = json.loads(mensagensJSON)
        self.assertEqual(len(mensagens), len(mensagensDB))
        for i in range(len(mensagens)):
            self.assertEqual(mensagensDB[i]["id"], mensagens[i].id.int)
            self.assertEqual(
                mensagensDB[i]["data"],
                mensagens[i].data.strftime("%Y-%m-%d"))
            self.assertEqual(
                mensagensDB[i]["status"],
                mensagens[i].status)
            self.assertEqual(
                mensagensDB[i]["texto"],
                mensagens[i].texto)

    def test_update_mensagem_success(self):
        """Verifica que o método updateMessage atualiza a mensagem esperada"""
        mensagens = list(Mensagem.objects.all())
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
        mensagens = list(Mensagem.objects.all())
        mensagensCount = len(mensagens)
        mensagemID = mensagens[0].id
        mensagemJSON = dbHandler.deleteMessage(mensagemID)
        self.assertEqual(mensagensCount-1, len(list(Mensagem.objects.all())))
        mensagem = json.loads(mensagemJSON)
        self.assertEqual(mensagem["id"], mensagens[0].id.int)
        self.assertEqual(
            mensagem["data"],
            mensagens[0].data.strftime("%Y-%m-%d"))
        self.assertEqual(mensagem["status"], mensagens[0].status)
        self.assertEqual(mensagem["texto"], mensagens[0].texto)


class ListMessagesViewsTest(TestCase):
    def test_list_mensagens_view_success(self):
        """Avalia se o enpoint /mensagens retorna uma lista de mensagens como
        esperado
        """
        response = self.client.get(reverse("mensagens:list"))
        self.assertEquals(response.status_code, 200)

        messages = list(Mensagem.objects.all())

        responseMessages = json.loads(response.content)
        self.assertEqual(len(messages), len(responseMessages))
        for i in range(len(messages)):
            self.assertEqual(responseMessages[i]["id"], messages[i].id.int)
            self.assertEqual(
                responseMessages[i]["data"],
                messages[i].data.strftime("%Y-%m-%d"))
            self.assertEqual(
                responseMessages[i]["status"],
                messages[i].status)
            self.assertEqual(
                responseMessages[i]["texto"],
                messages[i].texto)

    def test_list_empty_mensagens_success(self):
        """Avalia caso o banco de dados esteja vazio, o endpont /mensagens
        retorna uma lista vazia
        """
        Mensagem.objects.all().delete()
        response = self.client.get(reverse("mensagens:list"))
        self.assertEquals(response.status_code, 200)
        responseMessages = json.loads(response.content)
        self.assertEquals(0, len(responseMessages))
class MessageProcessorTest(TestCase):
    def test_positive_sentiment_test(self):
        """Testa se o algoritmo de análise de sentimento avalia uma frase
        positiva corretamente"""
        text = "Sou uma frase feliz, feliz, feliz"
        messageProcessor = MessageProcessor()
        score = messageProcessor.analyseSentiment(text)
        self.assertTrue(score > 0)

    def test_negative_sentiment_test(self):
        """Testa se o algoritmo de análise de sentimento avalia uma frase
        negativa corretamente"""
        text = "Sou uma frase triste, triste, triste"
        messageProcessor = MessageProcessor()
        score = messageProcessor.analyseSentiment(text)
        self.assertTrue(score < 0)

    def test_messages_sentiment_process(self):
        """Testa que o método analyseMessagesSentiment retorna os resultados
            esperados
        """
        dataMensagem = "2000-5-23"
        statusMensagem = "Em Espera"
        positiveMessage = Mensagem(
            data=dataMensagem, status=statusMensagem,
            texto="Sou uma frase feliz feliz feliz")
        negativeMessage = Mensagem(
            data=dataMensagem,
            status=statusMensagem,
            texto="Sou uma frase triste")
        neutralMessage = Mensagem(
            data=dataMensagem,
            status=statusMensagem,
            texto="Sou uma frase")
        messageProcessor = MessageProcessor()
        analysedMessages = json.loads(
            messageProcessor.processMessagesSentiment(
                [positiveMessage, negativeMessage, neutralMessage]))
        self.assertTrue(analysedMessages[0]["valorSentimento"] > 0)
        self.assertEquals(analysedMessages[0]["sentimento"], "positivo")
        self.assertTrue(analysedMessages[1]["valorSentimento"] < 0)
        self.assertEquals(analysedMessages[1]["sentimento"], "negativo")
        self.assertTrue(analysedMessages[2]["valorSentimento"] == 0)
        self.assertEquals(analysedMessages[2]["sentimento"], "neutro")


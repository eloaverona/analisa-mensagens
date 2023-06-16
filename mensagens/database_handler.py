from .models import Mensagem


def insertMessage(newMessage):
    """Adiciona uma nova mensagem ao banco de dados

    Args:
        newMessage: A mensagem a ser adicionada serializada no formato de
        string JSON
    Raises:
        Exception: Um erro ocorreu ao deserializar o JSON ou ao se comunicar
        com o banco de dados
    """
    try:
        message = Mensagem.fromJSON(newMessage)
    except Exception as error:
        raise Exception(
            "Falha ao criar mensagem. Verifique o formato do input: {}"
            .format(error))
    try:
        message.save()
    except Exception as error:
        raise Exception(
            "Erro ao adicionar mensagem no banco de dados: {}".format(error))


def fetchMessage(messageID):
    """Pega uma mensagem específica no banco de dados

    Args:
        messageID: a id única da mensagem
    Returns:
        A mensagem serializada em formato de string JSON
    Raises:
        Exception: uma mensagem com a message_id fornecida não existe ou caso
     houver uma falha ao acessar o banco de dados
    """
    try:
        message = Mensagem.objects.get(pk=messageID)
    except Mensagem.DoesNotExist:
        raise Exception("Messagem com id {} não existe".format(messageID))
    except Exception as error:
        raise Exception("Erro ao acessar o banco de dados: {}".format(error))
    return message.toJSON()


def listMessages(jsonFormat=True):
    """Retorna uma lista com todas as mensagens no banco de dados
    Args:
        jsonFormat: Se True, retorna as mensagens em formato JSON
        se False, retorna as mensagens como um objeto Mensage.
        default = True
    Returns:
        Uma lista com as mensagens
    Raises:
        Exception: caso houver uma falha ao acessar o banco de dados
    """
    try:
        messages = list(Mensagem.objects.all())
        if jsonFormat:
            messages = list(map(lambda m: m.toJSON(), messages))
            messages = ", ".join(messages)
            messages = "[" + messages + "]"
    except Exception as error:
        raise Exception("Erro ao acessar o banco de dados: {}".format(error))
    return messages


def deleteMessage(messageID):
    """Deleta uma mensagem específica do banco de dados

    Args:
        messageID: a id única da mensagem a ser deletada
    Returns:
        A mensagem que foi deletada serializada em formato de string JSON
    Raises:
        Exception: uma mensagem com a message_id fornecida não existe ou caso
        houver uma falha ao acessar o banco de dados
    """

    try:
        message = Mensagem.objects.get(pk=messageID)
        jsonEncodedMessage = message.toJSON()
        message.delete()
    except Mensagem.DoesNotExist:
        raise Exception("Messagem com id {} não existe".format(messageID))
    except Exception as error:
        raise Exception("Erro ao acessar o banco de dados: {}".format(error))
    return jsonEncodedMessage


def updateMessage(messageID, jsonData):
    """Atualiza uma mensagem específica no banco de dados

    Args:
        messageID: a id única da mensagem a ser atualizada
        jsonData: a mensagem com os dados atualizados serializados em formato
        de string JSON
    Returns:
        A mensagem serializada em formato de string JSON
    Raises:
        Exception: uma mensagem com a message_id fornecida não existe ou caso
        houver uma falha ao acessar o banco de dados
    """
    try:
        message = Mensagem.objects.get(pk=messageID)
        updatedMessage = Mensagem.fromJSON(jsonData)
        message.status = updatedMessage.status
        message.texto = updatedMessage.texto
        message.data = updatedMessage.data
        message.save()
    except Mensagem.DoesNotExist:
        raise Exception("Messagem com id {} não existe".format(messageID))
    except ValueError as error:
        raise Exception(
            "Os dados do JSON não são uma mensagem válida: {}".format(error))
    except Exception as error:
        raise Exception("Erro ao acessar o banco de dados: {}".format(error))

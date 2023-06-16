from django.http import HttpResponse
from . import database_handler as dbHandler
import json
import logging


def listMessages(request):
    """Lida com requests para o path "/"
        args:
            request: o request em HTTP
        returns:
            Responde em HTTP com uma lista de mensagens em formato JSON
    """
    response = HttpResponse()
    response.headers["Content-Type"] = "application/json"
    try:
        messages = dbHandler.listMessages()
        response.write(messages)
    except Exception as error:
        logging.error(error)
        errorMessage = json.dumps({
            "error": {
                "code": 500,
                "message": "Um erro interno ao sistema aconteceu." +
                " Tente novamente mais tarde"
            }
        })
        response.write(errorMessage)
        response.status_code = 500
        return response
    return response

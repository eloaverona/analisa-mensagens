from django.urls import path
from . import views

app_name = "mensagens"

urlpatterns = [
    path(
        "",
        views.listMessages,
        name="list"),
    path(
        "sentiment/",
        views.analyseMessagesSentiment,
        name="sentiment"),
    path(
        "sentiment/count/",
        views.countMessagesSentiment,
        name="sentimentCount")]

import json
import string


class MessageProcessor():
    '''Processador de texto

    Implementa um algoritmo básico de análise de sentimentos de um texto
    em português.

    Attributes:
        wordPolarity: dicionário extraído do SentiLex-PT-02. Atribui uma
        polaridade a palabvras da língua portuguesa. As polaridades podem ser
        negativo (-1), neutro (0), positivo (1)
    '''
    wordPolarityFile = "mensagens/assets/pt_word_sentiment_polarity.json"
    wordPolarities = {}

    def __init__(self):
        with open(self.wordPolarityFile) as source:
            polarities = source.read()
            self.wordPolarities = json.loads(polarities)

    def analyseSentiment(self, text):
        '''Implementa um algoritimo básico de análise de sentimento de textos

        args:
            text: Texto em língua portuguesa a ser analisado
        returns:
            um valor int que pode ser um número positivo, 0 ou negativo.
            Números positivos indicam que o texto provavelmente é positivo,
            números negativos indicam que o texto provavelmente é negativo,
            0 indica que o texto provavelmente é neutro. O valor absoluto
            a intensidade do sentimento que o texto expressa.
        '''
        words = text.split()
        textSentiment = 0
        for word in words:
            striptedWord = word.translate(
                str.maketrans('', '', string.punctuation)).lower()
            wordPolarity = 0
            if striptedWord in self.wordPolarities:
                wordPolarity = self.wordPolarities[striptedWord]
            textSentiment = textSentiment + wordPolarity
        return textSentiment

    def processMessagesSentiment(self, messages):
        """ Analisa o texto de mensagens e retorna uma avaliação se essas
        mensagens são positivas, negativas, ou neutras.

        args:
            messages: uma lista de Mensagens
        returns:
            uma lista de mensagens e sua avaliação de sentimentos em
            formato JSON
        """
        try:
            analysedMessages = []
            for message in messages:
                sentimentScore = self.analyseSentiment(message.texto)
                sentiment = "neutro"
                if sentimentScore > 0:
                    sentiment = "positivo"
                elif sentimentScore < 0:
                    sentiment = "negativo"
                analysedMessages.append({
                    "id": message.id.int,
                    "status": message.status,
                    "data": str(message.data),
                    "texto": message.texto,
                    "valorSentimento": sentimentScore,
                    "sentimento": sentiment,
                })
            messagesJson = json.dumps(analysedMessages)
        except Exception as error:
            raise Exception("Ocorreu um erro enquanto processava mensagens." +
                            "{}".format(error))

        return messagesJson

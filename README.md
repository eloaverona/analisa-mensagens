# Mensagens

### Sobre

Esse projeto foi construindo em python, usando a framework django.

### Executar o servidor 

#### Via docker

1. Clone o repositório e mude para o diretório do projeto
```
$ git clone https://github.com/eloaverona/analisa_mensagens.git

$ cd analisa_mensagens 
```  
2. Rode o projeto dentro de um container docker via o comando
 
```
$ docker-compose up 
```

3. O servidor estará disponível em `localhost:8000/mensagens`
4. Para rodar os testes 
```
$ sudo docker container exec analisa_mensagens_django-app_1 python manage.py test mensagens
```
#### Execute localmente

Pré-requisitos: 
- Python 3

1. Clone o repositório e mude para o diretório do projeto

```
$ git clone https://github.com/eloaverona/analisa_mensagens.git

$ cd analisa_mensagens 

```
2- Instale via pip as dependências necessárias:
```
$ pip install -r requirements.txt
```
3. Para rodar o servidor no `localhost:8000/mensagens`
```
$ python manage.py runserver
```
4. Para rodar testes execute:

```
python manage.py test mensagens
```
### API

```yaml
paths:
  /mensagens:
    get:
      summary: Retorna uma lista de mensagen
      responses:
        200:
	  description: Sucesso ao conseguir as mensagens
          schema:
              type: array
              items: 
                Mensagem:
                  properties:
                    id:
                      type: integer
		    status:
	              type: string
                    data:
                      type: string
                    texto:
                      type: string
	500: 
         description: Um erro aconteceu
         schema:
	   properties: 
              error:
		properties:
		  code: integer
		  message: string

  /mensagens/sentiment:
    get:
      summary: Retorna uma lista de mensagens com análise de sentimento
      responses:
        200:
	  description: Sucesso ao conseguir as mensagens
          schema:
              type: array
              items: 
                Mensagem:
                  properties:
                    id:
                      type: integer
		    status:
	              type: string
                    data:
                      type: string
                    texto:
                      type: string
		    valorSentimento:
		      type: integer
		      description: um número positivo, zero ou negativo que indica se o sentimento da mensagem é positivo, neutro ou negativo.
                    sentimento:
		      type: string
	500: 
         description: Um erro aconteceu
         schema:
	   properties: 
              error:
		properties:
		  code: integer
		  message: string
	 
		
  /mensagens/sentiment/count:
    get:
      summary: Retorna uma conta de quantas mensagens positivas, negativas e neutras tem no banco de dados
      responses:
        200:
	  description: Sucesso ao conseguir a conta
          schema:
              properties:
		mensagensPositivas: 
	    	  type: integer
		mensagensNegativas:
		  type: integer
		mensagensNeutras:
		  type: integer
	500: 
         description: Um erro aconteceu
         schema:
	   properties: 
              error:
		properties:
		  code: integer
		  message: string
```

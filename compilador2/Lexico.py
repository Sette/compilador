
from Fila import Fila
from Token import Token


def getToken(w, lista, linha):
    for i in lista:
        if w == lista[i] or w in lista[i]:
            token = Token(w, i, linha)
            # print(token.cadeia)
            return token
    return None

class Lexico():
    def __init__(self,entrada):
        self.entrada = entrada
    def analisar(self):
        lista = {'Reservada': ["if", "then", "while", "do", "write",\
            "read", "else", "begin", "end","real","var","procedure","integer","program"], \
                 'Operador':["(", ")", "*", "/", "+", "-", ":=", "=",\
            "<>", ">=", ">", "<","<=",":", "," , ".",";", "$"]}

        tokens = Fila()

        fd = open(self.entrada, 'r')
        stream = fd.readlines()

        fila_entrada = Fila()

        for k in stream:
            for w in k:
                fila_entrada.add(w)

        teste = fila_entrada.peek()
        linha = 1
        while not fila_entrada.vazia() and fila_entrada.peek() != "." :
            elemento = fila_entrada.remove()
            if elemento == "\n":
                linha+=1
            if elemento in ["(", ")", "*", "+", "-", "=", ",",";","$"]:
                token = getToken(elemento, lista, linha)
                tokens.add(token)

            elif elemento == ":":
                if fila_entrada.peek() == "=":
                    elemento += fila_entrada.remove()
                token = getToken(elemento, lista, linha)
                tokens.add(token)
            elif elemento == ">":
                if fila_entrada.peek() == "=":
                    elemento = fila_entrada.remove()
                token = getToken(elemento, lista, linha)
                tokens.add(token)
            elif elemento == "<":
                if fila_entrada.peek() == "=":
                    elemento = fila_entrada.remove()
                elif fila_entrada.peek() == ">":
                    elemento = fila_entrada.remove()

                token = getToken(elemento, lista, linha)
                tokens.add(token)
            elif elemento == "{":
                while fila_entrada.peek() != "}":
                    elemento += fila_entrada.remove()

                elemento += fila_entrada.remove()
                #token = Token(elemento,"Comentário",linha)
                #tokens.add(token)
            elif elemento == "/":
                if fila_entrada.peek() == "*":
                    elemento += fila_entrada.remove()
                    while not (fila_entrada.peek() == "*" and fila_entrada.peek_2() == "/"):
                        elemento += fila_entrada.remove()

                    elemento += fila_entrada.remove()
                    elemento += fila_entrada.remove()
                    #token = Token(elemento, "Comentário", linha)
                    #tokens.add(token)

                else:
                    token = getToken(elemento, lista, linha)
                    tokens.add(token)
            elif elemento.isalpha():
                while fila_entrada.peek().isalpha() or fila_entrada.peek().isnumeric() :
                    elemento += fila_entrada.remove()
                #token = buscatabela(elemento)
                token = getToken(elemento, lista, linha)
                if not token:
                    token = Token(elemento,"Identificador",linha)
                tokens.add(token)
            elif elemento.isnumeric():
                while fila_entrada.peek().isnumeric():
                    elemento += fila_entrada.remove()
                if(fila_entrada.peek() == "."):
                    elemento += fila_entrada.remove()
                    while fila_entrada.peek().isnumeric():
                        elemento += fila_entrada.remove()
                    token = Token(elemento, "Real", linha)
                else:
                    token = Token(elemento, "Inteiro", linha)
                tokens.add(token)

            elif elemento != " " and elemento != "\n" and elemento != "\t":
                raise NameError("Token não identificado %s na linha: %s" % (elemento,linha))


        elemento = fila_entrada.remove()
        if elemento == ".":
            token = Token(elemento, "Finalizador", linha)
            tokens.add(token)
        if not fila_entrada.vazia():
            NameError("Código não finalizado")


        return tokens

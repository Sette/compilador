
from Fila import Fila

def getToken(w,lista,linha):
    for i in lista:
        if w == lista[i] or w in lista[i]:
            token = [w, i,linha]
            return token
    return None

lista = {'Reservada': ["if", "then", "while", "do", "write",\
    "read", "else", "begin", "end","real","var","procedure","integer","program"], \
         'Operador':["(", ")", "*", "/", "+", "-", ":=", "=",\
    "<>", ">=", ">", "<","<=",":", "," , ".",";", "$"]}

tokens = []

def main():
    fd = open('erro2', 'r')
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
            tokens.append(token)

        elif elemento == ":":
            if fila_entrada.peek() == "=":
                elemento = fila_entrada.remove()
            token = getToken(elemento, lista, linha)
            tokens.append(token)
        elif elemento == ">":
            if fila_entrada.peek() == "=":
                elemento = fila_entrada.remove()
            token = getToken(elemento, lista, linha)
            tokens.append(token)
        elif elemento == "<":
            if fila_entrada.peek() == "=":
                elemento = fila_entrada.remove()
            elif fila_entrada.peek() == ">":
                elemento = fila_entrada.remove()

            token = getToken(elemento, lista, linha)
            tokens.append(token)
        elif elemento == "{":
            while fila_entrada.peek() != "}":
                elemento += fila_entrada.remove()

            elemento += fila_entrada.remove()
            token = [elemento,"Comentário",linha]
            tokens.append(token)
        elif elemento == "/":
            if fila_entrada.peek() == "*":
                elemento += fila_entrada.remove()
                while not (fila_entrada.peek() == "*" and fila_entrada.peek_2() == "/"):
                    elemento += fila_entrada.remove()

                elemento += fila_entrada.remove()
                elemento += fila_entrada.remove()
                token = [elemento, "Comentário", linha]
                tokens.append(token)

            else:
                token = getToken(elemento, lista, linha)
                tokens.append(token)
        elif elemento.isalpha():
            while fila_entrada.peek().isalpha() or fila_entrada.peek().isnumeric() :
                elemento += fila_entrada.remove()
            #token = buscatabela(elemento)
            token = getToken(elemento, lista, linha)
            if not token:
                token = [elemento,"Identificador",linha]
            tokens.append(token)
        elif elemento.isnumeric():
            while fila_entrada.peek().isnumeric():
                elemento += fila_entrada.remove()
            if(fila_entrada.peek() == "."):
                elemento += fila_entrada.remove()
                while fila_entrada.peek().isnumeric():
                    elemento += fila_entrada.remove()
                token = [elemento, "Real", linha]
            else:
                token = [elemento, "Inteiro", linha]
            tokens.append(token)

        elif elemento != " " and elemento != "\n" and elemento != "\t":
            raise NameError("Token não identificado %s na linha: %s" % (elemento,linha))


    elemento = fila_entrada.remove()
    if elemento == ".":
        token = [elemento, "FInalizador", linha]
        tokens.append(token)
    if not fila_entrada.vazia():
        NameError("Código não finalizado")

    print(tokens)
if __name__=="__main__":
    main()

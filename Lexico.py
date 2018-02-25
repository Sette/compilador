
import csv

class Lexico():
    def __init__(self):

        fd = open('arqFonte_old', 'r')
        stream = fd.readlines()

        lista = {'Palavra reservada': ['var', ':', ',', 'integer', 'real', ';', 'if', 'then', 'id'], 'Atribuicao': ':=',
                 "Operadores": ['+']}
        tokens_split = ['+', ',', ':', ':=', ';']

        tokens = []

        cont = 1
        for k in stream:
            for w in k.split():
                token = getToken(w, cont, lista)
                aux = ""
                if not token:
                    if ('+' in w or ':=' in w or ',' in w or ':' in w or ';' in w):
                        for i in w:
                            if (i not in tokens_split):
                                aux += i
                            else:
                                token = getToken(aux, cont, lista)
                                if token:
                                    tokens.append(token)
                                else:
                                    if (aux.isalpha()):
                                        token = [aux, "id", cont]
                                        tokens.append(token)
                                    else:
                                        print("Erro léxico, token desconhecido: ", aux, " linha: ", cont)
                                        return None
                                token = getToken(i, cont, lista)

                                if token:
                                    tokens.append(token)
                                else:
                                    if (i.isalpha()):
                                        token = [i, "id", cont]
                                        tokens.append(token)
                                    else:
                                        print("Erro léxico, token desconhecido: ", i, " linha: ", cont)
                                aux = ""
                        if aux:
                            token = getToken(aux, cont, lista)
                            if not token:
                                if (aux.isalpha()):
                                    token = [aux, "id", cont]
                                else:
                                    print("Erro léxico, token desconhecido: ", aux, " linha: ", cont)
                            tokens.append(token)
                    else:
                        if (w.isalpha()):
                            token = [w, "id", cont]
                            tokens.append(token)
                        else:
                            print("Erro léxico, token desconhecido: ", w, " linha: ", cont)
                else:
                    tokens.append(token)
            cont += 1

        print(tokens)

        arquivoOutput = 'arquivo.csv'

        with open(arquivoOutput, 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter='-', quoting=csv.QUOTE_MINIMAL)
            for linha in tokens:
                spamwriter.writerow(linha)

        fd.close



def getToken(w,line,lista):
    for i in lista:
        if w == lista[i] or w in lista[i]:
            token = [w, i,line]
            return token

    return None

from Lexico import Lexico

import csv

ts = {}

tokens = []

tipo_esperado = ""

E_esq = ""
E_dir = ""
T_esq = ""
T_dir = ""
R_esq = ""
R_dir = ""
R1_esq = ""
R1_dir = ""
S1_quad = 1
prox = 2

temps = [0]

def geraTemp():
    global temps
    cont = 0
    for temp in temps:
        if temp == 0:
            temps[cont] = 1
            temps.append(0)
            break
        cont += 1
    return "T"+str(cont+1)

def get_ts(token):
    global ts
    get_dict = ts.get(token)

    if (get_dict == None):
        raise NameError("Variavel não encontrada: %s" % token.get("Cadeia"))

    return get_dict


def Z(entrada):
    entrada = I(entrada)
    entrada = S(entrada)
    return entrada


def I(entrada):
    elemento = entrada[0]
    if elemento[0] == "var":
        entrada = getNext(entrada)
        entrada = D(entrada)
        return entrada
    else:
        raise NameError("Erro Sintático. Esperava-se 'var' na linha", entrada[0][2])


def D(entrada):
    entrada = L(entrada)
    elemento = entrada[0]
    if (elemento[0] == ":"):
        entrada = getNext(entrada)
        entrada = K(entrada)
        entrada = O(entrada)
    else:
        raise NameError("Erro Sintático. Esperava-se ':' na linha", entrada[0][2])

    return entrada


def L(entrada):
    elemento = entrada
    if (entrada[0][1] == "id"):
        insert_ts = {entrada[0][0]: {"Cadeia": entrada[0][0], "Token": entrada[0][1], "Categoria": "var", \
                                     "Endereço": entrada[0][2]}}
        tokens.append(entrada[0][0])
        ts.update(insert_ts)
        entrada = getNext(entrada)
        entrada = X(entrada)
    else:
        raise NameError("Erro Sintático. Esperava-se uma variável na linha", entrada[0][2])

    return entrada


def X(entrada):
    if (entrada[0][0] == ","):
        entrada = getNext(entrada)
        entrada = L(entrada)

    return entrada


def K(entrada):
    if (entrada[0][0] == "real" or entrada[0][0] == "integer"):
        for token in tokens:
            try:
                update_dict = get_ts(token)
            except:
                raise NameError("Variavel não encontrada: %s" % token.get("Cadeia"))
            update_dict.update({"Tipo": entrada[0][0]})

        tokens.clear()
        entrada = getNext(entrada)
        return entrada
    else:
        raise NameError("Erro Sintático. Esperava-se tipo de variavel na linha", entrada[0][2])


def O(entrada):
    if (entrada[0][0] == ";"):
        entrada = getNext(entrada)
        entrada = D(entrada)
    return entrada


def S(entrada):
    global tipo_esperado, E_esq, E_dir, S1_quad, prox, R_dir
    try:
        elemento = entrada[0]
    except:
        return entrada
    if (entrada[0][1] == "id"):
        try:
            get_dict = get_ts(entrada[0][0])
        except:
            raise NameError("Variável não declarada")

        E_esq = entrada[0][0]

        tipo_esperado = get_dict.get("Tipo")
        entrada = getNext(entrada)
        if (entrada[0][0] == ":="):
            entrada = getNext(entrada)
            entrada = E(entrada)
            print("[:=", E_esq, E_dir,"]")
        else:
            raise NameError("Erro Sintático, esperava-se ':=' na linha", entrada[0][2])

        return entrada
    elif (entrada[0][0] == "if"):
        entrada = getNext(entrada)
        entrada = E(entrada)
        if (entrada[0][0] == "then"):
            tipo_esperado = ""
            tipo_esperado = ""
            entrada = getNext(entrada)
            S1_quad = prox
            prox += 1
            entrada = S(entrada)
            print(S1_quad,"JF", R_dir, prox)

            return entrada
        else:
            raise NameError("Erro Sintático. Esperava-se 'then'")
    else:
        raise \
            NameError("Erro Sintático. Esperava-se um id ou 'if' na linha", entrada[0][2])

    return entrada


def E(entrada):
    global R_esq, T_dir, E_dir, R_dir
    entrada = T(entrada)
    R_esq = T_dir
    entrada = R(entrada)
    E_dir = R_dir
    return entrada


def T(entrada):
    global tipo_esperado, T_dir
    if (entrada[0][1] == "id"):
        try:
            get_dict = get_ts(entrada[0][0])
        except:
            raise NameError("Variavel não encontrada: %s" % entrada[0][0])
        T_dir = entrada[0][0]
        if (tipo_esperado == ""):
            tipo_esperado = get_dict.get("Tipo")
        else:
            tipo_atual = get_dict.get("Tipo")
            if (not tipo_esperado == tipo_atual):
                raise NameError("Tipo de varíavel incompatível, esperava-se tipo: %s, linha: %s, variavel: %s" \
                                % (tipo_esperado, str(entrada[0][2]), str(entrada[0][0])))

        entrada = getNext(entrada)
        return entrada
    else:
        raise \
            NameError("Erro Sintático. Esperava-se uma variavel na linha", entrada[0][2])


def R(entrada):
    global R1_esq, T_dir, R_dir,R1_dir,R_esq
    try:
        value = entrada[0][0]
    except:
        R_dir = R_esq
        return entrada

    if (value == "+"):
        entrada = getNext(entrada)
        entrada = T(entrada)
        R1_esq = T_dir
        entrada = R(entrada)
        R_dir = geraTemp()
        print("[+", R_esq, R1_esq, R_dir,"]")
        return entrada
    else:
        R_dir = R_esq
        return entrada



def getNext(entrada):
    try:
        entrada.remove(entrada[0])
    except:
        raise \
            NameError("Erro Sintático. Código não finalizado, linha", entrada[0][2])

    return entrada


def main():
    lexico = Lexico()

    with open('arquivo.csv', 'r') as ficheiro:
        reader = csv.reader(ficheiro, delimiter='-', quoting=csv.QUOTE_NONE)
        tokens = [linha for linha in reader]

    entrada = Z(tokens)

    if (entrada):
        raise \
            NameError("Erro sintático: ", entrada)


if __name__ == "__main__":
    main()
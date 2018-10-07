
from Token import Token

from Fila import Fila



tokens = []

tipo_esperado = ""

prox = 0

escopos = [{}]

escopo_atual = 0

variaveis = []

parametros = []


def get_ts(token):
    global escopos, escopo_atual
    ts = escopos[escopo_atual]
    get_dict = ts.get(token)

    if (get_dict == None):
        raise NameError("Variavel não encontrada: %s" % token.get("Cadeia"))

    return get_dict


class Sintatico():
    def __init__(self,tokens):
        self.tokens = tokens

    def analisar(self):
        global escopos, escopo_atual
        self.S()
        for escopo in escopos:
            print("---------------------------------------")
            print(escopo)


    def programa(self):
        global escopos, escopo_atual
        elemento = self.tokens.remove()
        if not (elemento.cadeia == "program"):
            raise NameError("Erro Sintático. Esperava-se 'program' na linha", elemento.linha)
        else:
            elemento = self.tokens.remove()
            if not (elemento.classe == "Identificador"):
                raise NameError("Erro Sintático. Esperava-se um identificador na linha", elemento.linha)
            else:
                insert_ts = {elemento.cadeia: {"Cadeia": elemento.cadeia, "Token": elemento.classe, "Categoria": "program", \
                                             "Endereço": elemento.linha}}
                tokens.append(elemento.cadeia)

                ts = escopos[escopo_atual]

                ts.update(insert_ts)
                self.corpo()
                elemento = self.tokens.remove()
                if elemento.cadeia == ".":
                    print("AEE")


    def S(self):
        self.programa()

    def corpo(self):
        global escopos, escopo_atual
        self.dc()
        elemento = self.tokens.remove()
        if not (elemento.cadeia=="begin"):
            raise NameError("Erro Sintático. Esperava-se 'begin' na linha", elemento.linha)
        else:
            self.comandos()
            elemento = self.tokens.remove()
            if not (elemento.cadeia == "end"):
                raise NameError("Erro Sintático. Esperava-se 'end' na linha", elemento.linha)



    def dc(self):
        global escopos, escopo_atual
        elemento = self.tokens.peek()
        if elemento.cadeia == "var":
            self.dc_v()
            self.mais_dc()
        elif elemento.cadeia == "procedure":
            self.dc_p()
            self.mais_dc()

    def mais_dc(self):
        elemento = self.tokens.peek()
        if (elemento.cadeia == ";"):
            self.tokens.remove()
            self.dc()

    def dc_v(self):
        elemento = self.tokens.remove()
        if not (elemento.cadeia == "var"):
            raise NameError("Erro Sintático. Esperava-se 'var' na linha", elemento.linha)
        else:
            self.variaveis()
            elemento = self.tokens.remove()
            if not (elemento.cadeia == ":"):
                raise NameError("Erro Sintático. Esperava-se ':' na linha", elemento.linha)
            else:
                self.tipo_var()
                parametros.clear()

    def tipo_var(self):
        global escopos, escopo_atual
        elemento = self.tokens.remove()
        if not (elemento.cadeia == "real" or elemento.cadeia == "integer"):
            raise NameError("Erro Sintático. Esperava-se um tipo de variavel na linha", elemento.linha)
        else:
            if not variaveis:
                print("OPA")
            else:
                ts = escopos[escopo_atual]
                for variavel in variaveis:
                    insert_ts = variavel[1]
                    get_dict = insert_ts.get(variavel[0])
                    get_dict.update({"Tipo":elemento.cadeia})
                    ts.update(insert_ts)
                    parametros.append(insert_ts)
                variaveis.clear()



    def variaveis(self):
        global variaveis
        global escopos, escopo_atual, procedures
        elemento = self.tokens.remove()
        if not (elemento.classe == "Identificador"):
            raise NameError("Erro Sintático. Esperava-se um identificador na linha", elemento.linha)
        else:
            insert_ts = {elemento.cadeia: {"Cadeia": elemento.cadeia, "Token": elemento.classe, "Categoria": "var", \
                                           "Endereço": elemento.linha}}
            variaveis.append((elemento.cadeia,insert_ts))
            tokens.append(elemento.cadeia)
            #ts.update(insert_ts)
            self.mais_var()

    def mais_var(self):
        elemento = self.tokens.peek()
        if elemento.cadeia == ",":
            self.tokens.remove()
            self.variaveis()

    def dc_p(self):
        global escopos, escopo_atual, procedures
        elemento = self.tokens.remove()
        if not (elemento.cadeia == "procedure"):
            raise NameError("Erro Sintático. Esperava-se 'procedure' na linha", elemento.linha)
        else:
            elemento = self.tokens.remove()
            if not (elemento.classe == "Identificador"):
                raise NameError("Erro Sintático. Esperava-se um identificador na linha", elemento.linha)
            else:
                insert_ts = {elemento.cadeia: {"Cadeia": elemento.cadeia, "Token": elemento.classe, "Categoria": "procedure", \
                                               "Endereço": elemento.linha}}
                tokens.append(elemento.cadeia)
                procedures.append(insert_ts)

                ts = escopos[escopo_atual]

                #ts.update(insert_ts)

                escopo_atual+=1

                escopos.append({})

                self.parametros()
                self.corpo_p()

    def parametros(self):

        elemento = self.tokens.peek()
        if not (elemento.cadeia == "("):
            raise NameError("Erro Sintático. Esperava-se '(' na linha", elemento.linha)
        else:
            self.tokens.remove()
            self.lista_par()
            elemento = self.tokens.remove()
            if not (elemento.cadeia == ")"):
                raise NameError("Erro Sintático. Esperava-se ')' na linha", elemento.linha)


    def lista_par(self):
        global escopos, escopo_atual, procedures
        global procedures
        self.variaveis()
        elemento = self.tokens.remove()
        if not (elemento.cadeia == ":"):
            raise NameError("Erro Sintático. Esperava-se ':' linha", elemento.linha)
        else:
            self.tipo_var()

            self.mais_par()

    def mais_par(self):
        elemento = self.tokens.peek()
        if elemento.cadeia == ";":
           self.tokens.remove()
           self.lista_par()

    def corpo_p(self):
        global escopos,escopo_atual
        self.dc_loc()
        elemento = self.tokens.remove()
        if not (elemento.cadeia == "begin"):
            raise NameError("Erro Sintático. Esperava-se 'begin' na linha", elemento.linha)
        else:
            self.comandos()
            elemento = self.tokens.remove()
            if not (elemento.cadeia == "end"):
                raise NameError("Erro Sintático. Esperava-se 'end' na linha", elemento.linha)
            else:
                escopo_atual-=1

    def dc_loc(self):
        elemento =  self.tokens.peek()
        if elemento.cadeia == "var":
            self.dc_v()
            self.mais_dcloc()


    def mais_dcloc(self):
        elemento = self.tokens.peek()
        if elemento.cadeia == ";":
            self.tokens.remove()
            self.dc_loc()


    def lista_arg(self):
        elemento = self.tokens.peek()
        if (elemento.cadeia == "("):
            self.tokens.remove()
            self.argumentos()
            elemento = self.tokens.peek()
            if not (elemento.cadeia == ")"):
                raise NameError("Erro Sintático. Esperava-se ')' na linha", elemento.linha)
            else:
                self.tokens.remove()

    def argumentos(self):
        elemento = self.tokens.remove()
        if elemento.classe == "Identificador":
            try:
                get_dict = get_ts(elemento.cadeia)
            except:
                raise NameError("Variavel não encontrada: %s" % elemento.cadeia)
            self.mais_ident()
        else:
            raise NameError("Erro Sintático. Esperava-se um identificador na linha", elemento.linha)

    def mais_ident(self):
        elemento = self.tokens.peek()
        if elemento.cadeia == ";":
            self.tokens.remove()
            self.argumentos()

    def pfalsa(self):
        elemento = self.tokens.peek()
        if elemento.cadeia == "else":
            self.tokens.remove()
            self.comandos()

    def comandos(self):
        self.comando()
        self.mais_comandos()

    def mais_comandos(self):
        elemento = self.tokens.peek()
        if elemento.cadeia == ";":
            self.tokens.remove()
            self.comandos()

    def comando(self):
        elemento = self.tokens.remove()
        if (elemento.cadeia == "read") or (elemento.cadeia == "write"):
            elemento = self.tokens.remove()
            if elemento.cadeia == "(":
                self.variaveis()
                elemento = self.tokens.remove()
                if not (elemento.cadeia == ")"):
                    raise NameError("Erro Sintático. Esperava-se ')' na linha", elemento.linha)
            else:
                raise NameError("Erro Sintático. Esperava-se ')' na linha", elemento.linha)

        elif (elemento.cadeia == "while"):
            self.condicao()
            if not (self.tokens.remove().cadeia == "do"):
                raise NameError("Erro Sintático. Esperava-se 'do' na linha", elemento.linha)
            else:
                self.comandos()
                if not (self.tokens.remove().cadeia == "$"):
                    raise NameError("Erro Sintático. Esperava-se '$' na linha", elemento.linha)

        elif(elemento.cadeia == "if"):
            self.condicao()
            if not (self.tokens.remove().cadeia == "then"):
                raise NameError("Erro Sintático. Esperava-se 'then' na linha", elemento.linha)
            else:
                self.comandos()
                self.pfalsa()
                if not (self.tokens.remove().cadeia == "$"):
                    raise NameError("Erro Sintático. Esperava-se '$' na linha", elemento.linha)
        elif(elemento.classe == "Identificador"):
            try:
                get_dict = get_ts(elemento.cadeia)
            except:
                raise NameError("Variavel não encontrada: %s" % elemento.cadeia)
            self.restoident()

        else:
            raise NameError("Erro Sintático. Esperava-se algo na linha", elemento.linha)


    def restoident(self):
        if self.tokens.peek().cadeia == ":=":
            self.tokens.remove()
            self.expressao()
        else:
            self.lista_arg()

    def condicao(self):
        elemento = self.tokens.peek()
        if elemento.cadeia == "(":
            self.tokens.remove()
            self.expressao()
            self.relacao()
            self.expressao()
            elemento = self.tokens.peek()
            if not elemento.cadeia == ")":
                raise NameError("Erro Sintático. Esperava-se algo na linha", elemento.linha)
            else:
                self.tokens.remove()

    def relacao(self):
        elemento = self.tokens.remove()
        relacoes = ["=","<>",">=","<=",">","<"]
        if elemento.cadeia not in relacoes:
            raise NameError("Erro Sintático. Esperava-se relacional na linha", elemento.linha)


    def expressao(self):
        self.termo()
        self.outros_termos()

    def op_un(self):
        if self.tokens.peek().cadeia in ["+","-"]:
            self.tokens.remove()

    def outros_termos(self):
        if self.tokens.peek().cadeia in ["+","-"]:
            self.tokens.remove()
            self.termo()
            self.outros_termos()

    def op_ad(self):
        elemento = self.tokens.peek()
        if elemento.cadeia in ["+","-"]:
            self.tokens.remove()
        else:
            raise NameError("Erro Sintático. Esperava-se relacional na linha", elemento.linha)


    def termo(self):
        self.op_un()
        self.fator()
        self.mais_fatores()

    def mais_fatores(self):
        elemento = self.tokens.peek()
        if elemento.cadeia in ["*", "/"]:
            self.tokens.remove()
            self.fator()
            self.mais_fatores()

    def op_mul(self):
        elemento = self.tokens.peek()
        if elemento.cadeia in ["*","/"]:
            self.tokens.remove()
        else:
            raise NameError("Erro Sintático. Esperava-se relacional na linha", elemento.linha)

    def fator(self):
        elemento = self.tokens.peek()
        classes = ["Identificador", "Real", "Inteiro"]
        if not elemento.classe in classes:

            self.expressao()
        else:
            if elemento.classe == "Identificador":
                try:
                    get_dict = get_ts(elemento.cadeia)
                except:
                    raise NameError("Variavel não encontrada: %s" % elemento.cadeia)
            self.tokens.remove()

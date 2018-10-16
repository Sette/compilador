from Token import Token

from Fila import Fila



tokens = []

tipo_esperado = ""

prox = 0

escopos = {"main":{}}

escopo_atual = "main"

variaveis = []

parametros = []

procedures = []

argumentos = []

verifica_tipo = ""

comando = False



def get_ts(token):
    global escopos, escopo_atual
    ts = escopos.get(escopo_atual)
    get_dict = ts.get(token)

    if (get_dict == None):
        raise NameError("Variavel não encontrada: %s" % token)

    return get_dict


class Sintatico():
    def __init__(self,tokens):
        self.tokens = tokens

    def analisar(self):
        global escopos, escopo_atual
        self.S()

        for name in escopos:

            print(name)
            for escopo in escopos[name]:
                print(escopos[name][escopo])
            print("---------------------------------------")



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
                insert_ts = {elemento.cadeia: {"Cadeia": elemento.cadeia, "Token": elemento.classe, \
                                             "Endereço": elemento.linha,"Categoria":"program"}}
                tokens.append(elemento.cadeia)

                ts = escopos.get(escopo_atual)

                ts.update(insert_ts)
                self.corpo()
                elemento = self.tokens.remove()
                if elemento.cadeia == ".":
                    print("Código finalizado")


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


    def tipo_var(self):
        global escopos, escopo_atual, parametros
        elemento = self.tokens.remove()
        if not (elemento.cadeia == "real" or elemento.cadeia == "integer"):
            raise NameError("Erro Sintático. Esperava-se um tipo de variavel na linha", elemento.linha)
        else:
            if variaveis:
                ts = escopos.get(escopo_atual)
                for variavel in variaveis:
                    if variavel[0] not in parametros:
                        insert_ts = variavel[1]
                        get_dict = insert_ts.get(variavel[0])

                        if (ts.get(variavel[0])):
                            raise NameError("Erro na redeclaração de variaveis", variavel[0])

                        get_dict.update({"Tipo":elemento.cadeia})
                        ts.update(insert_ts)
                if procedures:
                    parametros.append(elemento.cadeia)

                variaveis.clear()



    def variaveis(self):
        global variaveis, parametros
        global escopos, escopo_atual, procedures, comando
        elemento = self.tokens.remove()
        if not (elemento.classe == "Identificador"):
            raise NameError("Erro Sintático. Esperava-se um identificador na linha", elemento.linha)
        else:
            insert_ts = {elemento.cadeia: {"Cadeia": elemento.cadeia, "Token": elemento.classe,  \
                                           "Endereço": elemento.linha,"Categoria": "var",}}


            variaveis.append((elemento.cadeia,insert_ts))
            tokens.append(elemento.cadeia)


            if procedures:
                parametros.append(elemento.cadeia)



            #ts.update(insert_ts)
            self.mais_var()

    def mais_var(self):
        elemento = self.tokens.peek()
        if elemento.cadeia == ",":
            self.tokens.remove()
            self.variaveis()

    def dc_p(self):
        global escopos, escopo_atual, procedures, prox_escopo
        elemento = self.tokens.remove()
        if not (elemento.cadeia == "procedure"):
            raise NameError("Erro Sintático. Esperava-se 'procedure' na linha", elemento.linha)
        else:
            elemento = self.tokens.remove()
            if not (elemento.classe == "Identificador"):
                raise NameError("Erro Sintático. Esperava-se um identificador na linha", elemento.linha)
            else:
                insert_ts = {elemento.cadeia: {"Cadeia": elemento.cadeia, "Token": elemento.classe, \
                                               "Endereço": elemento.linha,  "Categoria": "procedure","Parametros":[]}}
                tokens.append(elemento.cadeia)

                procedures.append(insert_ts)

                ts = escopos.get(escopo_atual)

                #ts.update(insert_ts)

                prox_escopo = elemento.cadeia

                escopos.update({elemento.cadeia:{}})

                self.parametros()
                self.corpo_p()

    def parametros(self):
        global procedures, escopos, parametros, escopo_atual, prox_escopo
        elemento = self.tokens.peek()
        if not (elemento.cadeia == "("):
            raise NameError("Erro Sintático. Esperava-se '(' na linha", elemento.linha)
        else:
            self.tokens.remove()
            self.lista_par()

            ts_old = escopos.get(escopo_atual)


            escopo_atual = prox_escopo
            ts = escopos.get(escopo_atual)
            #ts.update(ts_old)

            tokens = []
            for par in parametros:
                if (par != "real" and par != "integer"):
                    insert_ts = {par: {"Cadeia": par, "Token": "id",  "Categoria": "var"}}
                    ts.update(insert_ts)
                    tokens.append(par)
                else:
                    for token in tokens:
                        update = ts.get(token)
                        update.update({"Tipo":par})
                    tokens.clear()

            procedure = procedures[0]
            for name in procedure:
                nome = name
                procedure[name].update({"Parametros": parametros[:]})

            ts = escopos.get("main")

            ts.update(procedure)

            procedures.clear()
            parametros.clear()

            elemento = self.tokens.remove()
            if not (elemento.cadeia == ")"):
                raise NameError("Erro Sintático. Esperava-se ')' na linha", elemento.linha)



    def lista_par(self):
        global escopos, escopo_atual, procedures, parametros
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
            #Voltar escopo para o main
            escopo_atual = "main"
            if not (elemento.cadeia == "end"):
                raise NameError("Erro Sintático. Esperava-se 'end' na linha", elemento.linha)


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
        global argumentos
        elemento = self.tokens.remove()
        if elemento.classe == "Identificador":
            try:

                get_dict = get_ts(elemento.cadeia)

                if (argumentos):
                    idx = 0
                    for arg in argumentos:
                        if (arg == "integer" or arg == "real"):
                            verifica = arg
                            break
                        idx +=1

                    if (get_dict["Tipo"] == verifica):
                        argumentos[0]-=1
                    else:
                        raise NameError("Tipo não compativel no procedimento")

                    if(argumentos[0] == 0):
                        argumentos.remove(0)
                        argumentos.remove(verifica)

            except:
                raise NameError("Variavel não encontrada: %s" % elemento.cadeia)
            self.mais_ident()
        else:
            raise NameError("Erro Sintático. Esperava-se um identificador na linha", elemento.linha)

    def mais_ident(self):
        global argumentos
        elemento = self.tokens.peek()
        if elemento.cadeia == ";":
            self.tokens.remove()
            self.argumentos()

        if (argumentos):
            print(argumentos)
            raise NameError("Quantidade incorreta de parametros")

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
        global argumentos,verifica_tipo
        global variaveis
        elemento = self.tokens.remove()
        if (elemento.cadeia == "read") or (elemento.cadeia == "write"):
            elemento = self.tokens.remove()
            if elemento.cadeia == "(":
                self.variaveis()

                for var in variaveis:
                    v = var[0]
                    ts = get_ts(v)


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
                if (get_dict["Categoria"] == "procedure"):
                    cont = 0;
                    argumentos.clear()
                    for par in get_dict["Parametros"]:
                        if par != "real" and par != "integer":
                            cont+=1
                        else:
                            argumentos.append(cont)
                            argumentos.append(par)
                            cont = 0
                if (get_dict["Categoria"] == "var"):
                    verifica_tipo = get_dict["Tipo"]

            except:

                if (escopo_atual != "main"):
                    ts = escopos["main"]
                    if (ts.get(elemento.cadeia)):
                        pass
                    else:
                        raise NameError("Variavel não encontrada: %s" % elemento.cadeia)
            self.restoident()

        else:
            raise NameError("Erro Sintático. Esperava-se algo na linha", elemento.linha)


    def restoident(self):
        global procedure
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
        global verifica_tipo
        self.termo()
        self.outros_termos()
        verifica_tipo = ""


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
        global verifica_tipo
        elemento = self.tokens.peek()
        classes = ["Identificador", "Real", "Inteiro"]
        if not elemento.classe in classes:
            self.expressao()
        else:
            if elemento.classe == "Identificador":
                try:
                    get_dict = get_ts(elemento.cadeia)
                    if (verifica_tipo and verifica_tipo != get_dict["Tipo"]):
                        raise NameError("Tipos incompativeis: %s" % elemento.cadeia)

                    verifica_tipo = get_dict["Tipo"]
                except:
                    raise NameError("Variavel não encontrada: %s" % elemento.cadeia)
            else:
                verifica = verifica_tipo
                if (verifica_tipo == ""):
                    if (elemento.classe == "Inteiro"):
                        verifica_tipo == "integer"
                    elif (elemento.classe == "Real"):
                        verifica_tipo = "real"
                else:
                    if(elemento.classe == "Inteiro"):
                        if (verifica_tipo != "integer"):
                            raise NameError("Tipos de variáveis incompativeis")
                    elif(elemento.classe == "Real"):
                        if (verifica_tipo != "real"):
                            raise NameError("Tipos de variáveis incompativeis")



            self.tokens.remove()


from Token import Token

from Fila import Fila

class Sintatico():
    def __init__(self,tokens):
        self.tokens = tokens

    def analisar(self):
        self.S()

    def programa(self):
        elemento = self.tokens.remove()
        if not (elemento.cadeia == "program"):
            raise NameError("Erro Sintático. Esperava-se 'program' na linha", elemento.linha)
        else:
            elemento = self.tokens.remove()
            if not (elemento.classe == "Identificador"):
                raise NameError("Erro Sintático. Esperava-se um identificador na linha", elemento.linha)
            else:
                self.corpo()
                elemento = self.tokens.remove()
                if elemento.cadeia == ".":
                    print("AEE")


    def S(self):
        self.programa()

    def corpo(self):
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
        elemento = self.tokens.remove()
        if not (elemento.cadeia == "real" or elemento.cadeia == "integer"):
            raise NameError("Erro Sintático. Esperava-se um tipo de variavel na linha", elemento.linha)

    def variaveis(self):
        elemento = self.tokens.remove()
        if not (elemento.classe == "Identificador"):
            raise NameError("Erro Sintático. Esperava-se um identificador na linha", elemento.linha)
        else:
            self.mais_var()

    def mais_var(self):
        elemento = self.tokens.peek()
        if elemento.cadeia == ",":
            self.tokens.remove()
            self.variaveis()

    def dc_p(self):
        elemento = self.tokens.remove()
        if not (elemento.cadeia == "procedure"):
            raise NameError("Erro Sintático. Esperava-se 'procedure' na linha", elemento.linha)
        else:
            elemento = self.tokens.remove()
            if not (elemento.classe == "Identificador"):
                raise NameError("Erro Sintático. Esperava-se um identificador na linha", elemento.linha)
            else:
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
        self.dc_loc()
        elemento = self.tokens.remove()
        if not (elemento.cadeia == "begin"):
            raise NameError("Erro Sintático. Esperava-se 'begin' na linha", elemento.linha)
        else:
            self.comandos()
            elemento = self.tokens.remove()
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
        elemento = self.tokens.remove()
        if elemento.classe == "Identificador":
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
            self.tokens.remove()


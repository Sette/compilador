
from Lexico import Lexico
from Sintatico import Sintatico

def main():
    tokens = Lexico("erro")
    tokens = tokens.analisar()
    lista = tokens.getList()
    #for elemento in lista:
    #    print(elemento.cadeia)
    sintatico = Sintatico(tokens)
    sintatico.analisar()


if __name__=="__main__":
    main()

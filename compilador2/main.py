
from Lexico import Lexico
from Sintatico import Sintatico

def main():
    tokens = Lexico("entrada")
    tokens = tokens.analisar()
    lista = tokens.getList()
    #for elemento in lista:
    #    print(elemento.cadeia)
    sintatico = Sintatico(tokens)
    sintatico.analisar()
    print("Inicio de tradução")


if __name__=="__main__":
    main()

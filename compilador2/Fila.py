class Fila(object):
    def __init__(self):
        self.dados = []

    def add(self, elemento):
        self.dados.append(elemento)

    def peek(self):
        return self.dados[0]

    def peek_2(self):
        return self.dados[1]

    def remove(self):
        return self.dados.pop(0)

    def vazia(self):
        return len(self.dados) == 0
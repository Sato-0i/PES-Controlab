import os
import pickle

ARQUIVO = "dados.pkl"


class Banco:
    def __init__(self):
        self.estabelecimentos = []
        self.usuarios = []
        self.produtos = []
        self.ordens = []
        self.prox_produto = 1
        self.prox_os = 1


def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "rb") as f:
            return pickle.load(f)
    return Banco()


def salvar(banco):
    with open(ARQUIVO, "wb") as f:
        pickle.dump(banco, f)

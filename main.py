import random
from datetime import date

import dados
from modelos import (Clinica, Laboratorio, Dentista, Protetico,
                     Produto, OrdemServico)

banco = dados.carregar()
usuario_logado = None

TIPOS = ["Total", "Parcial", "Sobre Implante"]
MATERIAIS = ["Zirconia", "Resina", "Porcelana"]
CORES = ["A1", "A2", "A3", "A3.5", "A4", "B1", "B2", "B3", "B4", "C1", "C2", "D2"]
FORMAS = ["Dinheiro", "Cartao", "PIX", "Boleto"]


#  funcoes auxiliares :)

def falar(texto):
    print("Bot: " + texto)


def perguntar(texto):
    return input("Bot: " + texto + "\nVoce: ").strip()


def ler_numero(texto, tipo=int):
    while True:
        try:
            return tipo(perguntar(texto).replace(",", "."))
        except ValueError:
            falar("Valor invalido, tente de novo.")


def ler_data(texto):
    while True:
        try:
            dia, mes, ano = perguntar(texto + " (dd/mm/aaaa)").split("/")
            return date(int(ano), int(mes), int(dia))
        except ValueError:
            falar("Data invalida.")


def escolher(titulo, opcoes):
    falar(titulo)
    for i, op in enumerate(opcoes, 1):
        print(f"   {i}) {op}")
    while True:
        r = perguntar("Digite o numero da opcao")
        if r.isdigit() and 1 <= int(r) <= len(opcoes):
            return int(r) - 1
        falar("Opcao invalida.")


def eh_protetico():
    return isinstance(usuario_logado, Protetico)


def minhas_ordens():
    # cada usuario so ve as ordens em que esta envolvido
    if eh_protetico():
        return [o for o in banco.ordens if o.laboratorio is usuario_logado.estabelecimento]
    return [o for o in banco.ordens if o.dentista is usuario_logado]


def mostrar_ordem(o):
    dentes = ", ".join(str(e) for e in o.elementos)
    produtos = "; ".join(f"{p.tipo}/{p.material}" for p in o.produtos)
    entrega = f"{o.data_entrega.day:02d}/{o.data_entrega.month:02d}/{o.data_entrega.year}"
    print(f"   OS {o.numero} | codigo {o.codigo} | {o.status} | {o.situacao_prazo()}")
    print(f"   Paciente: {o.paciente} (prontuario {o.prontuario}) | Cor: {o.cor} | Dentes: {dentes}")
    print(f"   Produtos: {produtos}")
    print(f"   Entrega prevista: {entrega} | Pagamento: {o.pagamento.status()}")
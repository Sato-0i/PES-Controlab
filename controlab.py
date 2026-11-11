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

#proximo é passo é cadastro e login

# Cadastro e Login 

def cadastrar_usuario():
    falar("CADASTRO DE USUARIO")
    i = escolher("Qual a sua funcao?", ["Dentista", "Protetico"])
    if i == 0:
        classe_est, classe_usu, tipo_est = Clinica, Dentista, "clinica"
    else:
        classe_est, classe_usu, tipo_est = Laboratorio, Protetico, "laboratorio"

    lista = [e for e in banco.estabelecimentos if isinstance(e, classe_est)]
    opcoes = [e.nome for e in lista] + ["Cadastrar nova " + tipo_est if i == 0 else "Cadastrar novo " + tipo_est]
    j = escolher(f"A qual {tipo_est} voce esta vinculado?", opcoes)
    if j == len(lista):
        nome_est = perguntar("Nome da " + tipo_est)
        if nome_est == "":
            falar("O nome e obrigatorio.")
            return
        endereco = perguntar("Endereco")
        contato = perguntar("Contato")
        estab = classe_est(nome_est, endereco, contato)
    else:
        estab = lista[j]

    nome = perguntar("Seu nome completo")
    login = perguntar("Escolha um login")
    senha = perguntar("Escolha uma senha")
    if nome == "" or login == "" or senha == "":
        falar("Preencha todos os campos.")
        return
    for u in banco.usuarios:
        if u.login == login:
            falar("Esse login ja existe.")
            return
    if estab not in banco.estabelecimentos:
        banco.estabelecimentos.append(estab)
    banco.usuarios.append(classe_usu(nome, login, senha, estab))
    dados.salvar(banco)
    falar("Cadastro realizado com sucesso!")


def fazer_login():
    global usuario_logado
    falar("LOGIN")
    login = perguntar("Login")
    senha = perguntar("Senha")
    for u in banco.usuarios:
        if u.login == login and u.conferir_senha(senha):
            usuario_logado = u
            falar(f"Bem-vindo, {u.nome} ({u.funcao}).")
            return True
    falar("Login ou senha incorretos.")
    return False
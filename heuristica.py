import random

# Matriz de custos (empresas x projetos)
matrix_valores = [
    [12, 18, 15, 22, 9, 14, 20, 11, 17],
    [19, 8, 13, 25, 16, 10, 7, 21, 24],
    [6, 14, 27, 10, 12, 19, 23, 16, 8],
    [17, 11, 20, 9, 18, 13, 25, 14, 22],
    [10, 23, 16, 14, 7, 21, 12, 19, 15],
    [13, 25, 9, 17, 11, 8, 16, 22, 20],
    [21, 16, 24, 12, 20, 15, 9, 18, 10],
    [8, 19, 11, 16, 22, 17, 14, 10, 13],
    [15, 10, 18, 21, 13, 12, 22, 9, 16]
]

# Função para calcular o custo total de uma solução


def calcular_custo(solucao):
    custo_total = 0  # Custo total inicial
    # Para cada empresa, pega o projeto correspondente
    for empresa, projeto in enumerate(solucao):
        # Aqui, adicionamos em custo_total o valor da empresa X no projeto Y alocado.
        # usamos -1 porque os projetos são de 1 a 9, mas os índices da lista são de 0 a 8.
        # Adiciona o custo do projeto à soma total
        custo_total += matrix_valores[empresa][projeto - 1]
    return custo_total

# Para gerar vizinhos, trocamos os projetos entre duas empresas somente se o custo do novo projeto for menor que o atual.
# Assim, garantimos que estamos sempre buscando soluções melhores.


def gerar_vizinhos_melhores(solucao, custo_atual):
    vizinhos = []  # Lista para armazenar vizinhos melhores
    for i in range(len(solucao)):  # Compara todas as trocas possíveis entre empresas
        for j in range(i + 1, len(solucao)):
            vizinho = solucao.copy()  # Copia a solução atual pra poder mudar ela
            # Troca os projetos entre as duas empresas
            vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
            # Calcula o custo do vizinho novo
            custo_vizinho = calcular_custo(vizinho)
            if custo_vizinho < custo_atual:  # Será aceito se o custo for menor que o atual
                # Adiciona o vizinho à lista
                vizinhos.append((vizinho, custo_vizinho))
    return vizinhos

# Nossa função principal de Hill Climbing, que gera uma solução inicial aleatória e tenta melhorá-la.


def hill_climbing():
    solucao_atual = list(range(1, 10))  # Geramos uma lista de 1 a 9 aleatorioa
    # Embaralha a lista para gerar uma solução inicial aleatória
    random.shuffle(solucao_atual)
    # Chama a função de calcular custo
    custo_atual = calcular_custo(solucao_atual)

    while True:
        # Vai buscar os melhores vizinhos a partir da aleatória
        vizinhos_melhores = gerar_vizinhos_melhores(solucao_atual, custo_atual)

        # Caso ela seja a melhor solução e não tiver vizinhos melhores, para o loop.
        if not vizinhos_melhores:
            break

        melhor_vizinho, melhor_custo = min(
            vizinhos_melhores, key=lambda x: x[1])  # Seleciona o melhor vizinho entre todos encontrados.
        solucao_atual = melhor_vizinho  # Poe o melhor vizinho como a melhor solução
        custo_atual = melhor_custo  # Poe o melhor custo da seleção escolhida

    return solucao_atual, custo_atual


# Aqui basicamente chamamos o hill_climbing n vezes e dentre todas retornando a com menor custo. Buscamos o menor global assim.
def multi_start_hill_climbing(n):
    melhor_solucao = None
    # Valor infinito garante qualquer valor já seja o melhor. Poderia ser algo como 100000, mas por boas práticas é melhor por dessa forma.
    melhor_custo = float('inf')
    for _ in range(n):  # Execução do hill climbing
        solucao, custo = hill_climbing()
        # quando o custo de uma for menor que a atual, os valores mudam e ela passa a ser o menor local.
        if custo < melhor_custo:
            melhor_solucao = solucao
            melhor_custo = custo
    # Vai retornar o menor custo de todos da iteração, e junto a lista da solução. Aqui a chance de ser o mínimo global é alta.
    return melhor_solucao, melhor_custo


# Executa o Multi-start, podemos mudar as iterações aqui.
solucao, custo = multi_start_hill_climbing(100)

# Exibe resultado da melhor e seu custo
print("Melhor solução (projeto por empresa):", solucao)
print("Custo total:", custo)

# Exibe a matriz binária de alocação.
print("\nMatriz binária (empresa x projeto):")
# Cria a matriz 9x9 com 0 (zeros)
matriz_binaria = [[0 for _ in range(9)] for _ in range(9)]
for empresa, projeto in enumerate(solucao):
    # Coloca o 1 na posição correspondente de [empresa][projeto] = [i][j] que está no vetor
    # Subtrai porque la encima ta de 1 a 9, e tem que ser de 0 a 8 nas matrizes.
    matriz_binaria[empresa][projeto - 1] = 1

for linha in matriz_binaria:  # Print da matriz binária
    print(' '.join(str(valor) for valor in linha))

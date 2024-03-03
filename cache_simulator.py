import sys  # Importa o módulo sys para lidar com argumentos de linha de comando, variáveis de ambiente e controle de fluxo de entrada/saída.
import struct  # Importa o módulo struct para lidar com dados binários
import numpy as np  # Importa o módulo numpy para operações matemáticas
import random as rd  # Importa o módulo random para geração de números aleatórios
from collections import deque  # Importa a classe deque do módulo collections que fornece uma implementacao otimizada de uma fila de dupla extremidade em py

# Para usar o simulador, use o seguinte comando no terminal: python cache_simulator <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada
# Define a classe SimuladorCache


class SimuladorCache:
    # Método de inicialização da classe
    def __init__(self, nconjuntos, tamanho_bloco, associatividade, substituicao, flag_saida, arquivo_entrada):
        # Atributos da classe
        self.nconjuntos = nconjuntos  # Número de conjuntos na cache
        self.tamanho_bloco = tamanho_bloco  # Tamanho do bloco em bytes
        self.associatividade = associatividade  # Grau de associatividade da cache
        self.substituicao = substituicao  # Política de substituição (R: aleatório, L: LRU, F: FIFO)
        self.flag_saida = flag_saida  # Flag de saída para determinar o formato de saída
        self.linhas_cache = [[None] * associatividade for _ in range(nconjuntos)]  # Matriz representando a cache
        self.arquivo_entrada = arquivo_entrada  # Arquivo binário de entrada
        # Cálculo dos bits para offset, índice e tag
        self.bits_offset = int(np.log2(tamanho_bloco))
        self.bits_indice = int(np.log2(nconjuntos))
        self.bits_tag = 32 - self.bits_offset - self.bits_indice
        # Inicialização da fila para políticas de substituição LRU e FIFO
        if substituicao == 'F' or substituicao == 'L':
            self.fila = [deque() for _ in range(nconjuntos)]
        # Leitura dos dados binários do arquivo de entrada
        with open(arquivo_entrada, 'rb') as f:
            self.dados_binarios = f.read()
        # Conversão dos dados binários em uma sequência de números inteiros
        self.contagem_enderecos = len(self.dados_binarios) // 4
        self.valores_enderecos = struct.unpack('>' + 'i' * self.contagem_enderecos, self.dados_binarios)

    # Método para criar a cache
    def criar_cache(self):
        for i in range(self.nconjuntos):
            for j in range(self.associatividade):
                self.linhas_cache[i][j] = LinhaCache()  # Cria um objeto LinhaCache para cada linha da cache

    # Método para imprimir os atributos da cache
    def imprimir_atributos(self):
        print("Número de conjuntos:", self.nconjuntos, "Tamanho do bloco:", self.tamanho_bloco, "Associatividade:", self.associatividade)
        print("Política de substituição:", self.substituicao, "Flag de saída:", self.flag_saida)
        print("Número de conjuntos:", self.nconjuntos)
        print("Tamanho do conjunto:", self.associatividade, "blocos")
        print("Tamanho total da Cache:", self.nconjuntos * self.tamanho_bloco * self.associatividade, "bytes")
        print("Arquivo de entrada:", self.arquivo_entrada)
        print("Tipo da Cache:")
        # Determina e imprime o tipo de cache com base na associatividade
        if self.associatividade == 1:
            print("Mapeamento Direto")
        elif self.nconjuntos == 1:
            print("Totalmente Associativa")
        else:
            print("Associativa por Conjunto")

    # Método para realizar a substituição de blocos na cache
    def substituir(self, indice, tag, i):
        if self.substituicao == 'R':  # Política de substituição aleatória
            r = rd.randrange(0, self.associatividade)
            self.linhas_cache[indice][r].bloco = tag
        elif self.substituicao == 'L':  # Política de substituição LRU (Least Recently Used)
            l = self.fila[indice].popleft()
            self.linhas_cache[indice][l].bloco = tag
            self.fila[indice].append(l)
        elif self.substituicao == 'F':  # Política de substituição FIFO (First In First Out)
            l = self.fila[indice].popleft()
            self.linhas_cache[indice][l].bloco = tag
            self.fila[indice].append(l)
        else:  # Política de substituição padrão (aleatória)
            r = rd.randrange(0, self.associatividade)
            self.linhas_cache[indice][r].bloco = tag

    # Método para verificar se a cache está cheia
    def cheia(self):
        for i in range(self.nconjuntos):
            for j in range(self.associatividade):
                if self.linhas_cache[i][j].valido == 0:
                    return False
        return True

    # Método para simular o acesso em uma cache de mapeamento direto
    def mapeamento_direto(self, indice, tag, missComp, missCap, missConf, hits):
        if self.linhas_cache[indice][0].valido == 0:
            self.linhas_cache[indice][0].valido = 1
            self.linhas_cache[indice][0].bloco = tag
            missComp += 1
        else:
            if self.linhas_cache[indice][0].bloco != tag:
                self.linhas_cache[indice][0].bloco = tag
                if self.cheia():
                    missCap += 1
                else:
                    missConf += 1
            elif self.linhas_cache[indice][0].bloco == tag:
                hits += 1
        return missComp, missCap, missConf, hits

    # Método para simular o acesso em uma cache associativa por conjunto
    def associativo_por_conjunto(self, indice, tag, missComp, missCap, missConf, hits):
        for i in range(self.associatividade):
            if self.linhas_cache[indice][i].valido == 0:
                self.linhas_cache[indice][i].valido = 1
                self.linhas_cache[indice][i].bloco = tag
                if self.substituicao == 'F' or self.substituicao == 'L':
                    self.fila[indice].append(i)
                missComp += 1
                break
            elif self.linhas_cache[indice][i].bloco == tag:
                if self.substituicao == 'L':
                    self.fila[indice].remove(i)
                    self.fila[indice].append(i)
                hits += 1
                break
            elif i == (self.associatividade - 1):
                self.substituir(indice, tag, i)
                if self.cheia():
                    missCap += 1
                else:
                    missConf += 1
                break
        return missComp, missCap, missConf, hits

    # Método para ler os endereços e simular acessos à cache
    def ler(self):
        hits = 0
        missConf = 0
        missComp = 0
        missCap = 0
        for i in range(self.contagem_enderecos):
            tag = self.valores_enderecos[i] >> (self.bits_offset + self.bits_indice)
            indice = (self.valores_enderecos[i] >> self.bits_offset) & ((1 << self.bits_indice) - 1)
            if self.associatividade == 1:
                missComp, missCap, missConf, hits = self.mapeamento_direto(indice, tag, missComp, missCap, missConf, hits)
            else:
                missComp, missCap, missConf, hits = self.associativo_por_conjunto(indice, tag, missComp, missCap, missConf, hits)

        totalAcessos = missConf + hits + missComp + missCap
        taxaHits = hits / totalAcessos
        taxaMiss = (missConf + missComp + missCap) / totalAcessos
        taxaMissComp = missComp / (missConf + missComp + missCap)
        taxaMissCap = missCap / (missConf + missComp + missCap)
        taxaMissConf = missConf / (missConf + missComp + missCap)
        if self.flag_saida == 1:
            print("%d" % totalAcessos, "%.4f" % taxaHits, "%.4f" % taxaMiss, "%.2f" % taxaMissComp,
                  "%.2f" % taxaMissCap, "%.2f" % taxaMissConf)
            input()
        else:
            print("Total de acessos:", totalAcessos)
            print("Taxa de hit:", taxaHits)
            print("Taxa de misses:", taxaMiss)
            print("Taxa de misses compulsórios:", taxaMissComp)
            print("Taxa de misses de capacidade:", taxaMissCap)
            print("Taxa de misses de conflito:", taxaMissConf)
            input()

# Define a classe LinhaCache
class LinhaCache:
    # Método de inicialização da classe
    def __init__(self):
        self.valido = 0  # Indica se a linha da cache está válida (1) ou não (0)
        self.bloco = 0  # Armazena o valor do bloco de memória na linha da cache

# Função principal dada
def main():
    # Verifica se o número de argumentos é correto
    if len(sys.argv) != 7:
        print("Número incorreto de argumentos. Use:")
        print("python cache_simulator.py <nconjuntos> <tamanho_bloco> <associatividade> <substituição> <flag_saida> arquivo_entrada")
        exit(1)

    # Obtém os argumentos da linha de comando
    nconjuntos = int(sys.argv[1])
    tamanho_bloco = int(sys.argv[2])
    associatividade = int(sys.argv[3])
    substituicao = sys.argv[4]
    flag_saida = int(sys.argv[5])
    arquivo_entrada = sys.argv[6]

    # Cria uma instância do SimuladorCache
    simulador_cache = SimuladorCache(nconjuntos, tamanho_bloco, associatividade, substituicao, flag_saida, arquivo_entrada)
    # Cria a cache
    simulador_cache.criar_cache()
    # Imprime os atributos da cache se a flag de saída for 0
    if flag_saida == 0:
        simulador_cache.imprimir_atributos()
    # Realiza a leitura dos endereços e simula os acessos à cache
    simulador_cache.ler()

# Executa a função principal se o script for executado diretamente
if __name__ == '__main__':
    main()

# main.py

import os 
import re  #expressões regulares
from analisador_enron import Grafo

diretorio_emails = "C:/Users/Usuario/Documents/vscode/pyhton/TDEGrafos/Amostra Enron - 2016/brawner-s/all_documents"

# Função expressão regular
def extrair_emails(linha):
    return re.findall(r"[\w\.-]+@[\w\.-]+", linha.lower())

grafo = Grafo()

total_processados = 0

# Percorre todos os arquivos
for root, _, files in os.walk(diretorio_emails):
    for nome_arquivo in files:
        caminho_arquivo = os.path.join(root, nome_arquivo)
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                linhas = f.readlines()
                remetente = []
                destinatarios = []

                # Extrai remetente e destinatários a partir das linhas
                for linha in linhas:
                    if linha.startswith("From:"):
                        remetente = extrair_emails(linha)
                    elif linha.startswith("X-From:") and not remetente:
                        # Usa X-From: se From: não estiver presente
                        remetente = extrair_emails(linha)
                    elif linha.startswith(("X-To:", "X-cc:", "X-bcc:")):
                        destinatarios += extrair_emails(linha)

                # Adiciona as arestas no grafo para cada combinação remetente → destinatário
                for r in remetente:
                    for d in destinatarios:
                        grafo.adicionar_aresta(r, d)
                
                total_processados += 1  # Conta um e-mail processado
        except Exception as e:
            # Caso ocorra erro ao ler algum arquivo
            print(f"Erro ao processar {caminho_arquivo}: {e}")

print(f"Total de e-mails processados: {total_processados}")

grafo.salvar_lista_adjacencia("lista_adjacencia_enron.txt")

# Chama a análise geral do grafo
ordem, tamanho, isolados, top_saida, top_entrada = grafo.analise_geral()

# Imprime resultados da análise
print(f"Ordem (número de vértices): {ordem}")
print(f"Tamanho (número de arestas): {tamanho}")
print(f"Vértices isolados: {isolados}")

print("Top 20 graus de saída:")
for email, grau in top_saida:
    print(f"  {email}: {grau}")

print("Top 20 graus de entrada:")
for email, grau in top_entrada:
    print(f"  {email}: {grau}")

# Verifica se o grafo é Euleriano
eh_euleriano, motivo = grafo.euleriano()
print(f"É Euleriano? {eh_euleriano}. {motivo}")

# Verifica os vértices até uma distância D de um determinado e-mail (N)
N = "sandra.brawner@enron.com"  # E-mail de origem para análise de distância
D = 10  # Distância máxima
vizinhos = grafo.vertices_ate_distancia(N, D)
print(f"Vértices a até distância {D} de {N}:")
for v, d in vizinhos:
    print(f"  {v}: distância {d}")

# Calcula o diâmetro do grafo e o caminho correspondente
diametro, caminho = grafo.calcular_diametro()
print(f"Diâmetro do grafo: {diametro}")
print(f"Caminho correspondente: {caminho}")

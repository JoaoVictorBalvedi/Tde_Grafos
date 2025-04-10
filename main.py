import os  # Usado para percorrer diretórios e arquivos
import re  # Usado para extrair e-mails com expressões regulares
from analisador_enron import Grafo  # Importa a classe Grafo do arquivo analisador_enron.py

# Caminho onde estão os arquivos de e-mail do Enron
diretorio_emails = "C:/vscode/python/MetodosQuant/grafos/Tde_Grafos/Amostra Enron - 2016/brawner-s/all_documents"

# Função que extrai e-mails de uma linha de texto usando expressão regular
def extrair_emails(linha):
    return re.findall(r"[\w\.-]+@[\w\.-]+", linha.lower())

# Cria uma instância do grafo
grafo = Grafo()

# Inicializa um contador de e-mails processados
total_processados = 0

# Percorre todos os arquivos dentro do diretório especificado
for root, _, files in os.walk(diretorio_emails):
    for nome_arquivo in files:
        caminho_arquivo = os.path.join(root, nome_arquivo)
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                linhas = f.readlines()  # Lê todas as linhas do e-mail
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
                        # Adiciona destinatários diretos, cópia e cópia oculta
                        destinatarios += extrair_emails(linha)

                # Adiciona as arestas no grafo para cada combinação remetente → destinatário
                for r in remetente:
                    for d in destinatarios:
                        grafo.adicionar_aresta(r, d)
                
                total_processados += 1  # Conta um e-mail processado
        except Exception as e:
            # Caso ocorra erro ao ler algum arquivo
            print(f"Erro ao processar {caminho_arquivo}: {e}\n")

# Mostra o total de e-mails que foram processados
print(f"Total de e-mails processados: {total_processados}\n")

# Salva a lista de adjacência do grafo em um arquivo .txt
grafo.salvar_lista_adjacencia("lista_adjacencia_enron.txt")

# Chama a análise geral do grafo
ordem, tamanho, isolados, top_saida, top_entrada = grafo.analise_geral()

# Imprime resultados da análise
print(f"Ordem (número de vértices): {ordem}\n")
print(f"Tamanho (número de arestas): {tamanho}\n")
print(f"Vértices isolados: {isolados}\n")

print("Top 20 graus de saída:")
for email, grau in top_saida:
    print(f"  {email}: {grau}")

print("Top 20 graus de entrada:")
for email, grau in top_entrada:
    print(f"  {email}: {grau}")

# Verifica se o grafo é Euleriano
eh_euleriano, motivo = grafo.euleriano()
print(f"É Euleriano? {eh_euleriano}. {motivo}\n")

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
print(f"Caminho correspondente: {caminho}\n")

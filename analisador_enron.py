from collections import defaultdict, deque  # defaultdict facilita criação de dicionários com valores padrão
import heapq  # heapq permite trabalhar com filas de prioridade (usado no Dijkstra)

# Classe principal que representa o grafo de e-mails
class Grafo:
    def __init__(self):
        # Estrutura de dados: dicionário de dicionários (lista de adjacências) com pesos (frequência de e-mails)
        # Ex: self.adj['A']['B'] = 3 → A enviou 3 e-mails para B
        self.adj = defaultdict(lambda: defaultdict(int))

    # Adiciona uma aresta do remetente (origem) para o destinatário (destino)
    def adicionar_aresta(self, origem, destino):
        self.adj[origem][destino] += 1  # Incrementa o peso (frequência de envio)

    # Salva a lista de adjacência (grafo) em um arquivo de texto
    def salvar_lista_adjacencia(self, caminho):
        with open(caminho, 'w', encoding='utf-8') as f:
            for origem in self.adj:
                for destino in self.adj[origem]:
                    peso = self.adj[origem][destino]
                    f.write(f"{origem} -> {destino} [peso: {peso}]\n")


    def analise_geral(self):
        # Junta todos os vértices que aparecem como origem ou destino
        vertices = set(self.adj.keys()) | {d for destinos in self.adj.values() for d in destinos}
        arestas = sum(len(destinos) for destinos in self.adj.values())

        # Identifica vértices isolados (sem entrada nem saída)
        isolados = []
        for v in vertices:
            if v not in self.adj and all(v not in vizinhos for vizinhos in self.adj.values()):
                isolados.append(v)

        # Calcula grau de saída de cada vértice
        grau_saida = {}
        for vertice, vizinhos in self.adj.items():
            grau_saida[vertice] = sum(vizinhos.values())

        # Calcula grau de entrada de cada vértice
        grau_entrada = defaultdict(int)
        for origem in self.adj:
            for destino in self.adj[origem]:
                grau_entrada[destino] += self.adj[origem][destino]

        # Ordena os 20 maiores graus de saída e entrada
        top_saida = sorted(grau_saida.items(), key=lambda x: x[1], reverse=True)[:20]
        top_entrada = sorted(grau_entrada.items(), key=lambda x: x[1], reverse=True)[:20]

        return len(vertices), arestas, len(isolados), top_saida, top_entrada

    # Verifica se o grafo é Euleriano
    def euleriano(self):
        grau_in = defaultdict(int)
        grau_out = defaultdict(int)

        # Conta os graus de entrada e saída para cada vértice
        for u in self.adj:
            for v in self.adj[u]:
                grau_out[u] += self.adj[u][v]
                grau_in[v] += self.adj[u][v]

        # Se algum vértice tem grau de entrada diferente do grau de saída, não é Euleriano
        for v in set(list(grau_in) + list(grau_out)):
            if grau_in[v] != grau_out[v]:
                return False, f"Vértice {v} não tem grau de entrada igual ao de saída."

        # Verifica se o grafo é fortemente conexo usando DFS
        def dfs(origem, grafo):
            visitado = set()
            stack = [origem]
            while stack:
                u = stack.pop()
                if u not in visitado:
                    visitado.add(u)
                    stack.extend(grafo[u])
            return visitado

        # Conjuntos de vértices presentes
        todos = set(grau_out.keys()) | set(grau_in.keys())
        primeiro = next(iter(todos))  # Pega um vértice inicial qualquer

        # Gera a versão normal e a reversa do grafo
        normal = {u: list(self.adj[u].keys()) for u in self.adj}
        reverso = defaultdict(list)
        for u in self.adj:
            for v in self.adj[u]:
                reverso[v].append(u)

        # Verifica se é fortemente conexo no grafo original e transposto
        if dfs(primeiro, normal) != todos:
            return False, "Grafo não é fortemente conexo (direção original)."
        if dfs(primeiro, reverso) != todos:
            return False, "Grafo não é fortemente conexo (grafo transposto)."

        return True, "O grafo é Euleriano."

    # Encontra todos os vértices até uma distância D a partir de um vértice de origem
    def vertices_ate_distancia(self, inicio, D):
        dist = {inicio: 0}  # Dicionário com distâncias mínimas
        heap = [(0, inicio)]  # Fila de prioridade para Dijkstra
        resultado = []

        while heap:
            custo, atual = heapq.heappop(heap) # Pega o vértice com menor custo
            if custo <= D:
                resultado.append((atual, custo))  # Salva vértice e distância
                for vizinho in self.adj[atual]: # Itera sobre os destinatários do vértice atual
                    novo_custo = custo + self.adj[atual][vizinho] # Clacula a distância até o vizinho
                    if vizinho not in dist or novo_custo < dist[vizinho]:
                        dist[vizinho] = novo_custo # Atualiza distância mínima se o vizinho não foi visitado ou a distância é menor
                        heapq.heappush(heap, (novo_custo, vizinho))
        return resultado

    # Calcula o diâmetro do grafo: o maior entre os menores caminhos possíveis entre pares de vértices
    def calcular_diametro(self):
        maior_caminho = 0
        caminho_mais_longo = []

        for origem in list(self.adj): #Testa cada remetente como ponto de partida
            dist = {origem: 0} #Distância mínima do vértice de origem
            anterior = {origem: None} # Dicionário para rastrear o caminho
            heap = [(0, origem)] # Fila de prioridade para Dijkstra

            while heap: # Enquanto houver vértices na fila
                custo, atual = heapq.heappop(heap) # Pega o vértice com menor custo
                for vizinho in self.adj[atual]: # Explora os vizinhos 
                    novo_custo = custo + self.adj[atual][vizinho] #Calcula nova distância
                    if vizinho not in dist or novo_custo < dist[vizinho]: # Se o vizinho não foi visitado ou a nova distância é menor
                        dist[vizinho] = novo_custo # Atualiza a distância mínima
                        anterior[vizinho] = atual # Atualiza o vértice anterior
                        heapq.heappush(heap, (novo_custo, vizinho)) # Adiciona o vizinho à fila

            for destino in dist: # Verifica todos os destinos a partir do vértice de origem
                if dist[destino] > maior_caminho: # Se a distância for maior que o maior caminho encontrado
                    maior_caminho = dist[destino] # Atualiza o maior caminho
                    caminho = []
                    v = destino 
                    while v is not None:  # Continua até None
                        caminho.append(v) # Adiciona o vértice ao caminho
                        v = anterior[v] # Move para o vértice anterior
                    caminho_mais_longo = list(reversed(caminho))  # Remove append(origem)

        return maior_caminho, caminho_mais_longo

# Analisador de Contatos - Base de E-mails Enron

## Descrição
Este projeto analisa uma base de e-mails da Enron e constrói um grafo direcionado, ponderado e rotulado com base nas relações de envio de mensagens. A partir desse grafo, são feitas diversas análises, como verificação de ciclo Euleriano, grau de entrada/saída, diâmetro e vizinhança por distância.

## Funcionalidades
- Leitura e processamento de mensagens de e-mail
- Construção de grafo com:
  - Arestas direcionadas
  - Pesos com base na frequência de e-mails
  - Rótulos dos vértices como e-mails
- Geração de lista de adjacência (`.txt`)
- Cálculo de:
  - Ordem e tamanho do grafo
  - Vértices isolados
  - Top 20 graus de entrada/saída
  - Verificação de ciclo Euleriano
  - Vizinhos até distância D de um vértice N
  - Diâmetro do grafo

## Estrutura de Arquivos
- `main.py`: script principal para análise
- `analisador_enron.py`: classe `Grafo` com todas as funções
- `lista_adjacencia_enron.txt`: saída com a lista de adjacência
- `README.md`: este arquivo

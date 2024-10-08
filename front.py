import pickle
import pandas as pd
from shared import *

# Função para exibir o tabuleiro
def print_board(board):
    for row in board:
        print(' | '.join(row))  # Exibe cada linha do tabuleiro
        print('-' * 5)          # Exibe o separador entre as linhas
        
def parse_mlp_result(result):
    parser_table = ["x_win","o_win","draw","in_progress"]
    for i in range(len(result)):
        if result[i] == 1:
            return parser_table[i]
        
def parse_k_means_result(result):
    outcome_mapping = {0: 'o_win', 1: 'x_win', 2: 'draw', 3: 'in_progress'}
    return outcome_mapping[result]

# Função para a jogada de um jogador
def player_move(board, player):
    while True:
        try:
            row = int(input(f"Jogador {player}, escolha a linha (0, 1 ou 2): "))
            col = int(input(f"Jogador {player}, escolha a coluna (0, 1 ou 2): "))
            
            if board[row][col] == 'b':  # Verifica se a célula está vazia
                board[row][col] = player  # Marca o movimento no tabuleiro
                break
            else:
                print("Essa posição já está ocupada. Escolha outra.")
        except (IndexError, ValueError):
            print("Posição inválida. Tente novamente.")

def board_to_string(board):
    return ','.join(cell for row in board for cell in row)

# Função principal do jogo
def tic_tac_toe_game():
    # Inicializar o tabuleiro
    board = [['b', 'b', 'b'], ['b', 'b', 'b'], ['b', 'b', 'b']]
    current_player = 'X'  # O jogador X começa
    opcao = 0
    
    while True:
        print('Escolha o algoritmo usado para a avaliação:')
        print('1. Árvore de Decisão')
        print('2. k-Nearest Neighbors (kNN)')
        print('3. KMeans (apenas clusters, sem rótulos)')
        print('4. MLP')
        print('5. Sair')
        
        opcao = input("Digite o número da sua escolha: ")
        
        if opcao in ['1', '2', '3', '4']:
            break
        
        print('POR FAVOR FIQUE!!!!!')

    while True:
        print_board(board)

        board_string = board_to_string(board)
        board_list = board_string.split(',')
        print(board_list)
        
        mapping = {'X': 1, 'O': -1, 'b': 0}
        board_numeric = [mapping[cell] for cell in board_list]

        board_df = pd.DataFrame([board_numeric])
        
        if opcao == '1':
            with open('modelo_decision_tree.pkl', 'rb') as f:
                modelo_carregado = pickle.load(f)
    
            y_pred_novo = modelo_carregado.predict(board_df)
            
            print(f"A IA disse que o jogo ta: {parse_to_str(y_pred_novo)}")
            
        if opcao == '3':
            with open('kmeans_model.pkl', 'rb') as f:
                modelo_carregado = pickle.load(f)
    
            y_pred_novo = modelo_carregado.predict(board_df)
            
            print(f"A IA disse que o jogo ta: {parse_k_means_result(y_pred_novo[0])}")
        
        if opcao == '4':
            with open('mlp_model.pkl', 'rb') as f:
                modelo_carregado = pickle.load(f)
    
            y_pred_novo = modelo_carregado.predict(board_df)
            
            print(f"A IA disse que o jogo ta: {parse_mlp_result(y_pred_novo[0])}")
        
        # Jogada do jogador atual
        player_move(board, current_player)
        
        # Alternar o jogador
        current_player = 'O' if current_player == 'X' else 'X'
        
        # Verificar se o tabuleiro está cheio e, se sim, encerrar o jogo
        if all(cell != 'b' for row in board for cell in row):
            print_board(board)  # Imprime o tabuleiro pela última vez
            board_string = board_to_string(board)
            print(f"Todas as posições foram preenchidas. Estado final do tabuleiro: {board_string}")
            break

# Iniciar o jogo
tic_tac_toe_game()

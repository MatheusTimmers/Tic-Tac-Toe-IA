import pickle
import pandas as pd

# Função para exibir o tabuleiro de forma formatada
def print_board(board):
    for row in board:
        print(' | '.join(row))  # Exibe cada linha do tabuleiro
        print('-' * 5)          # Exibe o separador entre as linhas

# Função para converter o resultado do KMeans em uma string representativa
def parse_result_kNN_Tree(result):
    outcome_mapping = {-2: 'o_win', 2: 'x_win', 4: 'draw', 3: 'in_progress'}
    return outcome_mapping[result]

def parse_mlp_result_kMeans(result):
    parser_table = ["x_win","o_win","draw","in_progress"]
    for i in range(len(result)):
        if result[i] == 1:
            return parser_table[i]

# Função para coletar a jogada de um jogador
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

# Função para verificar se o jogo acabou e determinar o vencedor
def check_winner(board):
    # Verifica linhas
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != 'b':
            return f"{row[0].lower()}_win"  # Retorna "x_win" ou "o_win"

    # Verifica colunas
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != 'b':
            return f"{board[0][col].lower()}_win"  # Retorna "x_win" ou "o_win"

    # Verifica diagonais
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 'b':
        return f"{board[0][0].lower()}_win"  # Retorna "x_win" ou "o_win" (diagonal principal)
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != 'b':
        return f"{board[0][2].lower()}_win"  # Retorna "x_win" ou "o_win" (diagonal secundária)

    # Verifica empate (todas as posições preenchidas)
    if all(cell != 'b' for row in board for cell in row):
        return "draw"

    # Se nenhuma das condições acima for atendida, o jogo continua
    return "in_progress"

# Converte o tabuleiro em uma string (para manipulação mais fácil)
def board_to_string(board):
    return ','.join(cell for row in board for cell in row)

# Converte o tabuleiro em uma lista numérica para a entrada do modelo
def board_to_numeric(board):
    mapping = {'X': 1, 'O': -1, 'b': 0}
    board_list = board_to_string(board).split(',')
    return [mapping[cell] for cell in board_list]

# Função principal que gerencia o jogo
def tic_tac_toe_game():
    # Inicializa o tabuleiro vazio
    board = [['b', 'b', 'b'], ['b', 'b', 'b'], ['b', 'b', 'b']]
    current_player = 'X'
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
        elif opcao == '5':
            print("Obrigado por jogar!")
            return 
        
        print('Escolha inválida. Tente novamente.')

    # Loop principal do jogo
    while True:
        print_board(board)
        board_numeric = board_to_numeric(board)
        board_df = pd.DataFrame([board_numeric])

        # Carrega e usa o modelo selecionado
        if opcao == '1':
            with open('modelo_decision_tree.pkl', 'rb') as f:
                modelo_carregado = pickle.load(f)
        
        elif opcao == '2':
            with open('knn_model.pkl', 'rb') as f:
                modelo_carregado = pickle.load(f)
        
        elif opcao == '3':
            with open('kmeans_model.pkl', 'rb') as f:
                modelo_carregado = pickle.load(f)
        
        elif opcao == '4':
            with open('mlp_model.pkl', 'rb') as f:
                modelo_carregado = pickle.load(f)
        
        y_pred = modelo_carregado.predict(board_df)
        
        # Apresenta o resultado
        if (opcao in ['1','2']):
            print(f"A IA disse que o estado do jogo é: {parse_result_kNN_Tree(y_pred[0])}")
        elif (opcao in ['3','4']):
            print(f"A IA disse que o estado do jogo é: {parse_mlp_result_kMeans(y_pred[0])}")
            
        resultado_real = check_winner(board)
        print(f"Resultado real: {resultado_real}")
            
        # Jogada do jogador atual
        player_move(board, current_player)
        
        # Alternar o jogador
        current_player = 'O' if current_player == 'X' else 'X'
        
        if resultado_real == ['x_win', 'o_win', 'draw']:
            print_board(board)  # Exibe o tabuleiro final
            print(f"Todas as posições foram preenchidas. Estado final: {board_to_string(board)}")
            
            # Apresenta o resultado
            if (opcao in ['1','2']):
                print(f"A IA disse que esse jogo deu: {parse_result_kNN_Tree(y_pred[0])}")
            elif (opcao in ['3','4']):
                print(f"A IA disse que esse jogo deu: {parse_mlp_result_kMeans(y_pred[0])}")
                
            break

# Iniciar o jogo
tic_tac_toe_game()

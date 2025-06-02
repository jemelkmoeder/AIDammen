import copy

def initialize_board():
    """
    Initialiseert een 8x8-bord.
    Rode stukken (AI) staan op de bovenste drie rijen op de donkere velden.
    Zwarte stukken (jij) staan op de onderste drie rijen op de donkere velden.
    Lege velden worden aangeduid met '.'.
    """
    board = [['.' for _ in range(8)] for _ in range(8)]
    # Plaats AI (rode) stukken op rij 0-2 (donkere velden: waar (rij+kolom) % 2 == 1)
    for row in range(3):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = 'r'
    # Plaats jouw (zwarte) stukken op rij 5-7 op de donkere velden
    for row in range(5, 8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = 'b'
    return board

def print_board(board):
    """Drukt het bord af met rij- en kolomindexen."""
    print("   " + " ".join(str(i) for i in range(8)))
    for i, row in enumerate(board):
        print(f"{i}  " + " ".join(row))
        
def get_directions(piece):
    """
    Bepaalt de bewegingsrichtingen van een stuk.
    Normale zwarte stukken bewegen 'omhoog' (rij -1) en rode stukken 'omlaag' (rij +1).
    Koningen (B of R) mogen in alle vier diagonale richtingen bewegen.
    """
    if piece == 'b':
        return [(-1, -1), (-1, 1)]
    elif piece == 'r':
        return [(1, -1), (1, 1)]
    elif piece in ('B', 'R'):
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
def copy_board(board):
    """Geeft een ondiepe kopie (dieper dan referenties) van het bord terug."""
    return [row[:] for row in board]

def on_board(row, col):
    """Controleert of (row, col) binnen de grenzen van het bord valt."""
    return 0 <= row < 8 and 0 <= col < 8

def opponent_pieces(player):
    """
    Geeft de symboollijst terug van de tegenstander, rekening houdend met normale stukken en koningen.
    Als jij 'b' speelt, zijn de tegenstanders 'r' en 'R', en andersom.
    """
    if player == 'b':
        return ['r', 'R']
    else:
        return ['b', 'B']

def get_jump_moves(board, row, col, piece):
    """
    Zoekt alle sprongzetten (captures) voor een stuk op positie (row, col).
    De functie werkt recursief om meervoudige sprongen te ondersteunen.
    Elke zet wordt gepresenteerd als een lijst van (rij, kolom) tuples, beginnend bij de startpositie.
    """
    moves = []
    directions = get_directions(piece)
    for dr, dc in directions:
        mid_r = row + dr
        mid_c = col + dc
        jump_r = row + 2 * dr
        jump_c = col + 2 * dc
        if on_board(jump_r, jump_c) and board[jump_r][jump_c] == '.' and on_board(mid_r, mid_c) and board[mid_r][mid_c] in opponent_pieces(piece.lower()):
            # Maak een kopie van het bord en voer de sprong uit.
            temp_board = copy_board(board)
            temp_board[jump_r][jump_c] = temp_board[row][col]
            temp_board[row][col] = '.'
            temp_board[mid_r][mid_c] = '.'
            # Controleer of vanaf de nieuwe positie nog extra sprongen mogelijk zijn.
            subsequent_jumps = get_jump_moves(temp_board, jump_r, jump_c, temp_board[jump_r][jump_c])
            if subsequent_jumps:
                for sj in subsequent_jumps:
                    moves.append([(row, col)] + sj)
            else:
                moves.append([(row, col), (jump_r, jump_c)])
    return moves

def get_normal_moves(board, row, col, piece):
    """
    Genereert alle normale (niet-capturerende) bewegingszetten voor een stuk.
    """
    moves = []
    directions = get_directions(piece)
    for dr, dc in directions:
        new_r = row + dr
        new_c = col + dc
        if on_board(new_r, new_c) and board[new_r][new_c] == '.':
            moves.append([(row, col), (new_r, new_c)])
    return moves

def get_piece_moves(board, row, col):
    """
    Geeft, voor het stuk op (row, col), de geldige zetten terug. 
    Eerst worden capture (sprong) zetten gecontroleerd; indien aanwezig moeten deze verplicht genomen worden.
    """
    piece = board[row][col]
    if piece == '.':
        return []
    jumps = get_jump_moves(board, row, col, piece)
    if jumps:
        return jumps
    return get_normal_moves(board, row, col, piece)

def get_all_moves(board, player):
    """
    Zoekt alle zetten voor de gegeven speler (jij: 'b', AI: 'r').
    Indien er capture moves beschikbaar zijn, worden alleen die zetten teruggegeven (capture is verplicht).
    """
    moves = []
    for row in range(8):
        for col in range(8):
            if player == 'b' and board[row][col] in ['b', 'B']:
                for m in get_piece_moves(board, row, col):
                    moves.append(m)
            if player == 'r' and board[row][col] in ['r', 'R']:
                for m in get_piece_moves(board, row, col):
                    moves.append(m)
    capturing_moves = [m for m in moves if abs(m[0][0] - m[-1][0]) > 1]
    if capturing_moves:
        return capturing_moves
    return moves

def simulate_move(board, move):
    """
    Past de zet (een lijst van (rij, kolom) posities) toe op een kopie van het bord en retourneert het nieuwe bord.
    Verwijdert daarbij overgeslagen stukken en voert promotie naar koning uit indien nodig.
    """
    new_board = copy_board(board)
    start = move[0]
    r, c = start
    piece = new_board[r][c]
    new_board[r][c] = '.'
    # Verwijder alle gesprongen (captured) stukken.
    for i in range(1, len(move)):
        r0, c0 = move[i - 1]
        r1, c1 = move[i]
        if abs(r1 - r0) == 2:
            mid_r = (r0 + r1) // 2
            mid_c = (c0 + c1) // 2
            new_board[mid_r][mid_c] = '.'
    final_r, final_c = move[-1]
    new_board[final_r][final_c] = piece
    # Promotie naar koning: zwarte stukken worden koning als ze rij 0 bereiken en rode als ze rij 7 bereiken.
    if piece == 'b' and final_r == 0:
        new_board[final_r][final_c] = 'B'
    if piece == 'r' and final_r == 7:
        new_board[final_r][final_c] = 'R'
    return new_board

def evaluate_board(board):
    """
    Eenvoudige evaluatiefunctie.
    Elk 'normaal' stuk telt voor 1 punt, een koning voor 2 punten.
    De score is: (punten AI) - (punten speler).
    Een positieve score wijst in het voordeel van de AI.
    """
    red_score = 0
    black_score = 0
    for row in board:
        for cell in row:
            if cell == 'r':
                red_score += 1
            elif cell == 'R':
                red_score += 2
            elif cell == 'b':
                black_score += 1
            elif cell == 'B':
                black_score += 2
    return red_score - black_score

def minimax(board, depth, player, alpha, beta):
    """
    Minimale implementatie van minimax met alfa-beta pruning.
    - Als player 'r' (AI) is, maximaliseert de recursie de score.
    - Als player 'b' (jij) speelt, dan minimaliseert de recursie de score.
    """
    moves = get_all_moves(board, player)
    if depth == 0 or not moves:
        return evaluate_board(board), None
    if player == 'r':  # AI maximaliseert
        max_eval = float('-inf')
        best_move = None
        for move in moves:
            new_board = simulate_move(board, move)
            eval_score, _ = minimax(new_board, depth - 1, 'b', alpha, beta)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:  # Speler minimaliseert
        min_eval = float('inf')
        best_move = None
        for move in moves:
            new_board = simulate_move(board, move)
            eval_score, _ = minimax(new_board, depth - 1, 'r', alpha, beta)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def get_best_move(board, depth):
    """Wrapper voor minimax die de beste zet voor de AI (speler 'r') retourneert."""
    score, move = minimax(board, depth, 'r', float('-inf'), float('inf'))
    return move

def main():
    board = initialize_board()
    current_player = 'b'  # Jij (zwart) begint
    while True:
        if current_player == 'b':
            moves = get_all_moves(board, current_player)
            if not moves:
                print("Geen zetten meer voor jou. AI wint!")
                break
            print_board(board)
            print("Beschikbare zetten:")
            for index, m in enumerate(moves):
                # Elke zet wordt weergegeven als een lijst van posities
                print(f"{index}: {m}")
            try:
                choice = int(input("Selecteer het nummer van de zet: "))
            except ValueError:
                print("Ongeldige invoer, probeer het opnieuw.")
                continue
            if choice < 0 or choice >= len(moves):
                print("Ongeldige keuze, probeer het opnieuw.")
                continue
            selected_move = moves[choice]
            board = simulate_move(board, selected_move)
            current_player = 'r'
        else:
            print("AI is aan de beurt...")
            moves = get_all_moves(board, current_player)
            if not moves:
                print("Geen zetten meer voor AI. Jij wint!")
                break
            ai_move = get_best_move(board, 4)  # Verdiepingsniveau 4 voor minimax
            if ai_move is None:
                ai_move = moves[0]
            print("AI zet:", ai_move)
            board = simulate_move(board, ai_move)
            current_player = 'b'

if __name__ == "__main__":
    main()

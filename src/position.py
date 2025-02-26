from const import *
from burke import Burke

class Position:

    def __init__(self):
        self.generate_new = True
        self.pos_fen = ""

    def get_position(self, board, next_player):

        if self.generate_new:
            pos_list = []
            
            # Get all pieces and their positions into a list
            for row in range(ROWS):
                for col in range(COLS):
                    piece = board.squares[row][col].piece
                    if piece:
                        pos_list.append({
                            'piece': piece.name,
                            'color': piece.color,
                            'square': f"{chr(col + 97)}{8 - row}"  # Convert to chess notation
                        })

            # Now convert that list into a string that Burke can understand
            pos_str = "Chess pieces are located at: "
            for piece in pos_list:
                pos_str += f"{piece['color']} {piece['piece']} on {piece['square']};"

            pos_str += f"\nNext player is {next_player}"

            # Ask Burke to generate FEN notation of the position
            burke = Burke()
            self.pos_fen = burke.get_fen(pos_str)

            print(self.pos_fen)

            # Don't generate new FEN notation for the same position (until a new position is set on the board)
            self.generate_new = False

        return self.pos_fen

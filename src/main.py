import pygame
import sys
from const import *
from game import Game
from square import Square
from move import Move
from position import Position
from burke import Burke
from popup import Popup

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Ask Burke (Your Chess Assistant)')
        self.game = Game()
        self.font = pygame.font.Font(None, 32)
        self.position = Position()
        self.burke = Burke()
        self.popup = Popup(self.screen)


    def mainloop(self):
        
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        position = self.position
        burke = self.burke
        popup = self.popup

        while True:
            # show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # if clicked square has a piece ?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color) ?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show methods 
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                
                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # valid move ?
                        if board.valid_move(dragger.piece, move):
                            # normal capture
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)                            

                            # sounds
                            game.play_sound(captured)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                            position.generate_new = True
                            # next turn
                            game.next_turn()
                    
                    dragger.undrag_piece()
                
                # key press
                elif event.type == pygame.KEYDOWN:
                    
                    # changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # changing themes
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                    # evaluate position
                    if event.key == pygame.K_e:
                        pos_fen = position.get_position(board, game.next_player)
                        num_words = 100
                        context = "evaluate why white or black is better in this chess position"
                        evaluation = burke.evaluate_position(pos_fen, num_words, context)
                        popup.show("", evaluation, num_words)

                    # evaluate white's next best move
                    if event.key == pygame.K_w:
                        pos_fen = position.get_position(board, game.next_player)
                        num_words = 20
                        context = "evaluate white's next best move in this chess position"
                        evaluation = burke.evaluate_position(pos_fen, num_words, context)
                        popup.show("", evaluation, num_words)

                    # evaluate black's next best move
                    if event.key == pygame.K_b:
                        pos_fen = position.get_position(board, game.next_player)
                        num_words = 20
                        context = "evaluate black's next best move in this chess position"
                        evaluation = burke.evaluate_position(pos_fen, num_words, context)
                        popup.show("", evaluation, num_words)

                    # evaluate score
                    if event.key == pygame.K_s:
                        pos_fen = position.get_position(board, game.next_player)
                        num_words = 20
                        context = "evaluate the score of white from -20 to 20 in this chess position"
                        evaluation = burke.evaluate_position(pos_fen, num_words, context)
                        popup.show("", evaluation, num_words)

                    if event.key == pygame.K_h:
                        num_words = 35
                        help = """
                        t - change theme
                        r - reset theme
                        e - evaluate position
                        w - evaluate white's next best move
                        b - evaluate black's next best move
                        s - evaluate score
                        """
                        
                        popup.show("", help, num_words)

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

main = Main()
main.mainloop()
import pygame

from board import Board
from dialog import Dialog
from pieces import Pawn, WHITE, BLACK


def main():
    pygame.init()

    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 800
    board = Board()

    is_piece_draging = False
    focused_piece = None
    is_check = False
    is_promoted = False

    mouse_offset_x = 0
    mouse_offset_y = 0

    current_player_color = WHITE
    next_player_color = BLACK

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # set center of window
    board_offset_x = (screen.get_width() - board.get_width()) // 2
    board_offset_y = (screen.get_height() - board.get_height()) // 2

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if is_promoted:
                dialog.handle_events(event)
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left Mouse Button
                        x = event.pos[0] - board_offset_x
                        y = event.pos[1] - board_offset_y

                        focused_piece = board.get_collided_piece(
                            (x, y), current_player_color)

                        if focused_piece is not None:
                            is_piece_draging = True
                            board.move_up(focused_piece)

                            mouse_offset_x = focused_piece.rect.x - x
                            mouse_offset_y = focused_piece.rect.y - y

                elif event.type == pygame.MOUSEMOTION:
                    if is_piece_draging:
                        mouse_x, mouse_y = event.pos

                        # move a piece (in window)
                        focused_piece.rect.x = mouse_x - board_offset_x + mouse_offset_x
                        focused_piece.rect.y = mouse_y - board_offset_y + mouse_offset_y

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        is_piece_draging = False

                        # when piece is moved
                        if focused_piece is not None and board.set_piece_position(focused_piece):

                            if isinstance(focused_piece, Pawn) and focused_piece.is_promotion():
                                is_promoted = True
                                dialog = Dialog(focused_piece.color)
                            else:
                                # maybe there is check
                                is_check = board.is_check(
                                    current_player_color, next_player_color)

                                # generate valid moves for next player
                                # but when opponent has no move
                                # it's game over
                                if board.generate_valid_moves_for_player_pieces(next_player_color, current_player_color):

                                    # but there can be a draw
                                    if board.is_stalemate(current_player_color, next_player_color):
                                        print("Remis")

                                    # otherwise one player wins
                                    else:
                                        if current_player_color == WHITE:
                                            print(
                                                "Wygrał gracz z kolorem biały")
                                        else:
                                            print(
                                                "Wygrał gracz z kolorem czarnym")

                                    running = False

                                # change player
                                if current_player_color == WHITE:
                                    current_player_color = BLACK
                                    next_player_color = WHITE
                                else:
                                    current_player_color = WHITE
                                    next_player_color = BLACK
        board.blit_self()

        if is_promoted and dialog.piece_choose is not None:
            board.pawn_promotion(focused_piece, dialog.piece_choose)
            is_check = board.is_check(current_player_color, next_player_color)
            if board.generate_valid_moves_for_player_pieces(next_player_color, current_player_color):

                # but there can be a draw
                if board.is_stalemate(current_player_color, next_player_color):
                    print("Remis")

                # otherwise one player wins
                else:
                    if current_player_color == WHITE:
                        print(
                            "Wygrał gracz z kolorem biały")
                    else:
                        print(
                            "Wygrał gracz z kolorem czarnym")

                running = False
            # change player

            if current_player_color == WHITE:
                current_player_color = BLACK
                next_player_color = WHITE
            else:
                current_player_color = WHITE
                next_player_color = BLACK

            is_promoted = False
            screen.fill((0, 0, 0))

        if is_check:
            board.draw_check_warning(current_player_color)

        if is_piece_draging:
            board.draw_valid_moves(focused_piece)

        board.update()

        screen.blit(board, (board_offset_x, board_offset_y))

        if is_promoted:
            dialog.draw(screen)

        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()

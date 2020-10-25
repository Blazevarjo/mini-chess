import pygame

from board import Board

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 800


def main():
    pygame.init()

    is_piece_draging = False
    focused_piece = None

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    board = Board()

    board_offset_x = (screen.get_width() - board.get_width()) // 2
    board_offset_y = (screen.get_height() - board.get_height()) // 2

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left Mouse Button
                    x = event.pos[0] - board_offset_x
                    y = event.pos[1] - board_offset_y

                    focused_piece = board.get_collided_piece((x, y))

                    if focused_piece is not None:
                        is_piece_draging = True
                        mouse_offset_x = focused_piece.rect.x - x
                        mouse_offset_y = focused_piece.rect.y - y

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_piece_draging = False
                    if focused_piece is not None:
                        focused_piece.set_new_position()

            elif event.type == pygame.MOUSEMOTION:
                if is_piece_draging:
                    mouse_x, mouse_y = event.pos

                    # move a piece
                    focused_piece.rect.x = mouse_x - board_offset_x + mouse_offset_x
                    focused_piece.rect.y = mouse_y - board_offset_y + mouse_offset_y

        # update objects on screen
        board.update()

        screen.blit(board, (board_offset_x, board_offset_y))
        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()

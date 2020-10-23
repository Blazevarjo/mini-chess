import pygame
from board import Board


def main():
    pygame.init()

    is_piece_draging = False
    focused_piece = None

    board_offset_x = 0
    board_offset_y = 0

    screen = pygame.display.set_mode((900, 800))
    clock = pygame.time.Clock()
    board = Board()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left Mouse Button
                    x = event.pos[0] - board_offset_x
                    y = event.pos[1] - board_offset_y

                    focused_piece = board.GetCollidedPiece((x, y))

                    if focused_piece is not None:
                        is_piece_draging = True
                        mouse_offset_x = focused_piece.rect.x - x
                        mouse_offset_y = focused_piece.rect.y - y

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_piece_draging = False
                    if focused_piece is not None:
                        focused_piece.SetNewPosition()

            elif event.type == pygame.MOUSEMOTION:
                if is_piece_draging:
                    mouse_x, mouse_y = event.pos

                    # move a piece
                    focused_piece.rect.x = mouse_x - board_offset_x + mouse_offset_x
                    focused_piece.rect.y = mouse_y - board_offset_y + mouse_offset_y

        screen.blit(board, (board_offset_x, board_offset_y))
        
        # update objects on screen
        board.sprites_group.draw(screen)
        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()

import pygame

from board import Board

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 800


def main():
    pygame.init()

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

        # sprites_group.draw(screen)
        pygame.display.flip()

        screen.blit(board, (board_offset_x, board_offset_y))

        clock.tick(60)


if __name__ == "__main__":
    main()

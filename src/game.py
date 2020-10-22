import pygame
from board import Board
from pieces import Bishop, Rook


def main():
    pygame.init()

    screen = pygame.display.set_mode((900, 800))
    clock = pygame.time.Clock()
    board = Board()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # sprites_group.draw(screen)
        pygame.display.flip()

        screen.blit(board, (200, 100))

        clock.tick(60)


if __name__ == "__main__":
    main()

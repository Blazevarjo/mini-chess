import pygame
from pieces import Bishop, Rook


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    running = True
    sprites_group = pygame.sprite.Group()
    rook1 = Rook('B', 0, 0)
    rook2 = Rook('W', 1, 0)
    bishop1 = Bishop('W', 2, 0)

    sprites_group.add([rook1, rook2, bishop1])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        sprites_group.draw(screen)
        clock.tick(60)


if __name__ == "__main__":
    main()

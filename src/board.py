import pygame

from pieces import (
    King,
    Knight,
    Pawn,
    Rook,
    Queen
)


class Board(pygame.Surface):
    def __init__(self):
        super().__init__([520, 521])
        self.image = pygame.image.load('assets/Chess_Board.png')
        self.blit(self.image, [0, 0])
        self.array = [
            [Rook('B', 0, 0), Knight('B', 1, 0), King('B', 2, 0),
             Queen('B', 3, 0), Knight('B', 4, 0), Rook('B', 5, 0)],
            [Pawn('B', x, 1) for x in range(6)],
            [None for x in range(6)],
            [None for x in range(6)],
            [Pawn('W', x, 4) for x in range(6)],
            [Rook('W', 0, 5), Knight('W', 1, 5), King('W', 2, 5),
             Queen('W', 3, 5), Knight('W', 4, 5), Rook('W', 5, 5)]
        ]
        sprites_group = pygame.sprite.Group()

        # flatten 2d array and get only valid pieces to draw (delete None values)
        self.sprites = [
            piece for row in self.array for piece in row if piece is not None]

        sprites_group.add(self.sprites)
        sprites_group.draw(self)

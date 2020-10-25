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
        super().__init__([520, 519])
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

        # flatten 2d array and get only valid pieces to draw (delete None values)
        self.sprites = [
            piece for row in self.array for piece in row if piece is not None]

        self.sprites_group = pygame.sprite.Group()
        self.sprites_group.add(self.sprites)

    # update sprites on screen and draw them
    def update(self):
        self.blit(self.image, [0, 0])
        self.sprites_group.draw(self)

    # checking all pieces which can collide with given coords
    def get_collided_piece(self, pos):
        for piece in self.sprites:
            if piece.rect.collidepoint(pos):
                return piece

        return None

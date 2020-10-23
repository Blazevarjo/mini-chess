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
            [Rook('W', 0, 0), Knight('W', 1, 0), Queen('W', 2, 0),
             King('W', 3, 0), Knight('W', 4, 0), Rook('W', 5, 0)],
            [Pawn('W', x, 1) for x in range(6)],
            [None for x in range(6)],
            [None for x in range(6)],
            [Pawn('B', x, 4) for x in range(6)],
            [Rook('B', 0, 5), Knight('B', 1, 5), Queen('B', 2, 5),
             King('B', 3, 5), Knight('B', 4, 5), Rook('B', 5, 5)]
        ]

        # flatten 2d array and get only valid pieces to draw (delete None values)
        self.sprites = [
            piece for row in self.array for piece in row if piece is not None]

        self.sprites_group = pygame.sprite.Group()
        self.sprites_group.add(self.sprites)

    # update sprites on screen and draw them
    def Update(self, screen):        
        pass

    # checking all pieces which can collide with given coords
    def GetCollidedPiece(self, pos):
        for piece in self.sprites:
            if piece.rect.collidepoint(pos):
                return piece

        return None

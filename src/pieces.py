import pygame


class Piece(pygame.sprite.Sprite):
    symbol = None
    piece_name = None

    def __init__(self, color, x, y):
        super().__init__()
        self.color = color
        self.x = x
        self.y = y
        self.image = pygame.image.load(
            f"assets/pieces/{self.piece_name}{self.color}.png")
        self.rect = self.image.get_rect()
        self.rect.x = 18 + 80*x
        self.rect.y = 23 + 80*y

    def __str__(self):
        return f'{self.piece_name} x:{self.x} y:{self.y}'


class Bishop(Piece):
    symbol = 'B'
    piece_name = "Bishop"


class King(Piece):
    symbol = 'K'
    piece_name = 'King'


class Knight(Piece):
    symbol = 'N'
    piece_name = 'Knight'


class Pawn(Piece):
    symbol = 'P'
    piece_name = 'Pawn'


class Queen(Piece):
    symbol = 'Q'
    piece_name = 'Queen'


class Rook(Piece):
    symbol = 'R'
    piece_name = 'Rook'

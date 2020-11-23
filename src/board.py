import pygame

from pieces import (
    Bishop, King,
    Knight,
    Pawn, Piece,
    Rook,
    Queen,
    WHITE, BLACK
)


class Board(pygame.Surface):
    def __init__(self):
        super().__init__([520, 519])
        self.image = pygame.image.load('assets/Chess_Board.png')
        self.blit(self.image, [0, 0])
        self.array = [
            [Rook(BLACK, 0, 0), Knight(BLACK, 1, 0), King(BLACK, 2, 0),
             Queen(BLACK, 3, 0), Knight(BLACK, 4, 0), Rook(BLACK, 5, 0)],
            [Pawn(BLACK, x, 1) for x in range(6)],
            [None for x in range(6)],
            [None for x in range(6)],
            [Pawn(WHITE, x, 4) for x in range(6)],
            [Rook(WHITE, 0, 5), Knight(WHITE, 1, 5), King(WHITE, 2, 5),
             Queen(WHITE, 3, 5), Knight(WHITE, 4, 5), Rook(WHITE, 5, 5)]
        ]

        # flatten 2d array and get only valid pieces to draw (delete None values)
        self.sprites = [
            piece for row in self.array for piece in row if piece is not None]

        self.sprites_group = pygame.sprite.Group()
        self.sprites_group.add(self.sprites)

    # update sprites on screen and draw them
    def blit_self(self):
        self.blit(self.image, [0, 0])

    def update(self):
        self.sprites_group.draw(self)

    # checking all pieces which can collide with given coords
    # and color (only one player can play at the same time!)
    def get_collided_piece(self, pos, color):
        for piece in self.sprites:
            if piece.rect.collidepoint(pos) and piece.color == color:
                return piece

        return None

    def set_piece_position(self, focused_piece):
        old_y, old_x = focused_piece.y, focused_piece.x

        # assign new position of piece to board array
        focused_piece.set_new_position(self.array)

        attacked_piece = self.array[focused_piece.y][focused_piece.x]

        # when piece didn't move
        if attacked_piece is self.array[old_y][old_x]:
            return False

        # set old position to None
        self.array[old_y][old_x] = None

        # remove attacked piece
        if attacked_piece is not None and attacked_piece is not focused_piece:
            attacked_piece.kill()
            self.sprites.remove(attacked_piece)

        self.array[focused_piece.y][focused_piece.x] = focused_piece

        # dev env
        for row in self.array:
            for piece in row:
                print(f'{str(piece):^20}', end='')
            print()
        print()

        return True

    def draw_valid_moves(self, piece):
        for x, y in piece.valid_moves_position(self.array):
            pygame.draw.rect(self, [255, 0, 0], [x+10, y + 10, 60, 60], 5)

    def draw_check_warning(self, color):
        for row in self.array:
            for piece in row:
                if piece is not None and piece.color == color and piece.piece_name == "King":
                    pygame.draw.rect(self, [255, 0, 0], [piece.rect.x + 10, piece.rect.y + 10, 60, 60], 5)
                    return


    def is_check(self, current_player):
        player_pieces = [
            piece for row in self.array for piece in row if piece is not None and piece.color == current_player]
        moves = set()

        for piece in player_pieces:
            moves.update(piece.valid_moves(self.array))

        opponent_color = current_player = BLACK if current_player == WHITE else WHITE

        opponent_king = None

        for row in self.array:
            for piece in row:
                if piece is not None and piece.color == opponent_color and piece.piece_name == "King":
                    opponent_king = piece
                    break

        return (opponent_king.x, opponent_king.y) in moves

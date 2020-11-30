import pygame


class Button():
    def __init__(self, y, piece, color):
        self.image_normal = pygame.image.load(
            f'assets/pieces/{piece}{color}.png')

        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.rect.topright = (150, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


class Dialog():
    def __init__(self, color):
        self.rook = Button(150, 'Rook', color)
        self.knight = Button(250, 'Knight', color)
        self.queen = Button(350, 'Queen', color)

        self.piece_choose = None

    def draw(self, surface):
        self.rook.draw(surface)
        self.knight.draw(surface)
        self.queen.draw(surface)

    def handle_events(self, event):
        if self.rook.is_clicked(event):
            self.piece_choose = 'R'
        elif self.knight.is_clicked(event):
            self.piece_choose = 'N'
        elif self.queen.is_clicked(event):
            self.piece_choose = 'Q'

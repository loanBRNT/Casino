import pygame
class Button(pygame.sprite.Sprite):
    ''' Create a button clickable with changing hover color'''
    def __init__(self, text="Click",
                pos=(0,0), fontsize=16,
                colors="white on blue", hover_colors="red on green",
                command=lambda: print("No command activated for this button")):
        super().__init__()
        self.text = text
        self.command = command
        self.colors = colors
        self.original_colors = colors
        self.fg, self.bg = self.colors.split(" on ")
        self.fgh, self.bgh = hover_colors.split(" on ")
        self.font = pygame.font.SysFont("Arial", fontsize)
        self.pos = pos
        self.create_original()
        self.create_hover_image()
    def create_original(self):
        self.image = self.create_bg(self.text, self.fg, self.bg)
        self.original_image = self.image.copy()
    def create_hover_image(self):
        self.hover_image = self.create_bg(self.text, self.fgh, self.bgh)
        self.pressed = 1

    def create_bg(self, text, fg, bg):
        self.text = text
        image = self.font.render(self.text, 1, fg)
        self.rect = image.get_rect()
        self.rect.x, self.rect.y = self.pos
        bgo = pygame.Surface((self.rect.w, self.rect.h))
        bgo.fill(bg)
        bgo.blit(image, (0,0))
        return bgo
    def update(self):
        ''' CHECK IF HOVER AND IF CLICK THE BUTTON '''
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.hover_image
            self.check_if_click()
        else:
            self.image = self.original_image
    def check_if_click(self):
        ''' checks if you click on the button and makes the call to the action just one time'''
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and self.pressed == 1:
                # print("Execunting code for button '" + self.text + "'")
                self.command()
                self.pressed = 0
            if pygame.mouse.get_pressed() == (0,0,0):
                self.pressed = 1

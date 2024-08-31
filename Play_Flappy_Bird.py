import pygame
import os
import random

pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

# Load images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("Lato", 50)
BUTTON_FONT = pygame.font.SysFont("comicsans", 40)


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (4, 35, 89))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)

    bird.draw(win)
    pygame.display.update()

def draw_start_screen(win):
    # Draw the background
    win.blit(BG_IMG, (0, 0))

    logo_img = pygame.image.load(os.path.join("imgs", "logo.png"))
    logo_img = pygame.transform.scale(logo_img, (420, 100))  # Resize image to 300x150 pixels
    logo_rect = logo_img.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 100))
    win.blit(logo_img, logo_rect.topleft)

    # Load and draw the start button image
    start_img = pygame.image.load(os.path.join("imgs", "start.png"))
    start_img = pygame.transform.scale(start_img, (240, 100))  # Resize image to 200x100 pixels
    start_rect = start_img.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2+210))
    win.blit(start_img, start_rect.topleft)

    pygame.display.update()
    return start_rect


def draw_game_over(win, score):
    # Load and resize the game over image
    game_over_img = pygame.image.load(os.path.join("imgs", "game_over.png"))
    game_over_img = pygame.transform.scale(game_over_img, (300, 250))  # Resize image to 300x250 pixels

    # Draw the resized image
    img_rect = game_over_img.get_rect(center=(WIN_WIDTH // 2 + 25, WIN_HEIGHT // 2 - 90))
    win.blit(game_over_img, img_rect.topleft)

    # Load and draw the play button image
    play_img = pygame.image.load(os.path.join("imgs", "play.png"))
    play_img = pygame.transform.scale(play_img, (200, 100))  # Resize image to 200x100 pixels
    play_rect = play_img.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 105))
    win.blit(play_img, play_rect.topleft)

    # Load and draw the quit button image
    quit_img = pygame.image.load(os.path.join("imgs", "quit_button.png"))
    quit_img = pygame.transform.scale(quit_img, (200, 100))  # Resize image to 200x100 pixels
    quit_rect = quit_img.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 200))
    win.blit(quit_img, quit_rect.topleft)

    pygame.display.update()
    return play_rect, quit_rect


def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    # Show start screen
    start_rect = draw_start_screen(win)
    game_started = False

    while not game_started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos):
                    game_started = True
                    break

    # Game loop
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    score = 0
    game_over = False

    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if play_rect and play_rect.collidepoint(mouse_pos):
                        main()  # Restart the game
                    if quit_rect and quit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        quit()
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bird.jump()

        if not game_over:
            bird.move()
            add_pipe = False
            rem = []
            for pipe in pipes:
                pipe.move()
                if pipe.collide(bird):
                    game_over = True

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if add_pipe:
                pipes.append(Pipe(600))
                score += 1

            for r in rem:
                pipes.remove(r)

            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                game_over = True

            base.move()
            draw_window(win, bird, pipes, base, score)
        else:
            play_rect, quit_rect = draw_game_over(win, score)


if __name__ == "__main__":
    main()

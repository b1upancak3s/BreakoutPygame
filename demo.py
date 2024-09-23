import random

import pygame

pygame.init()

screen = pygame.display.set_mode((1280,720))

clock = pygame.time.Clock()

speed = 13

brick_list = []

color_list = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']


class Player(pygame.Rect):

    def __init__(self, x, y):
        super().__init__(x, y, 100, 25)   # arbitrary values
        self.vx = 0

    def draw(self):
        pygame.draw.rect(screen, 'white', self, 0) # fill
        pygame.draw.rect(screen, 'blue', self, 1) # outline

    def update(self):
        self.x += self.vx
        if (player.x + player.width) >= screen.get_width():
            player.x = screen.get_width() - player.width
        elif player.x <= 0:
            player.x = 0

class Ball(pygame.Rect):

    def __init__(self, x, y, diameter):
        super().__init__(x, y, diameter, diameter)
        self.vx = random.randint(3, 5) * random.choice([1, -1])
        self.vy = random.randint(3, 5)

    def draw(self):
        pygame.draw.ellipse(screen, 'white', self, 0)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if ball.x < 0 or ball.x > screen.get_width() - ball.width:
            ball.vx *= -1
        if ball.y < 0:
            ball.vy *= -1

class Brick(pygame.Rect):

    def __init__(self, x, y, color):
        super().__init__(x, y, 100, 30)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self, 0)
        pygame.draw.rect(screen, 'white', self, 1)

# create game objects
player = Player(screen.get_width()/2 - 50, screen.get_height() - 50)
ball = Ball(screen.get_width()/2, screen.get_height()/2, 20)
for y in range(0, 3):
    for x in range(0, 10):
        brick_list.append(Brick(x * 128 + 10, y * 50 + 10, color_list[random.randint(0, 5)]))

while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.vx += -1 * speed
            if event.key == pygame.K_d:
                player.vx += speed
            if event.key == pygame.K_r:
                ball.x = screen.get_width()/2
                ball.y = screen.get_height()/2
                ball.vx = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.vx += speed
            if event.key == pygame.K_d:
                player.vx += -1 * speed

    # Do logical updates here.
    player.update()
    ball.update()
    if ball.colliderect(player):
        ball.vy *= -1
        ball.y = player.y - ball.width
        diff = (ball.x + ball.w/2) - (player.x + player.w/2)
        ball.vx += diff//2
        if ball.x <= player.x + player.width/2:
            ball.vx = -1 * random.randint(3, 5)
        else:
            ball.vx = random.randint(3, 5)
    for bricks in brick_list:
        if ball.colliderect(bricks):
            temp_vx = ball.vx
            temp_vy = ball.vy
            ball.vy *= -1
            diff = (ball.x + ball.w / 2) - (bricks.x + bricks.w / 2)
            ball.vx += diff // 2
            if ball.x <= bricks.x + bricks.width / 2:
                ball.vx = -1 * random.randint(3, 5)
            else:
                ball.vx = random.randint(3, 5)
            brick_list.remove(bricks)



    screen.fill('black')  # Fill the display with a solid color

    # Render the graphics here.
    player.draw()
    ball.draw()
    for i in brick_list:
        i.draw()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)
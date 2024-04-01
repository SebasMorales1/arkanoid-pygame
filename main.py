import pygame
from entities import *

# Configs
SCREEN_SIZE = (420, 580)
BG_COLOR = (1, 11, 43)
PLAYER_WIDTH = 120
PLAYER_INITIAL_POS = ((SCREEN_SIZE[0]-PLAYER_WIDTH)//2, SCREEN_SIZE[1]-40) 

BALL_RADIUS = 8
BALL_INITIAL_STICKED = PLAYER_WIDTH//2
BALL_INITIAL_POS = (PLAYER_INITIAL_POS[0]+BALL_INITIAL_STICKED, PLAYER_INITIAL_POS[1]-BALL_RADIUS)

def main():
    pygame.init()
    pygame.display.set_caption("Arkanoid clone - pygame")
    screen = pygame.display.set_mode(SCREEN_SIZE)

    running = True
    
    player = Player(list(PLAYER_INITIAL_POS), PLAYER_WIDTH)
    ball = Ball(list(BALL_INITIAL_POS), BALL_RADIUS, BALL_INITIAL_STICKED)
    clock = pygame.time.Clock()

    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == 32:
                    if ball.state == 0:
                        ball.ydirection = -1
                        ball.state = 1

        keys = pygame.key.get_pressed()
        player.movement(keys)
        player.check_collision(SCREEN_SIZE[0])

        ball.movement(player.pos)
        ball.check_collision_with_player(player.pos, player.width)
        ball.check_collision(SCREEN_SIZE[0])

        screen.fill(BG_COLOR)
        player.draw(screen)
        ball.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()

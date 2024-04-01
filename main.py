import pygame
import sys
import os
from entities import *

# Configs
SCREEN_SIZE = (420, 580)
BG_COLOR = (1, 11, 43)
PLAYER_WIDTH = 120
PLAYER_INITIAL_POS = ((SCREEN_SIZE[0]-PLAYER_WIDTH)//2, SCREEN_SIZE[1]-40) 

BALL_RADIUS = 8
BALL_INITIAL_STICKED = PLAYER_WIDTH//2
BALL_INITIAL_POS = (PLAYER_INITIAL_POS[0]+BALL_INITIAL_STICKED, PLAYER_INITIAL_POS[1]-BALL_RADIUS)

WHITE = (255, 255, 255)
GRAY1 = (212, 212, 212)
AQUA = (171, 245, 245)

def main():
    pygame.init()
    pygame.display.set_caption("Arkanoid clone - pygame")
    screen = pygame.display.set_mode(SCREEN_SIZE)

    running = True
    gameover = False
    
    player = Player(list(PLAYER_INITIAL_POS), PLAYER_WIDTH)
    ball = Ball(list(BALL_INITIAL_POS), BALL_RADIUS, BALL_INITIAL_STICKED)
    clock = pygame.time.Clock()

    font_route = os.path.join(os.path.dirname(__file__), "gameover.ttf")
    font = pygame.font.Font(font_route, 25)
    font2 = pygame.font.Font(font_route, 15)

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
                    elif gameover:
                        # Restart player and ball props
                        gameover = False
                        player.pos = list(PLAYER_INITIAL_POS)

                        ball.state = 0
                        ball.pos = list(BALL_INITIAL_POS)
                        ball.sticked = BALL_INITIAL_STICKED
                        ball.xdirection = 0
                        ball.ydirection = 0

                        continue

        if ball.pos[1] > SCREEN_SIZE[1]:
            gameover = True

            gameover_text = font.render("GAMEOVER", True, WHITE)
            score = font2.render(f"Score: {0}", True, GRAY1)
            max_score = font2.render(f"Max score: {0}", True, GRAY1)
            restart_text = font2.render(f"<space> Play again", True, AQUA)

            screen.fill(BG_COLOR)
            screen.blit(score, (20,140))
            screen.blit(max_score, (20,180))
            screen.blit(gameover_text, (SCREEN_SIZE[0]//2 - gameover_text.get_width()//2, 80))
            screen.blit(restart_text, (SCREEN_SIZE[0]//2 - restart_text.get_width()//2, SCREEN_SIZE[1]-100))

            pygame.display.flip()
            continue

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
    pygame.quit()
    sys.exit()

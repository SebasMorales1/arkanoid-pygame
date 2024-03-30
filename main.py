import pygame

class Collision_with_bordersTrait:
    def __init__(self, pos, width):
        self.pos = pos
        self.width = width

    def check_collision(self, screen_size, type_shape):
        if self.pos[0] < 0:
            self.pos[0] = 0 if type_shape == "rect" else self.width
            return (-1,0)
        elif self.pos[0] > screen_size[0]-self.width:
            self.pos[0] = screen_size[0]-self.width
            return (1,0)
        elif self.pos[1] < 0:
            self.pos[1] = 0 if type_shape == "rect" else self.width
            return (0,-1)

class Player(Collision_with_bordersTrait):
    def __init__(self, pos, width):
        self.color = (46, 151, 199)
        self.speed = 15
        self.width = width
        self.pos = pos

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.pos, (self.width,20)))

    def movement(self, keys):
        if keys[pygame.K_RIGHT]:
            self.pos[0] += self.speed
        elif keys[pygame.K_LEFT]:
            self.pos[0] += -self.speed

class Ball(Collision_with_bordersTrait):
    def __init__(self, pos, width, sticked):
        self.color = (255, 255, 255)
        self.speed = 7
        self.state = 0 # State = 0: sticky 1: in movement
        self.width = width
        self.xdirection = 0
        self.ydirection = 0
        self.pos = pos
        self.sticked = sticked

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.width)

    def movement(self, player_pos):
        if self.state == 0:
            self.pos[0] = player_pos[0] + self.sticked
        elif self.state == 1:
            self.pos[0] += (self.speed-1)*self.xdirection
            self.pos[1] += self.speed*self.ydirection

    def check_collision(self, screen_size):
        collision = super().check_collision(screen_size, "ball")
        
        if collision:
            if collision[1]:
                self.ydirection = -collision[1]
            if collision[0]:
                self.xdirection = -collision[0]

    def check_collision_with_player(self, player_pos, player_width):
        # Get the area occupied by the player and the ball on the x-axis 
        xplayer_area = (player_pos[0], player_pos[0]+player_width)
        xball_area = (self.pos[0], self.pos[0]+self.width)

        yplayer_area = (player_pos[1], player_pos[1]+20)
        yball_area = (self.pos[1], self.pos[1]+self.width)
        collisioned_x = xball_area[0] >= xplayer_area[0] and xball_area[1] <= xplayer_area[1]
        collisioned_y = yball_area[1] >= yplayer_area[0]-self.width and yball_area[0] <= yplayer_area[0]
        collisioned_only_x = collisioned_x and yball_area[0] < yplayer_area[1] and yball_area[1] > yplayer_area[0]

        center = player_width//2+player_pos[0]
        collision_side = 1 if self.pos[0] > center else -1 if self.pos[0] < center else 0

        if collisioned_x and collisioned_y and self.state != 0:
            self.ydirection = -1
            if self.xdirection == 0 and collision_side != 0:
                self.xdirection = collision_side
        elif collisioned_only_x:
            self.pos[0] += collision_side
            self.xdirection = collision_side
            self.xangle += 10*collision_side

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
        player.check_collision(SCREEN_SIZE, "rect")

        ball.movement(player.pos)
        ball.check_collision_with_player(player.pos, player.width)
        ball.check_collision(SCREEN_SIZE)

        screen.fill(BG_COLOR)
        player.draw(screen)
        ball.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()

import pygame

class Player:
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
    
    def check_collision(self, screen_size):
        if self.pos[0] < 0:
            self.pos[0] = 0
        elif self.pos[0] + self.width > screen_size:
            self.pos[0] = screen_size - self.width

class Ball:
    def __init__(self, pos, radius, sticked):
        self.color = (255, 255, 255)
        self.speed = 3
        self.state = 0 # State = 0: sticky 1: in movement
        self.radius = radius
        self.xdirection = 0
        self.ydirection = 0
        self.pos = pos
        self.sticked = sticked

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)

    def movement(self, player_pos):
        if self.state == 0:
            self.pos[0] = player_pos[0] + self.sticked
        elif self.state == 1:
            self.pos[0] += (self.speed-1)*self.xdirection
            self.pos[1] += self.speed*self.ydirection

    def check_collision(self, screen_size):
        if self.pos[1] - self.radius < 0:
            self.ydirection = 1
        elif self.pos[0] - self.radius < 0:
            self.xdirection = 1
        elif self.pos[0] + self.radius > screen_size:
            self.xdirection = -1

    def check_collision_with_player(self, player_pos, player_width):
        # Get the area occupied by the player and the ball on the x-axis 
        xplayer_area = (player_pos[0], player_pos[0]+player_width)
        xball_area = (self.pos[0], self.pos[0]+self.radius)

        yplayer_area = (player_pos[1], player_pos[1]+20)
        yball_area = (self.pos[1], self.pos[1]+self.radius)
        collisioned_x = xball_area[0] >= xplayer_area[0] and xball_area[1] <= xplayer_area[1]
        collisioned_y = yball_area[1] >= yplayer_area[0]-self.radius and yball_area[0] <= yplayer_area[0]
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

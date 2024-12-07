import pygame, sys, random 

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,680))
    screen.blit(floor_surface,(floor_x_pos + 288,680))

class roo(pygame.sprite.Sprite):
    def __init__(self): 
        super().__init__()
        #roo_jump1 = pygame.transform.scale2x(pygame.image.load('roo_jump1.png').convert_alpha())
        #roo_jump2 = pygame.transform.scale2x(pygame.image.load('roo_jump2.png').convert_alpha())
        #roo_jump3 = pygame.transform.scale2x(pygame.image.load('roo_jump3.png').convert_alpha())
        #roo_jump4 = pygame.transform.scale2x(pygame.image.load('roo_jump4.png').convert_alpha())
        #roo_jump5 = pygame.transform.scale2x(pygame.image.load('roo_jump5.png').convert_alpha())
        #roo_jump6 = pygame.transform.scale2x(pygame.image.load('roo_jump6.png').convert_alpha())
        #self.roo_frames = [roo_jump1, roo_jump2,roo_jump3,roo_jump4,roo_jump5,roo_jump6]
        #self.roo_index = 0
        #self.roo_surface = self.roo_frames[roo_index]
        #self.roo_rect = self.roo_surface.get_rect(center = (100,458))
        #self.gravity = 0
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.roo_rect.bottom >= 600:
         self.gravity = 0.25

    def apply_gravity(self):
        self.gravity += 1
        self.roo_rect.y += self.gravity
        if self.roo_rect.bottom >= 600:
            self.roo_rect.bottom = 600

    #def roo_animation(self):
    #       self.new_roo = self.roo_frames[roo_index]
    #      self.new_roo_rect = self.new_roo.get_rect(center = (100,self.roo_rect.centery))
    #     return self.new_roo,self.new_roo_rect

    def update(self):
        self.player_input()
        self.apply_gravity()

def create_cactus():
    random_cactus_pos = random.choice(cactus_height)
    bottom_cactus = cactus_surface.get_rect(midtop = (900,random_cactus_pos))
    #top_cactus = cactus_surface.get_rect(midbottom = (900,random_cactus_pos - 300))
    return bottom_cactus#,top_cactus

def move_cactus(cactuses):
    for cactus in cactuses:
        cactus.centerx -= 5
    visible_cactuses = [cactus for cactus in cactuses if cactus.right > -10]
    return visible_cactuses

def draw_cactus(cactuses):
    for cactus in cactuses:
        screen.blit(cactus_surface,cactus)

def check_collision(cactuses):
    global can_score
    for cactus in cactuses:
        if roo_rect.colliderect(cactus):
            death_sound.play()
            can_score = True
            return False

def roo_animation():
    new_roo = roo_frames[roo_index]
    new_roo_rect = new_roo.get_rect(center = (100,roo_rect.centery))
    return new_roo,new_roo_rect

def rotate_roo(roo):
    new_roo = pygame.transform.rotozoom(roo,-roo_movement * 2,1)
    return new_roo


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (512,60))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
        score_rect = score_surface.get_rect(center = (512,60))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (512,670))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def cactus_score_check():
    global score, can_score 
    
    if cactus_list:
        for cactus in cactus_list:
            if 95 < cactus.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if cactus.centerx < 0:
                can_score = True

# pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 2, buffer = 1024)
pygame.init()
screen = pygame.display.set_mode((1024, 800))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',50)

# Game Variables
roo_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

bg_surface = pygame.image.load('background.png').convert_alpha()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('floor.png').convert_alpha()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

roo_jump1 = pygame.transform.scale2x(pygame.image.load('roo_jump1.png').convert_alpha())
roo_jump2 = pygame.transform.scale2x(pygame.image.load('roo_jump2.png').convert_alpha())
roo_jump3 = pygame.transform.scale2x(pygame.image.load('roo_jump3.png').convert_alpha())
roo_jump4 = pygame.transform.scale2x(pygame.image.load('roo_jump4.png').convert_alpha())
roo_jump5 = pygame.transform.scale2x(pygame.image.load('roo_jump5.png').convert_alpha())
roo_jump6 = pygame.transform.scale2x(pygame.image.load('roo_jump6.png').convert_alpha())
roo_frames = [roo_jump1, roo_jump2,roo_jump3,roo_jump4,roo_jump5,roo_jump6]
roo_index = 0
roo_surface = roo_frames[roo_index]
roo_rect = roo_surface.get_rect(center = (100,458))
gravity = 0

#timer 
ROOJUMP = pygame.USEREVENT + 1
pygame.time.set_timer(ROOJUMP,200)

cactus_surface = pygame.image.load('Sprite-0001-cactus.png')
cactus_surface = pygame.transform.scale2x(cactus_surface)
cactus_list = []
SPAWNCACTUS = pygame.USEREVENT
pygame.time.set_timer(SPAWNCACTUS,1800)
cactus_height = [600]

game_over_surface = pygame.transform.scale2x(pygame.image.load('guide 1.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (512,380))

#import sound effect
jump_sound = pygame.mixer.Sound('sound/sfx_swooshing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
bg_music = pygame.mixer.Sound('sound/bg_music.wav')
bg_music.play(loops = -1)

SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT,100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        else:
            #if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_SPACE and game_active:
             #   roo_movement = 0
              #  roo_movement -= 6
               # jump_sound.play()
            if event.type == pygame.K_SPACE and game_active == True:
                game_active = False
                cactus_list.clear()
                roo_rect.center = (100,580)
                roo_movement = 0
                score = 0

        if event.type == SPAWNCACTUS:
            cactus_list.append(create_cactus())

        if event.type == ROOJUMP:
            if roo_index < 5:
                roo_index += 1
            else:
                roo_index = 0

            roo_surface,roo_rect = roo_animation()
    
    screen.blit(bg_surface,(0,0))

    if game_active:
        # Roos
        rotated_roo = rotate_roo(roo_surface)
        roo_rect.centery += roo_movement
        screen.blit(rotated_roo,roo_rect)
        game_active = check_collision(cactus_list)

        # cactus
        cactus_list = move_cactus(cactus_list)
        draw_cactus(cactus_list)

        # Score
        cactus_score_check()
        score_display('main_game')
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')


    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -700:    
        floor_x_pos = 0


    pygame.display.update()
    clock.tick(120)


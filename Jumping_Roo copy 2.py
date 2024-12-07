#Group Name : Lima
# Hao Liu(Lucas) ID: 350622
# FuYan Xu(Alice)ID: 347105
# LiYao Li       ID: 347018
 
import pygame, sys, random 

def draw_floor():
	screen.blit(floor_surface,(floor_x_pos,680))   #use screen.blit funtion to blit the floor surface into the screen
	screen.blit(floor_surface,(floor_x_pos + 288,680))

def create_cactus():
	bottom_cactus = cactus_surface.get_rect(midtop = (1000,600))  #place the cactus position
	return bottom_cactus

def move_cactus(cactuses):  #create a function to move cactus
	for cactus in cactuses:
		cactus.centerx -= 5   #take all the rect move to the left 
	visible_cactuses = [cactus for cactus in cactuses if cactus.right > -10]
	return visible_cactuses

def draw_cactus(cactuses):
	for cactus in cactuses:
		screen.blit(cactus_surface,cactus)
		
def check_collision(cactuses):   #create a function to check the collision
	global can_score
	for cactus in cactuses:
		if roo_rect.colliderect(cactus):  #if any cactus rect colliderect with roo_rect
			death_sound.play()
			can_score = True
			return False

	return True


def roo_animation():
	new_roo = roo_frames[roo_index]
	new_roo_rect = new_roo.get_rect(center = (60,roo_rect.centery)) #take previous roo centery position when create a new roo surface
	return new_roo,new_roo_rect

def score_display(game_state):
	if game_state == 'main_game':   #create a score surface
		score_surface = game_font.render(str(int(score)),True,(255,255,255))
		score_rect = score_surface.get_rect(center = (512,60))
		screen.blit(score_surface,score_rect)
	if game_state == 'game_over':  #use f str to put both text and number on the score surface
		score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
		score_rect = score_surface.get_rect(center = (512,60))
		screen.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (512,670))  #put high score in 670 y position 
		screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):     #create a function to update the score and high score
	if score > high_score:
		high_score = score
	return high_score

def cactus_score_check():   #create a function to check score
	global score, can_score   #use global function in pygame to modify the score when can_score is true
	
	if cactus_list:
		for cactus in cactus_list:
			if 95 < cactus.centerx < 105 and can_score:
				score += 1
				score_sound.play()
				can_score = False
			if cactus.centerx < 0:
				can_score = True

# pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((1024, 800))  #set pygame screen size to show the whole screen in my laptop screen
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',50)  #call pygame font function to import the text

# Game Variables
gravity = 0.25
roo_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

#import background
bg_surface = pygame.image.load('background.png').convert_alpha()
bg_surface = pygame.transform.scale2x(bg_surface)

#import floor 
floor_surface = pygame.image.load('floor.png').convert_alpha()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0 #floor orginal position as 0

#import Roo with different move posture to a frame list
roo_jump1 = pygame.transform.scale2x(pygame.image.load('roo_jump1.png').convert_alpha())
roo_jump2 = pygame.transform.scale2x(pygame.image.load('roo_jump2.png').convert_alpha())
roo_jump3 = pygame.transform.scale2x(pygame.image.load('roo_jump3.png').convert_alpha())
roo_jump4 = pygame.transform.scale2x(pygame.image.load('roo_jump4.png').convert_alpha())
roo_jump5 = pygame.transform.scale2x(pygame.image.load('roo_jump5.png').convert_alpha())
roo_jump6 = pygame.transform.scale2x(pygame.image.load('roo_jump6.png').convert_alpha())

# create a list to put all the roo surface
roo_frames = [roo_jump1, roo_jump2,roo_jump3,roo_jump4,roo_jump5,roo_jump6]
roo_index = 0
roo_surface = roo_frames[roo_index]#assign a specific index roo from frames into roo_surface
roo_rect = roo_surface.get_rect(center = (130,600))#set rectangle for Roo

#Timer 
ROOJUMP = pygame.USEREVENT + 1
pygame.time.set_timer(ROOJUMP,200)

#import cactus
cactus_surface = pygame.image.load('Sprite-0001-cactus.png') 
cactus_surface = pygame.transform.scale2x(cactus_surface)
cactus_list = []
SPAWNCACTUS = pygame.USEREVENT  #create a new variable triger by timer
pygame.time.set_timer(SPAWNCACTUS,1800) #every 1.8 second create a new cactus

#import game over surface and rect
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
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and roo_rect.bottom>=680 and game_active:
				roo_movement = 0
				roo_movement -= 9  #make roo move upwards 6 everytime when click space key
				jump_sound.play()
			if event.key == pygame.K_SPACE and game_active == False:  #when click space key and game is over, restart the game
				game_active = True
				cactus_list.clear()  #clear the cactus 
				roo_rect.center = (130,580)
				roo_movement = 0  #roo movement restart from 0
				score = 0  #score clear back to 0

		if event.type == SPAWNCACTUS:
			cactus_list.append(create_cactus())   #take any return form cactus list extend to create cactus function

		if event.type == ROOJUMP:
			if roo_index < 5:
				roo_index += 1  #increase roo index by 1
			else:
				roo_index = 0

			roo_surface,roo_rect = roo_animation()   #take each roo from the list to get a rect
    #blit backgroun surface into the screen 
	screen.blit(bg_surface,(0,0))

	if game_active:  #if game_active is true, run below code
		
        # Roos
		roo_movement += gravity
		if roo_rect.bottom >= 680:roo_rect.bottom = 680
		roo_rect.centery += roo_movement		
		screen.blit(roo_surface,roo_rect)
		game_active = check_collision(cactus_list)
		
		# cactus
		cactus_list = move_cactus(cactus_list)
		draw_cactus(cactus_list)
		
		# Score
		cactus_score_check()
		score_display('main_game')
	else:   #if game_active is not true, run below
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

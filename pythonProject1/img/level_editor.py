import pygame
import pickle
from os import path


pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
tile_size = 50
cols = 20
margin = 100
screen_width = 900
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')


#load images
bg_img = pygame.image.load('sky.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
dirt_img = pygame.image.load('dirt.png')
grass_img = pygame.image.load('grass.png')
blob_img = pygame.image.load('blob.png')
platform_x_img = pygame.image.load('platform_x.png')
platform_y_img = pygame.image.load('platform_y.png')
lava_img = pygame.image.load('lava.png')
coin_img = pygame.image.load('coin.png')
exit_img = pygame.image.load('exit.png')
# save_img = pygame.image.load('save_btn.png')
#load_img = pygame.image.load('load_btn.png')
deathcoin_img = pygame.image.load('meat.png')
opposum_img = pygame.image.load('opposum.png')
stone_img = pygame.image.load('stone.png')
ice_img = pygame.image.load("ice.png")


#define game variables
clicked = False
level = 1

#define colours
light_grey = (220, 220, 220)
white = (255, 255, 255)
green = (144, 201, 120)
blue = (140, 190, 213)

font = pygame.font.SysFont('Futura', 24)

#create empty tile list
world_data = []
for row in range(20):
	r = [0] * 20
	world_data.append(r)

#create boundary
for tile in range(0, 20):
	world_data[19][tile] = 1
	world_data[0][tile] = 1
	world_data[tile][0] = 1
	world_data[tile][19] = 1
	world_data[15][tile] = 1
	world_data[tile][17] = 1

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_grid():
	for c in range(21):
		#vertical lines
		pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height))
		#horizontal lines
		pygame.draw.line(screen, white, (0, c * tile_size), (screen_width, c * tile_size))


def draw_world():
	for row in range(20):
		for col in range(20):
			if world_data[row][col] > 0:
				if world_data[row][col] == 1:
					#dirt blocks
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 2:
					#grass blocks
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 3:
					#enemy blocks
					img = pygame.transform.scale(blob_img, (tile_size, int(tile_size * 0.75)))
					screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
				if world_data[row][col] == 4:
					#horizontally moving platform
					img = pygame.transform.scale(platform_x_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 5:
					#vertically moving platform
					img = pygame.transform.scale(platform_y_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 6:
					#lava
					img = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
				if world_data[row][col] == 7:
					#coin
					img = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))
					screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
				if world_data[row][col] == 8:
					#exit
					img = pygame.transform.scale(exit_img, (tile_size, int(tile_size * 1.5)))
					screen.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))
				if world_data[row][col] == 9:
					#deathcoin
					img = pygame.transform.scale(deathcoin_img, (tile_size // 2, tile_size // 2))
					screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
				if world_data[row][col] == 10:
					#enemy blocks
					img = pygame.transform.scale(opposum_img, (tile_size * 2, int(tile_size * 0.65)))
					screen.blit(img, (col * tile_size + (tile_size // -2), row * tile_size + (tile_size * 0.35)))
				if world_data[row][col] == 11:
					#stone blocks
					img = pygame.transform.scale(stone_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 12:
					#ice blocks
					img = pygame.transform.scale(ice_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))

#create load and save buttons


#main game loop
run = True
while run:
	key = pygame.key.get_pressed()
	if key[pygame.K_s]:
		pickle_out = open(f'level{level}_data', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
	if key[pygame.K_l]:
		if path.exists(f'level{level}_data'):
			pickle_in = open(f'level{level}_data', 'rb')
			world_data = pickle.load(pickle_in)

	clock.tick(fps)

	#draw background
	screen.fill(blue)
	screen.blit(bg_img, (0, 0))






	#show the grid and draw the level tiles
	draw_grid()
	draw_world()


	#text showing current level
	draw_text(f'Level: {level}', font, white, tile_size - 50, screen_height - 800)
	draw_text('Press UP or DOWN to change level', font, light_grey, tile_size - 50, screen_height - 785)
	draw_text('Press S or L to save the level or load the previous level', font, light_grey, tile_size - 50, screen_height - 768)
	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		#mouseclicks to change tiles
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // tile_size
			#check that the coordinates are within the tile area
			if x < 20 and y < 20:
				#update tile value
				if pygame.mouse.get_pressed()[0] == 1:
					world_data[y][x] += 1
					if world_data[y][x] > 12:
						world_data[y][x] = 0
				elif pygame.mouse.get_pressed()[2] == 1:
					world_data[y][x] -= 1
					if world_data[y][x] < 0:
						world_data[y][x] = 12
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		#up and down key presses to change level number
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			elif event.key == pygame.K_DOWN and level > 1:
				level -= 1

	#update game display window
	pygame.display.update()

pygame.quit()
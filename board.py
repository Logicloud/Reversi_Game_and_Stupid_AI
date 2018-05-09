import numpy as np
import sys
import time
import pygame
import pygame.gfxdraw
from pygame.locals import *
from Game import find_avail_points, priority, computer_player

class Reversi(object):

	def __init__(self):
		# White = 1, Black = -1, Available = 0
		# Black first
		self.length = 700
		self.width = 540

		self.executive = -1
		self.name = {1: 'White', -1: 'Black'}
		self.priority = priority()
		self.board = np.array([[ 0,  0,  0,  0,  0,  0,  0,  0],
							   [ 0,  0,  0,  0,  0,  0,  0,  0],
							   [ 0,  0,  0,  0,  0,  0,  0,  0],
							   [ 0,  0,  0,  1, -1,  0,  0,  0],
							   [ 0,  0,  0, -1,  1,  0,  0,  0],
							   [ 0,  0,  0,  0,  0,  0,  0,  0],
							   [ 0,  0,  0,  0,  0,  0,  0,  0],
							   [ 0,  0,  0,  0,  0,  0,  0,  0]])
		# self.board = np.array([[ -1,  1,  -1,  1,  -1,  1,  -1,  1],
		# 					   [ -1,  1,  -1,  1,  -1,  1,  -1,  1],
		# 					   [ -1,  1,  -1,  1,  -1,  1,  -1,  1],
		# 					   [ -1,  1,  -1,  1,  -1,  1,  -1,  1],
		# 					   [ -1,  1,  -1,  1,  -1,  1,  -1,  1],
		# 					   [ -1,  1,  -1,  1,  -1,  0,  -1,  1],
		# 					   [ -1,  1,  -1,  1,  -1,  1,  -1,  1],
		# 					   [ -1,  1,  -1,  1,  -1,  1,  -1,  1]])

	def draw_board(self):

		pygame.init()
		self.screen = pygame.display.set_mode((self.length, self.width))
		pygame.display.set_caption("Reversi")

		white = (255, 255, 255)
		black = (0, 0, 0)
		orange = (255, 128, 0)
		grey = (192, 192, 192)
		red = (255, 0, 0)
		background = (51, 153, 255)
		checker = (21,114,21)

		# Distance between checker and window boundaries
		boundary = 30
		line_width = 1

		row = 8
		column = 8

		# Grid size
		grid_width = 60
		grid_length = 60

		self.screen.fill(background)

		# Display mode choice
		pygame.draw.rect(self.screen, white, (100, 210, 175, 125))
		pygame.draw.rect(self.screen, white, (425, 210, 175, 125))
		pygame.draw.rect(self.screen, black, (100, 210, 175, 125), 2)
		pygame.draw.rect(self.screen, black, (425, 210, 175, 125), 2)

		printing_font = pygame.font.Font(None, 60)
		PVE_mode = printing_font.render("PVE", True, black)
		PVP_mode = printing_font.render("PVP", True, black)
		self.screen.blit(PVE_mode, (145, 255))
		self.screen.blit(PVP_mode, (470, 255))
		pygame.display.update()		
		
		# Check which mode is chosen
		fuse_1 = 0
		cont = True
		while cont and fuse_1 < 1000:
			fuse_1 += 1
			time.sleep(0.2)		

			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit()
				if event.type == MOUSEBUTTONDOWN:

					mode_c, mode_r = event.pos
					if 100 < mode_c < 275 and 210 < mode_r < 335:
						cont = False
						PVE = True
					elif 425 < mode_c < 600 and 210 < mode_r < 335:
						cont = False						
						PVE = False

		# If PVE mode is chosen, ask which color the user want to play
		# If user choose black, user play first. Otherwise, AI play first
		human_draw = True
		if PVE:
			pygame.draw.rect(self.screen, grey, (100, 210, 175, 125))
			pygame.draw.rect(self.screen, grey, (425, 210, 175, 125))
			pygame.draw.rect(self.screen, black, (100, 210, 175, 125), 2)
			pygame.draw.rect(self.screen, black, (425, 210, 175, 125), 2)

			printing_font = pygame.font.Font(None, 60)
			pygame.draw.circle(self.screen, white, (188, 273), grid_width/2-2, 0)
			pygame.draw.circle(self.screen, black, (188, 273), grid_width/2-2, 1)			
			pygame.draw.circle(self.screen, black, (513, 273), grid_width/2-2, 0)

			pygame.gfxdraw.box(self.screen, pygame.Rect(170,75,361,100), (255,255,255,100))

			printing_font = pygame.font.Font(None, 60)
			choose_color = printing_font.render("Choose color", True, black)
			printing_font = pygame.font.Font(None, 30)
			notification = printing_font.render("(Black first)", True, black)
			self.screen.blit(choose_color, (218, 95))
			self.screen.blit(notification, (298, 140))

			pygame.display.update()		
		
			fuse_2 = 0
			cont = True

			while cont and fuse_2 < 1000:
				fuse_2 += 1
				time.sleep(0.2)	

				for event in pygame.event.get():
					if event.type == QUIT:
						sys.exit()
					if event.type == MOUSEBUTTONDOWN:
						mode_c, mode_r = event.pos
						if 100 < mode_c < 275 and 210 < mode_r < 335:
							cont = False
							human_draw = False
						elif 425 < mode_c < 600 and 210 < mode_r < 335:
							cont = False						
							human_draw = True

		# Game start at here
		# cont will plus one everytime when there is no possible move for one executive
		# cont will be reset to zero if one step is taken
		# if cont = 2, it means that both players have no possible move, then game end
		cont = 0  
		fuse_3 = 0
		available_space = 1

		while cont < 2 and available_space > 0 and fuse_3 < 10000:

			self.screen.fill(background)	
			available_space = 0
			fuse_3 += 1
			computer_draw = False
			delay = False
			time.sleep(0.2)

			if human_draw:
				for event in pygame.event.get():
					if event.type == QUIT:
						sys.exit()
					elif event.type == MOUSEBUTTONDOWN:
						mouse_c, mouse_r = event.pos
						# Relate input coordinate with self.board coordinate
						point_r = int((mouse_r - boundary) / grid_width)
						point_c = int((mouse_c - boundary) / grid_length)
						board_pos = (point_r, point_c)
						# Find all possible sites to put piece. The function returns a dictionary contains
						# the pieces to be reversed
						move_dict = find_avail_points(self.board, self.executive)
						# If one executive has no available moves, display a message and change executive
						if len(move_dict) == 0:
							printing_font = pygame.font.Font(None, 24)
							No_move = printing_font.render("%s has no available " % (self.name[self.executive]), True, black)
							X_turn = printing_font.render("moves. %s's turn to" % (self.name[-self.executive]), True, black)
							left_string = printing_font.render("play", True, black)
							self.screen.blit(No_move, (520, 150))
							self.screen.blit(X_turn, (520, 170))
							self.screen.blit(left_string, (520, 190))
							delay = True
							self.executive *= -1
							cont += 1
						# Put and reverse pieces 
						if board_pos in move_dict.keys():
							self.board[board_pos[0]][board_pos[1]] = self.executive
							for site in move_dict[board_pos]:
								self.board[site[0]][site[1]] *= -1
							self.executive *= -1
							# In PVE mode, after one step, activate computer player
							if PVE: 
								computer_draw = True					
							cont = 0
			else:			
				human_draw = True
				computer_draw = True

			# Draw checker
			pygame.draw.rect(self.screen, checker, (boundary, boundary, 540 - 2 * boundary, 540 - 2 * boundary))

			# Draw 8*8 blocks
			for i in range(row + 1):
				c_start = boundary
				c_end = boundary + row * grid_length
				r = boundary + i * grid_length
				pygame.draw.line(self.screen, black, (c_start, r), (c_end, r), line_width)
			for j in range(column + 1): 
				r_start = boundary
				r_end = boundary + column * grid_width
				c = boundary + j * grid_width
				pygame.draw.line(self.screen, black, (c, r_start), (c, r_end), line_width)

			# Draw pieces and count scores
			white_count = 0
			black_count = 0

			for i in range(row):
				y = boundary + i * grid_width + grid_width / 2 
				for j in range(column):
					x = boundary + j * grid_length + grid_length / 2					
					if self.board[i][j] == 1:
						white_count += 1 
						pygame.draw.circle(self.screen, white, (x, y), grid_width/2-2, 0)
					elif self.board[i][j] == -1:
						black_count += 1					
						pygame.draw.circle(self.screen, black, (x, y), grid_width/2-2, 0)
					else:
						# count available sites
						available_space += 1
			
			# Display current mode
			printing_font = pygame.font.Font(None, 80)
			if PVE:
				play_mode = printing_font.render("PVE", True, black)
			else:
				play_mode = printing_font.render("PVP", True, black)
			self.screen.blit(play_mode, (550, 50))

			# Show executive and scores
			pygame.draw.circle(self.screen, white, (560, 300), grid_width/2-2, 0)			
			pygame.draw.circle(self.screen, black, (560, 400), grid_width/2-2, 0)

			if self.executive == 1: 
				pygame.draw.circle(self.screen, red, (560, 300), grid_width/2, 4)
			else:
				pygame.draw.circle(self.screen, red, (560, 400), grid_width/2, 4)	
			
			printing_font = pygame.font.Font(None, 60)
			print_white_count = printing_font.render("x %d" % (white_count), True, black)
			print_black_count = printing_font.render("x %d" % (black_count), True, black)
			self.screen.blit(print_white_count, (600, 280))
			self.screen.blit(print_black_count, (600, 380))

			pygame.display.update()

			# Sleep three second if one executive has no possible moves
			if delay:
				time.sleep(3)

			# Computer player
			if computer_draw:
				# Presend to think
				time.sleep(0.5)
				computer_move, reverse_site = computer_player(self.board, self.executive, self.priority)

				# Put and reverse pieces
				if computer_move != None:
					self.board[computer_move[0]][computer_move[1]] = self.executive
					for site in reverse_site:
						self.board[site[0]][site[1]] *= -1
					self.executive *= -1

					# Update screen
					white_count = 0
					black_count = 0
					for i in range(row):
						y = boundary + i * grid_width + grid_width / 2 
						for j in range(column):
							x = boundary + j * grid_length + grid_length / 2					
							if self.board[i][j] == 1:
								white_count += 1
								pygame.draw.circle(self.screen, white, (x, y), grid_width/2-2, 0)
							elif self.board[i][j] == -1:
								black_count += 1					
								pygame.draw.circle(self.screen, black, (x, y), grid_width/2-2, 0)
							else:
								available_space += 1
					
					pygame.display.update()

		# Display Game Over
		pygame.gfxdraw.box(self.screen, pygame.Rect(90,100,361,100), (255,255,255,100))
		printing_font = pygame.font.Font(None, 70)
		Game_over = printing_font.render("Game Over", True, orange)
		self.screen.blit(Game_over, (138, 125))
		pygame.display.update()
		time.sleep(1)

		# Display winner
		pygame.gfxdraw.box(self.screen, pygame.Rect(70, 340, 401, 100), (255, 255, 255, 100))
		if white_count < black_count:
			Winner = printing_font.render("Winner is Black", True, orange)
			self.screen.blit(Winner, (85, 370))
		elif white_count > black_count: 
			Winner = printing_font.render("Winner is White", True, orange)
			self.screen.blit(Winner, (85, 370))		
		else:
			Winner = printing_font.render("Draw", True, orange)
			self.screen.blit(Winner, (211, 370))	

		pygame.display.update()	
		time.sleep(5)
		sys.exit()
	
A = Reversi()
A.draw_board()

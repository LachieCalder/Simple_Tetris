# Tetris clone with basic features (WIP)
# By Lachie Calder

import pygame, sys, random
from pygame.locals import *

class Shape(object):
    O = (((0,0,0,0,0), (0,0,0,0,0),(0,0,1,1,0),(0,0,1,1,0),(0,0,0,0,0)),) * 4

    I = (((0,0,0,0,0),(0,0,0,0,0),(0,1,1,1,1),(0,0,0,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,1,0,0)),
         ((0,0,0,0,0),(0,0,0,0,0),(1,1,1,1,0),(0,0,0,0,0),(0,0,0,0,0)),
         ((0,0,1,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,0,0,0)))

    L = (((0,0,0,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,1,1,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,0,0,0),(0,1,1,1,0),(0,1,0,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,1,1,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,0,1,0),(0,1,1,1,0),(0,0,0,0,0),(0,0,0,0,0)))

    J = (((0,0,0,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,1,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,1,0,0,0),(0,1,1,1,0),(0,0,0,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,1,1,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,0,0,0),(0,1,1,1,0),(0,0,0,1,0),(0,0,0,0,0)))

    Z = (((0,0,0,0,0),(0,0,0,1,0),(0,0,1,1,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,0,0,0),(0,1,1,0,0),(0,0,1,1,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,1,0,0),(0,1,1,0,0),(0,1,0,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,1,1,0,0),(0,0,1,1,0),(0,0,0,0,0),(0,0,0,0,0)))

    S = (((0,0,0,0,0),(0,0,1,0,0),(0,0,1,1,0),(0,0,0,1,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,0,0,0),(0,0,1,1,0),(0,1,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,1,0,0,0),(0,1,1,0,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,1,1,0),(0,1,1,0,0),(0,0,0,0,0),(0,0,0,0,0)))

    T = (((0,0,0,0,0),(0,0,1,0,0),(0,0,1,1,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,0,0,0),(0,1,1,1,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,1,0,0),(0,1,1,0,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,1,0,0),(0,1,1,1,0),(0,0,0,0,0),(0,0,0,0,0)))

    SHAPES = {'O': O, 'I': I, 'L': L, 'J': J, 'Z': Z, 'S':S, 'T':T}

    def __init__(self, name=None):
    	if not name == None:
    		self.name = name
    	else:
    		self.name = random.choice(Shape.SHAPES.keys())
    	self.rotation = 0
    	self.shapearray = Shape.SHAPES[self.name][self.rotation]

    def rotate_shape(self):
    	if not self.rotation == 3:
    		self.rotation += 1
    	else:
    		self.rotation = 0
    	self.shapearray = Shape.SHAPES[self.name][self.rotation]
    	return self.shapearray


class Game(object):

	def __init__(self):
		self.width = 11
		self.height = 20
		self.block_size = 20
		self.board = []
		for u in range(0, self.height):
			self.board.append([0] * self.width)

	# draws the board based on self.board
	def draw_board(self):
		self.clear_screen()
		x, y = 0, 0
		for row in self.board:
			for cell in row:
				if cell == 1 or cell == 2:
					left = x * self.block_size
					top = y * self.block_size * -1
					pygame.draw.rect(DISPLAYSURF, BLUE, (left, top, self.block_size, self.block_size))
				x += 1
			y -= 1
			x = 0

	# fills screen with black, ready to draw the board again.
	def clear_screen(self):
		DISPLAYSURF.fill((0,0,0))

	# generates a new shape at the top of the screen
	def spawn_shape(self):
		self.new_shape = Shape()
		self.xnew, self.draw_point = 2, 0
		self.shape_positions = self.new_shape.shapearray

		# finds the bottom of the shape (last layer it has a block on)
		if not 1 in self.shape_positions[3]:
			self.maxh = 3
		elif not 1 in self.shape_positions[4]:
			self.maxh = 4
		else:
			self.maxh = 5

	# draws the shape again, dropped down one step
	def draw_shape(self):
		self.x = self.xnew
		self.delete_shape()
		count = 0
		for i, row in enumerate(self.board):
			if i >= self.draw_point and i < self.draw_point + self.maxh:
				for cell in range(self.x, self.x + 5):
					if self.shape_positions[count][cell - self.x] == 1 and self.board[i][cell] == 0:
						self.board[i][cell] = self.shape_positions[count][cell - self.x]
					if self.shape_positions[count][cell - self.x] == 0 and self.board[i][cell] == 1:
						self.board[i][cell] = self.shape_positions[count][cell - self.x]
				count += 1
		self.draw_point += 1

	# removes last shape position from board object
	def delete_shape(self):
		self.x = self.xnew
		count = 0
		for i, row in enumerate(self.board):
			if i >= self.draw_point and i < self.draw_point + self.maxh:
				for cell in range(self.x, self.x + 5):
					if self.board[i][cell] == self.shape_positions[count][cell - self.x]:
						self.board[i][cell] = 0
				count += 1

	# returns true if shape is at bottom of the screen
	def check_if_at_bottom(self):
		if 1 in self.board[self.height - 1]:
			return True
		else:
			return False

	# returns True if shape will collide with objects already there.
	def check_if_collide(self):
		last_row_after_shape = 0  # the row after the end of the current shape being moved
		last_line_of_shape = self.maxh - 1  # the line containing the last line of the shape with a 1
		
		# finds the last row after the shape
		for i, row in enumerate(self.board):
			if 1 in row and i > last_row_after_shape:
				last_row_after_shape = i 
		last_row_after_shape += 1

		# checks if shape can fit into gap
		for i, cell in enumerate(self.board[last_row_after_shape][self.x: self.x + 5]):  # iterates over slice of cells containing shape
			if self.shape_positions[last_line_of_shape][i] == 1 and cell == 2:
				return True
		return False

	# changes all 1 on board to 2
	def save_to_board(self):
		for i, row in enumerate(self.board):
			for n, cell in enumerate(row):
				if cell == 1:
					self.board[i][n] = 2

	# checks if the tetris blocks have reached the top
	def check_finished(self):
		if 2 in self.board[1]:
			return True
		return False

	# moves shape left or right by changing x the shape is drawn from
	def move_shape(self, direction):
		if direction == "Left":
			self.xnew -= 1
		elif direction == "Right":
			self.xnew += 1

	# gets next version of shape
	def get_rotated_shape(self):
		self.shape_positions = self.new_shape.rotate_shape()

	# checks if any row is filled fully with 2(NOT IMPLEMENTED FULLY)
	def check_row_filled(self):
		for i, row in enumerate(self.board):
			if row[1] == 2 and row.count(row[1]) == len(row) - 1:  # checks all elements in row (a list) are 2
				self.clear_row(i)

	# replaces all cells in row with 0
	def clear_row(self, row):
		for cell in xrange(0, 11):
			self.board[row][cell] = 0

# setting Variables, initializing game

pygame.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0, 0, 255)

FPS = 5
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((200, 400))
pygame.display.set_caption('Beta Tetris!')

DISPLAYSURF.fill(BLACK)

Tetris = Game()
Tetris.spawn_shape()
Tetris.draw_board()
counter = 0


while True:  # Main game loop
	if Tetris.check_finished() == True:
		break

	Tetris.draw_shape()
	Tetris.draw_board()

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_LEFT:
				Tetris.move_shape("Left")
			elif event.key == K_RIGHT:
				Tetris.move_shape("Right")
			elif event.key == K_SPACE:
				Tetris.get_rotated_shape()

	if Tetris.check_if_at_bottom() == True or Tetris.check_if_collide() == True:
		Tetris.save_to_board()
		Tetris.spawn_shape()

	Tetris.check_row_filled()

	pygame.display.update()
	fpsClock.tick(FPS)

# displaying game over screen

DISPLAYSURF.fill(BLACK)
myfont = pygame.font.SysFont("sans-serif", 50)
label1 = myfont.render("GAME", 1, (100,255,0))
label2 = myfont.render("OVER", 1, (100,255,0))
DISPLAYSURF.blit(label1, (40, 50))
DISPLAYSURF.blit(label2, (40, 100))

while True: # Secondary loop, specifically for game over screen

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	pygame.display.update()
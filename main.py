import pygame #type: ignore
import sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN

def is_board_full(grid):
  return all(all(row) for row in grid) # all(row) checks if all cells in row are filled
  # iterated through all 3 rows, checked via another all() function

def check_win(clicked_grid):
  # put win function here

pygame.init()
screen_width, screen_height = 768, 432
screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()
delta_time = 0

grid_size = 3
min_dimension = min(screen_width, screen_height)
cell_size = min_dimension // grid_size
margin = 20

X_icon = pygame.image.load('ulttictactoegame_x.png')
X_icon = pygame.transform.scale(X_icon, (cell_size - 15, cell_size - 15))
O_icon = pygame.image.load('ulttictactoegame_o.png')
O_icon = pygame.transform.scale(O_icon, (cell_size - 15, cell_size - 15))
placed_images = []

current_player = 'X'
clicked_grid = [[''] * grid_size for _ in range(grid_size)] # to store who clicked a square

running = True
while running:
  offset_x = (screen_width - min_dimension) // 2 + margin # center the board
  offset_y = (screen_height - min_dimension) // 2 + margin

  screen.fill([17, 0, 34])

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False # quit if close button clicked

    elif event.type == MOUSEBUTTONDOWN and event.button == 1: # if lmb button click = true
      mouse_x, mouse_y = pygame.mouse.get_pos()

      grid_x = (mouse_x - offset_x) // cell_size # gets coordinates of current grid space
      grid_y = (mouse_y - offset_y) // cell_size

      # checked if the click is in a negative grid space
      if 0 <= grid_x < grid_size and 0 <= grid_y < grid_size and clicked_grid[grid_y][grid_x] == '':
        clicked_grid[grid_y][grid_x] = current_player

        print(current_player, "Clicked grid space:", grid_x, grid_y)

        image_x_pos = grid_x * cell_size + offset_x + (cell_size - X_icon.get_width()) // 2 
        image_y_pos = grid_y * cell_size + offset_y + (cell_size - X_icon.get_height()) // 2

        if current_player == 'O':
          placed_images.append((O_icon, (image_x_pos, image_y_pos)))
        else:
          placed_images.append((X_icon, (image_x_pos, image_y_pos)))

        current_player = 'O' if current_player == 'X' else 'X'

  # loops from 1 to grid_side (exclusive), with i as index
  for i in range(1, grid_size):
    x = i * cell_size + offset_x
    pygame.draw.line(screen, (255, 255, 255), (x, offset_y), (x, screen_height - offset_y), 5)
  for j in range(1, grid_size):
    y = j * cell_size + offset_y
    pygame.draw.line(screen, (255, 255, 255), (offset_x, y), (screen_width - offset_x, y), 5)

  for placed_image in placed_images:
    screen.blit(*placed_image)

  if check_win(clicked_grid):
    print("Game over, ", current_player, " won!")
    running = False
  if is_board_full(clicked_grid):
    print("It's a tie!")
    running = False

  pygame.display.flip() # necessary to update screen

  delta_time = clock.tick(60) / 1000 # locks fps to 60

pygame.quit()

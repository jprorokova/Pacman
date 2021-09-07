from pygame.math import Vector2 as vec

#SCREEN SETTINGS
TOP_BOTTOM_BUFFER = 50
WIDTH,HEIGHT = 610,670
MAZE_WIDTH,MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER,HEIGHT-TOP_BOTTOM_BUFFER
FPS = 60

#colour settings
BLACK = (0,0,0)
RED = (255,0,0)
GREY = (120,120,120)
WHITE = (255,255,255)
PLAYER_COLOUR = (190,194,15)
#font settings
START_TEXT_SIZE = 16
START_FONT = 'arial black'
#player settings
PLAYER_START_POS = vec(1,10)

#mob settings
import glob
import pygame
import settings

# Load cards textures
CARD_TX_PATH = 'sprites/cards/'
tx_cards = {fn.split('\\')[-1].split('.')[0]:pygame.image.load(fn) for fn in glob.glob(CARD_TX_PATH + '*.png')}

# Load background texture
tx_mat = pygame.image.load("sprites/mat.png")


# Load and swap color of zone
def load_zone(color):
    tx = pygame.PixelArray(pygame.image.load("sprites/player_zone.png"))
    tx.replace((255, 255, 255), color, weights=(1,1,1))
    surf = tx.surface
    tx.close()
    return surf

# Load players zones textures
tx_player_zones = []
for color in settings.PLAYER_COLORS:
    tx_player_zones.append(load_zone(color))

# Load dealer zones textures
tx_dealer_zone = load_zone(color)


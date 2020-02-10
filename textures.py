import glob
from pygame.image import load


CARD_SPRITE_PATH = 'sprites/cards/'

tx_mat = load("sprites/mat.png")
tx_player_zone = load("sprites/player_zone.png")

tx_cards = {fn.split('\\')[-1].split('.')[0]:load(fn) for fn in glob.glob(CARD_SPRITE_PATH + '*.png')}

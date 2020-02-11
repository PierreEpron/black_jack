# import random
# random.seed(0)


DEALER_COLOR = (128, 0, 0) # Maroon
PLAYER_COLORS = [
    (230,25,75),    # Red
    (60,180,75),    # Green
    (0, 130, 200),  # Blue
    (145, 30, 180), # Purple
    (230,190,255),  # Lavender
    ((128,128,0)),  # Olive
    (0,0,128),      # Navy
    (245,130,48)]    # Orange

# Used for first 2 deals, interval between card displayed
TIME_TO_WAIT = .25

# Used for create deck of cards
AS = 'A'
FIGURES = ['H', 'D', 'C', 'S']
BASE_DECK = [
    ('2', 2), ('3', 3), ('4', 4), ('5', 6),
    ('6', 6), ('7', 7), ('8', 8), ('9', 9),
    ('10', 10), ('J', 10), ('Q', 10), 
    ('K', 10), (AS, 1)]
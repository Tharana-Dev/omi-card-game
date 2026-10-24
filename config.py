# config.py
import pygame

WIDTH, HEIGHT = 1024, 700
CARD_W, CARD_H = 70, 90
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

RANK_VALUE = {"7":0, "8":1, "9":2, "10":3, "J":4, "Q":5, "K":6, "A":7}
PLAYERS = ["human", "right_ai", "partner", "left_ai"]

AI_OFFSETS = {
    "right_ai": (60, 0),
    "partner": (0, -60),
    "left_ai": (-60, 0),
    "human": (0, 60)
}

BG_COLOR = (50, 70, 30)
TRUMP_COLOR = (25, 25, 255)
TEXT_COLOR = (25, 25, 255)
PROMPT_COLOR = (25, 25, 25)
TRICK_CLEAR_DELAY = 1500

FONT_CARD = None
FONT_PROMPT = None

def init_fonts():
    global FONT_CARD, FONT_PROMPT
    FONT_CARD = pygame.font.SysFont("segoeuisymbol", 24)
    FONT_PROMPT = pygame.font.SysFont(None, 45)

def update_card_size(width, height):
    global CARD_W, CARD_H
    CARD_W = max(50, min(100, width // 15))
    CARD_H = int(CARD_W * 90 / 70)

# Initial call based on default dimensions
update_card_size(WIDTH, HEIGHT)

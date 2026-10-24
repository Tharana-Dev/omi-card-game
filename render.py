# render.py
import pygame
import config

def draw_card(screen, center_x, center_y, card=None, face_up=True, angle=0):
    if config.FONT_CARD is None:
        return
    card_surf = pygame.Surface((config.CARD_W, config.CARD_H), pygame.SRCALPHA)
    if face_up and card is not None:
        rank, suit = card
        color = (0, 0, 0) if suit in ("♠", "♣") else (255, 0, 0)
        pygame.draw.rect(card_surf, (255, 255, 255), (0, 0, config.CARD_W, config.CARD_H), border_radius=5)
        pygame.draw.rect(card_surf, (0, 0, 0), (0, 0, config.CARD_W, config.CARD_H), 2, border_radius=5)
        text = config.FONT_CARD.render(f"{rank}{suit}", True, color)
        card_surf.blit(text, (10, 30))
    else:
        pygame.draw.rect(card_surf, (100, 100, 100), (0, 0, config.CARD_W, config.CARD_H), border_radius=5)
        pygame.draw.rect(card_surf, (0, 0, 0), (0, 0, config.CARD_W, config.CARD_H), 2, border_radius=5)
        text = config.FONT_CARD.render("¿", True, (255, 255, 255))
        text_rect = text.get_rect(center=(config.CARD_W // 2, config.CARD_H // 2))
        card_surf.blit(text, text_rect)

    if angle != 0:
        card_surf = pygame.transform.rotate(card_surf, angle)
    rect = card_surf.get_rect(center=(center_x, center_y))
    screen.blit(card_surf, rect.topleft)

# main.py
import pygame
import sys
import config
from game_logic import Game

def show_start_screen(screen):
    from config import WIDTH, HEIGHT
    clock = pygame.time.Clock()

    try:
        pygame.mixer.music.load("start_bg.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)  # loop indefinitely
    except:
        print("Start screen music not found")

    def draw_gradient():
        for y in range(HEIGHT):
            r = 20 + int(y * 20 / HEIGHT)
            g = 50 + int(y * 30 / HEIGHT)
            b = 60 + int(y * 40 / HEIGHT)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    title_font = pygame.font.SysFont("segoeuisymbol", 72, bold=True)
    button_font = pygame.font.SysFont("segoeuisymbol", 36)
    small_font = pygame.font.SysFont(None, 24)

    start_rect = None
    instr_rect = None

    def show_instructions():
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))
        instr_font = pygame.font.SysFont(None, 28)
        lines = [
            "Omi Rules",
            "",
            "• Single‑click on a green‑bordered card to play.",
            "• You must follow the led suit if you have it.",
            "• If you don't have the led suit, you may play any card (including trump).",
            "• Trump beats all other suits.",
            "• First team to 10 points wins.",
            "• All 8 tricks → 3 points to winner.",
            "• 5‑7 tricks: declarer's team wins → +1; loses → opponents +2.",
            "• Draw (4‑4) → no points, next round winner gets +2 (bonus round).",
            "",
            "Click anywhere to close."
        ]
        y_offset = HEIGHT//2 - 150
        for line in lines:
            text = instr_font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH//2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 30
        pygame.display.flip()
        waiting = True
        while waiting:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN or ev.type == pygame.KEYDOWN:
                    waiting = False

    while True:
        # Handle resize events during start screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.VIDEORESIZE:
                # Update config dimensions and screen surface
                config.WIDTH, config.HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.RESIZABLE)
                # Update local references
                WIDTH, HEIGHT = config.WIDTH, config.HEIGHT
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect and start_rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()   # stop start screen music
                    return True
                if instr_rect and instr_rect.collidepoint(event.pos):
                    show_instructions()
                    # After instructions, loop continues, redrawing start screen

        # Redraw everything with current dimensions
        draw_gradient()

        # Title with shadow
        title_shadow = title_font.render("Omi: Sri Lankan Card Game", True, (0, 0, 0))
        title_text = title_font.render("Omi: Sri Lankan Card Game", True, (255, 215, 0))
        shadow_rect = title_shadow.get_rect(center=(WIDTH//2 + 4, HEIGHT//2 - 100 + 4))
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
        screen.blit(title_shadow, shadow_rect)
        screen.blit(title_text, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        # Start button
        start_text = button_font.render("Start Game", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        start_color = (100, 100, 100) if start_rect.collidepoint(mouse_pos) else (60, 60, 60)
        pygame.draw.rect(screen, start_color, start_rect.inflate(40, 20), border_radius=10)
        pygame.draw.rect(screen, (200, 200, 200), start_rect.inflate(40, 20), 2, border_radius=10)
        screen.blit(start_text, start_rect)

        # Instructions button
        instr_text = button_font.render("Instructions", True, (255, 255, 255))
        instr_rect = instr_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 150))
        instr_color = (80, 80, 80) if instr_rect.collidepoint(mouse_pos) else (50, 50, 50)
        pygame.draw.rect(screen, instr_color, instr_rect.inflate(40, 20), border_radius=10)
        pygame.draw.rect(screen, (200, 200, 200), instr_rect.inflate(40, 20), 2, border_radius=10)
        screen.blit(instr_text, instr_rect)

        # Footer
        footer = small_font.render("Sri Lankan Trick Taking Game", True, (200, 200, 200))
        footer_rect = footer.get_rect(center=(WIDTH//2, HEIGHT - 30))
        screen.blit(footer, footer_rect)

        pygame.display.flip()
        clock.tick(60)

def choose_trump_popup(screen):
    overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    prompt_text = config.FONT_PROMPT.render("Choose trump suit (click on suit)", True, (255, 85, 50))
    text_rect = prompt_text.get_rect(center=(config.WIDTH//2, config.HEIGHT//2 - 100))
    screen.blit(prompt_text, text_rect)

    suits_symbols = ["♠", "♥", "♣", "♦"]
    positions = [(config.WIDTH//2 - 160, config.HEIGHT//2 - 50),
                 (config.WIDTH//2 + 140, config.HEIGHT//2 - 50),
                 (config.WIDTH//2 - 160, config.HEIGHT//2 + 50),
                 (config.WIDTH//2 + 140, config.HEIGHT//2 + 50)]
    rects = []
    for sym, pos in zip(suits_symbols, positions):
        text = config.FONT_CARD.render(sym, True, (255, 255, 255))
        rect = text.get_rect(center=pos)
        pygame.draw.rect(screen, (80, 80, 80), rect.inflate(40, 40), border_radius=10)
        screen.blit(text, rect)
        rects.append((sym, rect))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for sym, rect in rects:
                    if rect.collidepoint(event.pos):
                        return sym

def show_game_over_popup(screen, winner):
    from config import WIDTH, HEIGHT
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))

    font = pygame.font.SysFont(None, 48)
    text = font.render(f"{winner} wins the game!", True, (255, 215, 0))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    screen.blit(text, text_rect)

    button_font = pygame.font.SysFont(None, 36)
    restart_text = button_font.render("Restart", True, (255,255,255))
    quit_text = button_font.render("Quit", True, (255,255,255))

    restart_rect = restart_text.get_rect(center=(WIDTH//2 - 80, HEIGHT//2 + 50))
    quit_rect = quit_text.get_rect(center=(WIDTH//2 + 80, HEIGHT//2 + 50))

    pygame.draw.rect(screen, (80,80,80), restart_rect.inflate(20,10), border_radius=5)
    pygame.draw.rect(screen, (80,80,80), quit_rect.inflate(20,10), border_radius=5)
    screen.blit(restart_text, restart_rect)
    screen.blit(quit_text, quit_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return "restart"
                if quit_rect.collidepoint(event.pos):
                    return "quit"

def main():
    pygame.init()
    config.init_fonts()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Omi – Sri Lankan Card Game")
    clock = pygame.time.Clock()
    
    pygame.mixer.init()
    if not show_start_screen(screen):
        pygame.quit()
        sys.exit()

    game = Game()

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                config.WIDTH, config.HEIGHT = event.w, event.h
                config.update_card_size(config.WIDTH, config.HEIGHT)
                screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.RESIZABLE)
                game.screen = screen
                game.resize_background()
                # Do NOT clear current trick or led suit
                game.recalculate_positions()

                
            elif event.type == pygame.QUIT:
                running = False
            else:
                game.handle_input(event)

        game.update()
        game.draw()
        pygame.display.flip()

        if game.game_over:
            choice = show_game_over_popup(screen, game.winner)
            if choice == "restart":
                game.restart_game()
            else:
                running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

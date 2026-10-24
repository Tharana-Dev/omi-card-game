# game_logic.py
import pygame
import random
import config
from render import draw_card
from ai import ai_play


class Game:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.players = config.PLAYERS
        self.current_player_index = 0
        self.trump_suit = None
        self.led_suit = None
        self.played_cards = []
        self.current_trick = []
        self.human_hand = []
        self.right_ai_hand = []
        self.partner_hand = []
        self.left_ai_hand = []
        self.trick_clearing = False
        self.trick_clear_time = 0
        self.game_over = False
        self.winner = None

        # Load sounds
        try:
            self.card_sound = pygame.mixer.Sound("card_play.wav")
            self.card_sound.set_volume(0.5)
            self.game_over_sound = pygame.mixer.Sound("game_over.wav")
            self.game_over_sound.set_volume(0.7)
        except:
            self.card_sound = None
            self.game_over_sound = None

        # Round scoring and rotation
        self.dealer_index = 0
        self.declarer_index = (self.dealer_index + 1) % 4
        self.bonus_pending = False
        self.round_tricks_declarer = 0
        self.round_tricks_opponents = 0
        self.round_tricks_played = 0
        self.score_human_partner = 0
        self.score_ai = 0
        self.bonus_round = False

        # Position variables
        self.human_y = None
        self.human_x_start = None
        self.partner_y = None
        self.partner_x_start = None
        self.partner_card_spacing = 50
        self.left_x = 70
        self.left_y_start = 170
        self.left_card_spacing = 50
        self.right_x = config.WIDTH - 70
        self.right_y_start = 170
        self.right_card_spacing = 50

        # Load background
        self.bg_original = None
        self.bg_image = None
        self.load_background()

        self.setup_game()
        self.recalculate_positions()

    def load_background(self):
        try:
            self.bg_original = pygame.image.load("image.png")
            self.bg_image = pygame.transform.scale(self.bg_original, (config.WIDTH, config.HEIGHT))
            print("Background loaded")
        except Exception as e:
            print(f"Background load error: {e}")
            self.bg_original = None
            self.bg_image = None

    def resize_background(self):
        if self.bg_original:
            self.bg_image = pygame.transform.scale(self.bg_original, (config.WIDTH, config.HEIGHT))

    def setup_game(self):
        ranks = ["7","8","9","10","J","Q","K","A"]
        suits = ["♠", "♥", "♣", "♦"]
        deck = []
        for suit in suits:
            for rank in ranks:
                deck.append((rank, suit))
        random.shuffle(deck)

        self.human_hand = deck[0:4]
        self.partner_hand = deck[4:8]
        self.left_ai_hand = deck[8:12]
        self.right_ai_hand = deck[12:16]

        self.draw_background()
        temp_x_start = (config.WIDTH - len(self.human_hand) * (config.CARD_W + 10)) // 2
        temp_y = config.HEIGHT - 100
        for i, card in enumerate(self.human_hand):
            x = temp_x_start + i * (config.CARD_W + 10)
            draw_card(self.screen, x + config.CARD_W//2, temp_y, card, face_up=True)

        declarer_name = self.players[self.declarer_index]
        if declarer_name == "human":
            from main import choose_trump_popup
            self.trump_suit = choose_trump_popup(self.screen)
        else:
            if declarer_name == "right_ai":
                hand = self.right_ai_hand
            elif declarer_name == "partner":
                hand = self.partner_hand
            else:
                hand = self.left_ai_hand
            suit_count = {}
            for (_, suit) in hand:
                suit_count[suit] = suit_count.get(suit, 0) + 1
            max_count = max(suit_count.values())
            best_suits = [s for s, c in suit_count.items() if c == max_count]
            self.trump_suit = random.choice(best_suits)

        self.human_hand.extend(deck[16:20])
        self.partner_hand.extend(deck[20:24])
        self.left_ai_hand.extend(deck[24:28])
        self.right_ai_hand.extend(deck[28:32])

        self.recalculate_positions()

        self.current_player_index = self.declarer_index
        self.led_suit = None
        self.current_trick = []
        self.played_cards = []
        self.trick_clearing = False
        self.round_tricks_declarer = 0
        self.round_tricks_opponents = 0
        self.round_tricks_played = 0

    def draw_background(self):
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill((50, 70, 30))

    def handle_input(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        if self.players[self.current_player_index] != "human":
            return
        if self.trick_clearing or self.game_over:
            return

        if self.led_suit is None:
            legal_indices = list(range(len(self.human_hand)))
        else:
            has_led = any(c[1] == self.led_suit for c in self.human_hand)
            if has_led:
                legal_indices = [i for i, c in enumerate(self.human_hand) if c[1] == self.led_suit]
            else:
                legal_indices = list(range(len(self.human_hand)))

        mx, my = event.pos
        for i, card in enumerate(self.human_hand):
            x = self.human_x_start + i * (config.CARD_W + 10)
            y_offset = -50 if i in legal_indices else 0
            card_top = self.human_y - config.CARD_H // 2 + y_offset
            card_rect = pygame.Rect(x, card_top, config.CARD_W, config.CARD_H)

            if card_rect.collidepoint(mx, my):
                if i not in legal_indices:
                    break
                self.human_hand.pop(i)
                if self.card_sound:
                    self.card_sound.play()
                self.current_trick.append(("human", card))
                center_x = config.WIDTH // 2
                center_y = config.HEIGHT // 2
                off_x, off_y = config.AI_OFFSETS["human"]
                self.played_cards.append((card, center_x + off_x, center_y + off_y))

                if self.led_suit is None:
                    self.led_suit = card[1]
                self.current_player_index = (self.current_player_index + 1) % 4
                if len(self.current_trick) == 4:
                    self.trick_clearing = True
                    self.trick_clear_time = pygame.time.get_ticks()
                self.human_x_start = (config.WIDTH - len(self.human_hand) * (config.CARD_W + 10)) // 2
                break

    def update(self):
        if self.game_over:
            return
        if not self.trick_clearing and self.players[self.current_player_index] != "human":
            pygame.time.delay(500)
            player = self.players[self.current_player_index]
            ai_play(self, player)

        if self.trick_clearing:
            current_time = pygame.time.get_ticks()
            if current_time - self.trick_clear_time > config.TRICK_CLEAR_DELAY:
                winner = self._get_trick_winner()
                if winner in ["human", "partner"]:
                    self.round_tricks_declarer += 1
                else:
                    self.round_tricks_opponents += 1
                self.round_tricks_played += 1

                self.played_cards.clear()
                self.current_trick.clear()
                self.led_suit = None
                self.trick_clearing = False
                self.current_player_index = self.players.index(winner)

                if self.round_tricks_played == 8:
                    self.end_round()

    def end_round(self):
        human_team_won = self.round_tricks_declarer > self.round_tricks_opponents
        tie = self.round_tricks_declarer == self.round_tricks_opponents

        if self.bonus_round:
            if human_team_won:
                self.score_human_partner += 2
            else:
                self.score_ai += 2
            self.bonus_round = False
        else:
            if self.round_tricks_declarer == 8 or self.round_tricks_opponents == 8:
                points = 3
                if self.round_tricks_declarer == 8:
                    self.score_human_partner += points
                else:
                    self.score_ai += points
            elif tie:
                self.bonus_round = True
            else:
                declarer_player = self.players[self.declarer_index]
                declarer_is_human_team = declarer_player in ["human", "partner"]
                if declarer_is_human_team:
                    if human_team_won:
                        self.score_human_partner += 1
                    else:
                        self.score_ai += 2
                else:
                    if human_team_won:
                        self.score_human_partner += 2
                    else:
                        self.score_ai += 1

        if self.score_human_partner >= 10:
            if self.game_over_sound:
                self.game_over_sound.play()
            self.game_over = True
            self.winner = "Human+Partner"
            return
        if self.score_ai >= 10:
            self.game_over = True
            self.winner = "AI Team"
            return

        self.dealer_index = (self.dealer_index + 1) % 4
        self.declarer_index = (self.dealer_index + 1) % 4
        self.setup_game()

    def _get_trick_winner(self):
        best_card = None
        best_player = None
        for player, (rank, suit) in self.current_trick:
            is_trump = (suit == self.trump_suit)
            rank_val = config.RANK_VALUE[rank]
            if best_card is None:
                best_card = (rank_val, is_trump, suit)
                best_player = player
            else:
                if is_trump and not best_card[1]:
                    best_card = (rank_val, is_trump, suit)
                    best_player = player
                elif not is_trump and best_card[1]:
                    pass
                elif is_trump == best_card[1]:
                    if suit == best_card[2] or is_trump:
                        if rank_val > best_card[0]:
                            best_card = (rank_val, is_trump, suit)
                            best_player = player
        return best_player

    def draw(self):
        self.draw_background()

        from config import FONT_CARD, TRUMP_COLOR, TEXT_COLOR
        score_text = FONT_CARD.render(f"Human+Partner: {self.score_human_partner}   AI: {self.score_ai}", True, TEXT_COLOR)
        round_text = FONT_CARD.render(f"Round Tricks: {self.round_tricks_declarer} - {self.round_tricks_opponents}", True, TEXT_COLOR)
        trump_txt = FONT_CARD.render(f"Trump: {self.trump_suit}", True, TRUMP_COLOR)
        self.screen.blit(score_text, (10, 5))
        self.screen.blit(round_text, (10, 35))
        self.screen.blit(trump_txt, (20, 65))

        # Centre cards
        for card, cx, cy in self.played_cards:
            draw_card(self.screen, cx, cy, card, face_up=True)

        is_human_turn = (self.players[self.current_player_index] == "human" and not self.trick_clearing and not self.game_over)
        legal_indices = self.get_legal_cards_for_human() if is_human_turn else []
        for i, card in enumerate(self.human_hand):
            x = self.human_x_start + i * (config.CARD_W + 10)
            y_offset = -50 if i in legal_indices else 0
            draw_card(self.screen, x + config.CARD_W//2, self.human_y + y_offset, card, face_up=True)
            if i in legal_indices:
                card_rect = pygame.Rect(x, self.human_y - config.CARD_H//2 + y_offset, config.CARD_W, config.CARD_H)
                pygame.draw.rect(self.screen, (0, 255, 0), card_rect, 3, border_radius=5)

        for i in range(len(self.partner_hand)):
            draw_card(self.screen, self.partner_x_start + i * self.partner_card_spacing + 90, self.partner_y, None, face_up=False)

        for i in range(len(self.left_ai_hand)):
            draw_card(self.screen, self.left_x, self.left_y_start + i * self.left_card_spacing, None, face_up=False, angle=90)

        for i in range(len(self.right_ai_hand)):
            draw_card(self.screen, self.right_x, self.right_y_start + i * self.right_card_spacing, None, face_up=False, angle=-90)

    def get_legal_cards_for_human(self):
        if self.players[self.current_player_index] != "human":
            return []
        if self.trick_clearing:
            return []
        if self.led_suit is None:
            return list(range(len(self.human_hand)))
        has_led = any(c[1] == self.led_suit for c in self.human_hand)
        if has_led:
            return [i for i, c in enumerate(self.human_hand) if c[1] == self.led_suit]
        else:
            return list(range(len(self.human_hand)))

    def reposition_played_cards(self):
        """Recalculate positions of cards in current trick after resize."""
        if not self.current_trick:
            self.played_cards = []
            return
        center_x = config.WIDTH // 2
        center_y = config.HEIGHT // 2
        new_played = []
        for player, card in self.current_trick:
            off_x, off_y = config.AI_OFFSETS[player]
            new_played.append((card, center_x + off_x, center_y + off_y))
        self.played_cards = new_played

    def recalculate_positions(self):
        """Recalculate all card positions after window resize."""
        from config import WIDTH, HEIGHT, CARD_W, CARD_H
        # Human hand
        self.human_y = HEIGHT - 100
        self.human_x_start = (WIDTH - len(self.human_hand) * (CARD_W + 10)) // 2
        # Partner hand
        self.partner_y = 80
        self.partner_x_start = (WIDTH - len(self.partner_hand) * (CARD_W - 10)) // 2
        # Left AI vertical stack
        self.left_x = 70
        total_height_left = len(self.left_ai_hand) * self.left_card_spacing
        self.left_y_start = (HEIGHT - total_height_left) // 2
        # Right AI vertical stack
        self.right_x = WIDTH - 70
        total_height_right = len(self.right_ai_hand) * self.right_card_spacing
        self.right_y_start = (HEIGHT - total_height_right) // 2
        # Reposition cards already in the current trick
        self.reposition_played_cards()

        
    def restart_game(self):
        self.score_human_partner = 0
        self.score_ai = 0
        self.game_over = False
        self.winner = None
        self.bonus_round = False
        self.dealer_index = 0
        self.declarer_index = (self.dealer_index + 1) % 4
        self.setup_game()

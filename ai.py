import pygame
import random
import config

def ai_play(game, player_name):
    # Determine hand and partner based on player_name
    if player_name == "right_ai":
        hand = game.right_ai_hand
        partner = "left_ai"
    elif player_name == "partner":
        hand = game.partner_hand
        partner = "human"
    elif player_name == "left_ai":
        hand = game.left_ai_hand
        partner = "right_ai"
    else:
        return

    if not hand or game.trick_clearing:
        return

    led_suit = game.led_suit
    trump = game.trump_suit
    current_trick = game.current_trick

    def rank_value(card):
        return config.RANK_VALUE[card[0]]

    # Determine if partner is currently winning the trick
    partner_winning = False
    if current_trick:
        best_val = -1
        best_player = None
        best_is_trump = False
        for player, card in current_trick:
            is_trump = (card[1] == trump)
            val = rank_value(card)
            if best_player is None:
                best_val = val
                best_player = player
                best_is_trump = is_trump
            else:
                if is_trump and not best_is_trump:
                    best_val = val
                    best_player = player
                    best_is_trump = is_trump
                elif not is_trump and best_is_trump:
                    pass
                else:
                    if val > best_val:
                        best_val = val
                        best_player = player
                        best_is_trump = is_trump
        if best_player == partner:
            partner_winning = True

    # Choose card
    if led_suit is None:
        # Leading
        card = max(hand, key=rank_value)
    else:
        suited = [c for c in hand if c[1] == led_suit]
        if suited:
            if partner_winning:
                card = min(suited, key=rank_value)
            else:
                card = max(suited, key=rank_value)
        else:
            trump_cards = [c for c in hand if c[1] == trump]
            if trump_cards:
                if partner_winning:
                    card = min(trump_cards, key=rank_value)
                else:
                    card = max(trump_cards, key=rank_value)
            else:
                card = min(hand, key=rank_value)

    # Play card
    hand.remove(card)
    if game.card_sound:
        game.card_sound.play()
    game.current_trick.append((player_name, card))


    center_x = config.WIDTH // 2
    center_y = config.HEIGHT // 2
    off_x, off_y = config.AI_OFFSETS[player_name]
    game.played_cards.append((card, center_x + off_x, center_y + off_y))

    if game.led_suit is None:
        game.led_suit = card[1]

    game.current_player_index = (game.current_player_index + 1) % 4

    if len(game.current_trick) == 4:
        game.trick_clearing = True
        game.trick_clear_time = pygame.time.get_ticks()

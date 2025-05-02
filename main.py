
import random, time

# Rules:
#   Try to get as close to 21 without going over.
#   Kings, Queens, and Jacks are worth 10 points.
#   Aces are worth 1 or 11 points.
#   Cards 2 through 10 are worth their face value.
#   (H)it to take another card.
#   (S)tand to stop taking cards.
#   On your first play, you can (D)ouble down to increase your bet
#   but must hit exactly one more time before standing.
#   In case of a tie, the bet is returned to the player.
#   The dealer stops hitting at 17.
#
# Money: 5000
# How much do you bet? (1-5000, or QUIT)
# > 400
# Bet: 400
#
# DEALER: ???
#  ___   ___
# |## | |2  |
# |###| | ♥ |
# |_##| |__2|
#
# PLAYER: 17
#  ___   ___
# |K  | |7  |
# | ♠ | | ♦ |
# |__K| |__7|
#
#
# (H)it, (S)tand, (D)ouble down


def blackjack():
    class Hand:
        def __init__(self):
            self.cards = []
            self.value = 0
            self.ace = False

        def update(self):
            self.ace = False
            self.value = 0
            for card in self.cards:
                if card[0] == 'A':
                    self.ace = True
                    self.value += 1
                elif card[0] in ['J', 'Q', 'K']:
                    self.value += 10
                else:
                    self.value += int(card[0])
                if self.value + 10 > 21: self.ace = False

    class Player:
        def __init__(self, name, funds):
            self.name = name
            self.funds = funds
            self.hand = [Hand()]
            self.has_split = False

        def adjust_funds(self, amount):
            self.funds += amount

        def reset_hand(self):
            self.hand = [Hand()]
            self.has_split = False

        def split(self):
            self.has_split = True
            second_card = self.hand[1].cards.pop()
            self.hand.append(Hand())
            self.hand[-1].cards.append(second_card)




    def wait_time():  # Adjust speed of play
        time.sleep(1)

    def generate_deck(number):
        def shuffle(cards):
            random.shuffle(cards)
            return cards

        suits = [chr(9827), chr(9829), chr(9830), chr(9824)]  # '♣ ♥ ♦ ♠'
        face_cards = {'J': 10, 'Q': 10, 'K': 10, 'A': 1}

        deck_template = []
        for i in suits:
            for x in range(2, 11):  # Numbered cards
                deck_template.append((x, i))
            for y in face_cards:
                deck_template.append((y, i))
        return shuffle(deck_template * number)

    def burn():
        deck.pop(0)
        # nothing to return as card is discarded

    def draw():
        card = deck.pop()  # Pops end of list, for O(1) rather than start O(n) in Python. Shuffle means no different.
        return card

    def get_value(cards):
        ace = False
        value = 0
        for card in cards:
            if card[0] == 'A':
                ace = True
                value += 1
            elif card[0] in ['J', 'Q', 'K']:
                value += 10
            else:
                value += int(card[0])
            if value + 10 > 21: ace = False
        return value, ace

    def print_hand(hand, dealer_hidden):
        card_design = [' ___ ',
                       '|{} |',  # spacer will adjust format for 10
                       '| {} |',
                       '|_{}|']  # spacer will adjust format for 10
        hand_graphic = [[], [], [], []]
        for card in hand:
            spacer1 = ' '
            spacer2 = '_'
            num_char = str(card[0])
            suit_char = str(card[1])
            if card[0] == 10 and not dealer_hidden:  # adjust only if card is not hidden for case 10 only
                spacer1 = spacer2 = ''
            if dealer_hidden:
                suit_char = '?'
                num_char = '?'
                dealer_hidden = False
            hand_graphic[0].append(card_design[0])
            hand_graphic[1].append(card_design[1].format(num_char + spacer1))
            hand_graphic[2].append(card_design[2].format(suit_char))
            hand_graphic[3].append(card_design[3].format(spacer2 + num_char))


        for i in range(4):
            ''.join(hand_graphic[i])
            print('  '.join(hand_graphic[i]))

    def p_input():
        while True:
            try:
                choice = str(input('(H)it, (S)tand, (D)ouble down:\n'))
                match choice.upper():
                    case 'H' | 'S' | 'D': return choice.upper()
                    case _: print('Invalid input! Type ''H'', ''S'', or ''D''')
            except ValueError:
                print('Invalid input! Type ''H'', ''S'', or ''D''')

    def player_turn():
        print()
        p_score, p_Ace = get_value(p_hand)
        d_score, d_Ace = get_value(d_hand[1:])
        print(f'Dealer has: {d_score} ({d_score + 10})' if d_Ace else f'Dealer has: {d_score}')
        if p_score + 10 == 21:  # Only way to achieve this is if you have an ace (1) + a face/10 (10) = 11 (21)
            print('Player has Blackjack (21)!')
            return 21
        print(f'You have: {p_score} ({p_score + 10})' if p_Ace else f'You have: {p_score}')

        # add function here to split hands eventually if equal value cards show up in initial 2 drawn?
        while True:
            if p_score > 21:
                return p_score  # Ends turn without continuing through cards
            move = p_input()
            if move == 'S':  # Stand
                if p_Ace == True:
                    p_score += 10
                break
            if move == 'D':
                # double the bet
                p_wallet -= p_bet
                p_bet += p_bet
                print('Bet doubled. Draw one more card:')
                p_hand.append(draw())
                print(f'You drew a {p_hand[-1][0]} of {p_hand[-1][1]}')
                print_hand(p_hand, False)
                break
            if move == 'H': # Hit
                p_hand.append(draw())
                print(f'You drew a {p_hand[-1][0]} of {p_hand[-1][1]}')
                print_hand(p_hand, False)
            p_score, p_Ace = get_value(p_hand)
            print(f'You have: {p_score} ({p_score + 10})' if p_Ace else f'You have: {p_score}')
        print(f'Player stands with: {p_score}')
        return p_score

    def dealer_turn():
        print(f'Dealer reveals card: {d_hand[0][0]} of {d_hand[0][1]}')
        d_score, d_Ace = get_value(d_hand)  # This time, add value of all cards
        print_hand(d_hand, False)
        print(f'Dealer has: {d_score} ({d_score + 10})' if d_Ace else f'Dealer has: {d_score}')
        # DOES DEALER EVER SPLIT?? add function here to split hands eventually if equal value cards show up in initial 2 drawn?
        while True:
            wait_time()
            if d_score > 21:  # Bust
                break
            elif d_Ace == True and (17 <= d_score + 10 <= 21):
                d_score += 10  # if ace, use higher score
                break
            elif d_score >= 17:  # Dealer stands at 17  -  or d_score > p_score  # Dealer stands if ahead and under 17
                break
            d_hand.append(draw())
            d_score, d_Ace = get_value(d_hand)  # This time, add value of all cards
            print_hand(d_hand, False)
            print(f'Dealer hits: {d_hand[-1][0]} of {d_hand[-1][1]} - ({d_score})')
        print(f'Dealer stands with: {d_score}')
        return d_score

    print(f'{chr(9827)+chr(9829)+chr(9830)+chr(9824)} BLACKJACK {chr(9827)+chr(9829)+chr(9830)+chr(9824)}')
    deck = []
    SHOE = 6  # Shoe is the number of decks/size of the deck used in Blackjack. Casinos often use a 6-deck shoe.
    p_wallet = 500
    hand_count = 0

    while True:  # playing at 'table'
        if len(deck) < 250:
            deck = generate_deck(SHOE)  # Create and shuffle decks(n) of 52 cards (SHOE)
        hand_count += 1
        print(f'HAND #{hand_count}:')
        p_hand = []
        d_hand = []

        # Betting round 1
        p_bet = 0
        while p_bet == 0:
            try:
                p_bet = int(input(f'Available funds: {p_wallet}\nPlace your bet:'))
                if p_bet == 0:
                    print('Don''t be silly, you can''t bet nothing!')
            except ValueError:
                print('Please enter a valid number (bets are made in values of 10)')
            if p_bet % 10 != 0 or p_bet > p_wallet:
                p_bet = 0
                print('Please enter a valid number (bets are made in values of 10).')
        p_wallet -= p_bet

        # Deal Cards
        burn()  # burn first card as in casinos
        for i in range(2): # initial draw (both players)
            p_hand.append(draw())
            d_hand.append(draw())
        print_hand(d_hand, True)
        print(f'DEALER HAND: {d_hand[-1][0]} of {d_hand[-1][1]} and one card face down')
        wait_time()
        print_hand(p_hand, False)
        print(f'PLAYER HAND: {p_hand[0][0]} of {p_hand[0][1]}, {p_hand[1][0]} of {p_hand[1][1]}')
        wait_time()
        player_result = player_turn()
        wait_time()
        if player_result > 21:
            print('Player bust!\nRESULT: House wins.')
            p_bet = 0
        else:
            dealer_result = dealer_turn()
            wait_time()
            # Calculate Results
            print()
            if dealer_result > 21:
                print('Dealer is bust!')
                print(f'RESULT: Player wins with {player_result}')
                p_wallet += p_bet * 1.5  # Return bet + winnings at 3:2
            elif player_result == dealer_result:
                print(f'RESULT: Draw. Bets returned.')
                p_wallet += p_bet  # Return bet only
            elif player_result > dealer_result:
                print(f'RESULT: Player wins with {player_result}')
                p_wallet += p_bet * 1.5  # Return bet + winnings at 3:2
            else:
                print(f'RESULT: Dealer wins with {dealer_result}')
                p_bet = 0

        try:  # Play again? If not, breaks outermost loop and ends programme
            wait_time()
            play_again = input('\nPlay again? (Y/N):')
            if play_again.upper() == 'N':
                print('\nThanks for playing!')
                wait_time()
                break
            elif p_wallet < 10:
                print('Oops! You''re out of money!\nThanks for playing!')
                wait_time()
                break
        except ValueError:
            print('Invalid input! Type ''Y'' or ''N''')
        print('\n\n')

def main():
    blackjack()

if __name__ == '__main__':
    main()

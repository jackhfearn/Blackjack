
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


def blackjack_oop():
    class Card:
        def __init__(self, rank, suit):
            self.rank = rank
            self.suit = suit

        # is face card
        # is ace

    class Deck:
        def __init__(self, num):
            self.cards = []
            self.generate(num)
            self.shuffle()

        def clear(self):
            self.cards.clear()

        def generate(self, number):
            self.clear()
            suits = [chr(9827), chr(9829), chr(9830), chr(9824)]  # '♣ ♥ ♦ ♠'
            face_cards = {'J': 10, 'Q': 10, 'K': 10, 'A': 1}

            for i in suits:
                for x in range(2, 11):  # Numbered cards
                    self.cards.append(Card(x, i))
                for y in face_cards:
                    self.cards.append(Card(y, i))
            self.cards = self.cards * number
            self.shuffle()

        def shuffle(self):
            random.shuffle(self.cards)

        def burn(self):
            self.cards.pop()
            # nothing to return as card is discarded

        def draw(self):
            return self.cards.pop()  # Pops end of list, for O(1) rather than start O(n) in Python. Shuffling means no different.

    class Hand:
        def __init__(self):
            self.cards = []
            self.value = 0
            self.ace = False
            self.bet = 0
            self.blackjack = False

        def update(self, dealer_hidden=False):
            self.ace = False
            self.value = 0
            for card in self.cards:
                if card.rank == 'A':
                    self.ace = True
                    self.value += 1
                elif card.rank in ['J', 'Q', 'K']:
                    self.value += 10
                else:
                    self.value += int(card.rank)
                if dealer_hidden:
                    break
            if self.value + 10 > 21:
                self.ace = False

    class Player:
        all_players = []

        def __init__(self, name, funds=500):
            self.name = name
            self.funds = funds
            self.hand = Hand()
            self.split_hand = Hand()
            Player.all_players.append(self)

        def place_bet(self, hand, wager):
            self.funds -= wager
            hand.bet = wager

        def adjust_funds(self, amount):
            self.funds += amount

        def reset_hand(self):
            self.hand = Hand()
            self.split_hand = Hand()

        def split(self):
            if self.funds >= self.hand.bet:
                second_card = self.hand.cards.pop()  # Pop one card
                self.split_hand.cards.append(second_card)  # Then add card to new hand
                self.split_hand.bet = self.hand.bet
                self.adjust_funds(-self.split_hand.bet)
                self.hand.update()
                self.split_hand.update()
            else:
                print('Not enough funds to split!')

    class Dealer(Player):
        def __init__(self):
            super().__init__(name="Dealer", funds=0)
            self.hand.update(True)

    def wait_time():  # Adjust speed of play
        time.sleep(1)

    def betting(position):
        position.hand.bet = 0
        bet = 0
        while bet == 0:
            try:
                bet = int(input(f'{position.name} - Available funds: {position.funds}\nPlace your bet:'))
                if bet == 0:
                    print('Don''t be silly, you can''t bet nothing!')
            except ValueError:
                print('Please enter a valid number (bets are made in values of 10)')
            if bet % 10 != 0 or bet > position.funds:
                bet = 0
                print('Please enter a valid number (bets are made in values of 10).')
        position.adjust_funds(- bet)  # Negative number - instantly removed from overall funds
        position.hand.bet = bet

    def dealer_turn(house):
        house.hand.update()
        print(f'Dealer reveals card: {house.hand.cards[1].rank} of {house.hand.cards[1].suit}')
        print_hand(house.hand, False)
        if house.hand.value + 10 == 21 and house.hand.ace:
            print(f'{house.name} has Blackjack (21)!')
            house.hand.blackjack = True
            return
        else:
            print(f'Dealer has: {house.hand.value} ({house.hand.value + 10})'
              if house.hand.ace else f'Dealer has: {house.hand.value}')

        while True:
            wait_time()
            if house.hand.value > 21:  # Bust
                print('Dealer busts!')
                return
            elif house.hand.ace == True and (17 <= house.hand.value + 10 <= 21):
                house.hand.value += 10  # if ace, use higher score
                break
            elif house.hand.value >= 17:  # Dealer stands at 17
                break
            house.hand.cards.append(active_deck.draw())
            house.hand.update()  # This time, add value of all cards
            print_hand(house.hand, False)
            print(f'Dealer hits: {house.hand.cards[-1].rank} of {house.hand.cards[-1].suit} - ({house.hand.value})')
        print(f'Dealer stands with: {house.hand.value}')

    def player_turn(position):
        def p_action(first):
            while True:
                if first:
                    try:
                        choice = str(input('(H)it / (S)tand / (D)ouble down:\n'))
                        match choice.upper():
                            case 'H' | 'S' | 'D':
                                return choice.upper()
                            case _:
                                print('Invalid input! Type ''H'', ''S'', or ''D''')
                    except ValueError:
                        print('Invalid input!')
                else:
                    try:
                        choice = str(input('(H)it / (S)tand:\n'))
                        match choice.upper():
                            case 'H' | 'S':
                                return choice.upper()
                            case _:
                                print('Invalid input! Type ''H'' or ''S''')
                    except ValueError:
                        print('Invalid input!')

        position.hand.update()
        print_score(position.name, position.hand)
        if position.hand.value + 10 == 21 and position.hand.ace:
            print(f'{position.name} has Blackjack (21)!')
            position.hand.blackjack = True
            return
        else:
            dealer.hand.update(dealer_hidden=True)  # Hides value of second card by not including in update
            print_score(dealer.name, dealer.hand)

        # add function here to split hands eventually if equal value cards show up in initial 2 drawn?
        split_case = (position.hand.cards[0].rank == position.hand.cards[1].rank)
        while split_case == True:
            try:
                choice = str(input('Do you want to Split? (Y/N)'))
                match choice.upper():
                    case 'Y':
                        break
                    case 'N':
                        split_case = False
                        break
                    case _:
                        print('Invalid input!')
            except ValueError:
                print('Invalid input!')
        if split_case:
            position.split_hand.cards.append(position.hand.cards.pop())
            hands = [position.hand,position.split_hand]
        else:
            hands = [position.hand]
        first_action = True
        for i in hands:
                while True:
                if i.value > 21:
                    print('Player bust!')
                    break  # Ends turn without continuing through cards
                move = p_action(first_action)
                if move == 'S':  # Stand
                    if i.ace:
                       i.value += 10
                    break
                if move == 'D':
                    # double the bet (ONLY THE FIRST TIME ROUND -- MUST REMOVE OPTION FOR SECOND PLAYER INPUT)
                    position.funds -= i.bet
                    i.bet = i.bet * 2
                    print('Bet doubled. Draw one more card:')
                    i.cards.append(active_deck.draw())
                    i.update()
                    print(f'You drew a {i.cards[-1].rank} of {i.cards[-1].suit}')
                    print_hand(i, False)
                    if i.value > 21:
                        print('Player bust!')
                    break  # Ends turn without continuing through cards
                if move == 'H': # Hit
                    first_action = False
                    i.cards.append(active_deck.draw())
                    i.update()
                    print(f'You drew a {i.cards[-1].rank} of {i.cards[-1].suit}')
                    print_hand(i, False)
                i.update()
                print_score(position.name, i)
                first_action = False
            print(f'Player stands with: {i.value + 10}' if i.ace else f'You have: {i.value}')

    def deal():    # Deal Cards
        active_deck.burn()  # burn first card as in casinos
        for i in range(2):  # initial draw (both players)
            for person in Player.all_players:
                person.hand.cards.append(active_deck.draw())

        for person in Player.all_players:
            person.hand.update()
            if isinstance(person, Dealer):
                print_hand(person.hand, True)
                print(f'{person.name} has: {person.hand.cards[0].rank} of {person.hand.cards[0].suit},'
                      f' and one card face down')
            else:
                print_hand(person.hand, False)
                print(f'{person.name} has: {person.hand.cards[0].rank} of {person.hand.cards[0].suit},'
                  f' {person.hand.cards[1].rank} of {person.hand.cards[1].suit}')
            wait_time()

    def print_score(name, hand):
        print(f'{name} has: {hand.value} ({hand.value + 10})'
              if hand.ace else f'{name} has: {hand.value}')

    def print_hand(hand, dealer_hidden):  # NOT YET FIXED
        card_design = [' ___ ',
                       '|{} |',  # spacer will adjust format for 10
                       '| {} |',
                       '|_{}|']  # spacer will adjust format for 10
        hand_graphic = [[], [], [], []]
        for card in hand.cards:
            spacer1 = ' '
            spacer2 = '_'
            num_char = str(card.rank)
            suit_char = str(card.suit)
            if card.rank == 10 and not dealer_hidden:  # adjust only if card is not hidden for case 10 only
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

    def resolve_hand(hand):
        # Blackjack - Player (Win), also Dealer Blackjack (Draw/Push)
        # Player Bust (Lose)
        # Dealer Bust (Win)
        # Player > Dealer (Win) / Draw/Push / Lose (P<D)

        if hand.blackjack:  # If player has Blackjack
            if dealer.hand.blackjack:  # If Dealer also has Blackjack
                print(f'{person.name}: Draw. Bets returned.')
                return person.hand.bet  # Return bet only
            else:
                print(f'{person.name} has Blackjack (21)! Player wins!')
                return int(person.hand.bet * 2.5)  # Return bet + winnings at 3:2
        elif person.hand.value > 21:
            print(f'{person.name}: Bust! Bet lost.')  # Bet already deducted
            return 0
        elif dealer.hand.value > 21:
            print(f'{person.name}: {dealer.name} is bust!')
            print(f'{person.name} wins with {person.hand.value}')
            return int(person.hand.bet * 2) # Return bet + winnings at 2:2
        elif person.hand.value > dealer.hand.value:
            print(f'{person.name}: wins with {person.hand.value}')
            return int(person.hand.bet * 2) # Return bet + winnings at 2:2
        elif person.hand.value == dealer.hand.value:
            print(f'{person.name}: Draw. Bets returned.')
            return person.hand.bet  # Return bet only
        else:  # Player < Dealer
            print(f'{person.name}: Dealer wins with {dealer.hand.value}')
            return 0

    # INITIAL SETUP
    print(f'{chr(9827) + chr(9829) + chr(9830) + chr(9824)} BLACKJACK {chr(9827) + chr(9829) + chr(9830) + chr(9824)}')
    SHOE = 6  # Shoe is the number of decks/size of the deck used in Blackjack. Casinos often use a 6-deck shoe.
    active_deck = Deck(SHOE)
    active_deck.generate(SHOE)
    player_1 = Player("Player 1".upper())
    dealer = Dealer()
    hand_count = 0

    while True:  # playing at 'table'
        for person in Player.all_players:
            person.reset_hand()

        # Change Deck
        if len(active_deck.cards) < 105:
            active_deck.clear()
            active_deck.generate(SHOE)  # Create and shuffle decks(n) of 52 cards (SHOE)
            print('New deck in play')
            hand_count = 0

        # Betting
        hand_count += 1
        print(f'HAND #{hand_count}:')
        for person in Player.all_players:
            if not isinstance(person, Dealer):
                betting(person)
        # Deal Cards
        deal()

        # PLAYER TURNS
        for person in Player.all_players:
            if not isinstance(person, Dealer):
                player_turn(person)
                wait_time()

        # DEALER TURN - after all players - # STILL GOES EVEN IF SINGLE PLAYER AND BUSTS - NEED TO FIX!!!
        dealer_turn(dealer)

        # Calculate Results
        print('\nRESULTS:')
        for person in Player.all_players:
            if not isinstance(person, Dealer):
                person.funds += resolve_hand(person.hand)
            if len(person.split_hand.cards) != 0:
                person.funds += resolve_hand(person.split_hand)

        # Play again? If not, breaks outermost loop and ends programme
        try:
            wait_time()
            play_again = input('\nPlay again? (Y/N):')
            if play_again.upper() == 'N':
                print('\nThanks for playing!')
                wait_time()
                break
            elif player_1.funds < 10:
                print('Oops! You''re out of money!\nThanks for playing!')
                wait_time()
                break
        except ValueError:
            print('Invalid input! Type ''Y'' or ''N''')
            print()

def blackjack():
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

    def p_action():
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
        global p_wallet, p_bet
        p_score, p_ace = get_value(p_hand)
        d_score, d_ace = get_value(d_hand[1:])
        print(f'Dealer has: {d_score} ({d_score + 10})' if d_ace else f'Dealer has: {d_score}')
        if p_score + 10 == 21 and p_ace:  # Only way to achieve this is if you have an ace (1) + a face/10 (10) = 11 (21)
            print('Player has Blackjack (21)!')
            return 21
        print(f'You have: {p_score} ({p_score + 10})' if p_ace else f'You have: {p_score}')

        # add function here to split hands eventually if equal value cards show up in initial 2 drawn?
        while True:
            if p_score > 21:
                return p_score  # Ends turn without continuing through cards
            move = p_action()
            if move == 'S':  # Stand
                if p_ace:
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
            p_score, p_ace = get_value(p_hand)
            print(f'You have: {p_score} ({p_score + 10})' if p_ace else f'You have: {p_score}')
        print(f'Player stands with: {p_score}')
        return p_score

    def dealer_turn():
        print(f'Dealer reveals card: {d_hand[0][0]} of {d_hand[0][1]}')
        d_score, d_ace = get_value(d_hand)  # This time, add value of all cards
        print_hand(d_hand, False)
        print(f'Dealer has: {d_score} ({d_score + 10})' if d_ace else f'Dealer has: {d_score}')
        # DOES DEALER EVER SPLIT?? add function here to split hands eventually if equal value cards show up in initial 2 drawn?
        while True:
            wait_time()
            if d_score > 21:  # Bust
                break
            elif d_ace == True and (17 <= d_score + 10 <= 21):
                d_score += 10  # if ace, use higher score
                break
            elif d_score >= 17:  # Dealer stands at 17  -  or d_score > p_score  # Dealer stands if ahead and under 17
                break
            d_hand.append(draw())
            d_score, d_ace = get_value(d_hand)  # This time, add value of all cards
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
    # blackjack()
    blackjack_oop()

if __name__ == '__main__':
    main()

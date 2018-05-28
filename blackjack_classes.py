
import random

#Card class

class Card:

    def __init__(self, suit, name, value):
        self.suit = suit
        self.name = name
        self.value = value

    def __str__(self):
        return str(self.name + " of " + self.suit)

#Deck class

class Deck:

    def __init__(self):
        self.cards = []
        value = 1
        suits = ["Hearts", "Spades", "Diamonds", "Clubs"]
        names = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]

        for suit in suits:
            value = 1
            for name in names:
                self.cards.append(Card(suit, name, value))
                if value < 10:
                    value += 1
        random.shuffle(self.cards)

    def draw_a_card(self):
        return self.cards.pop()


    def __str__(self):
        for card in self.cards:
            print(card)
        return ""

#Shoe class - group of decks
class Shoe(Deck):

    def __init__(self, num_decks = 6):
        self.cards = []
        self.decks = []

        for _ in range(num_decks):
            self.decks.append(Deck())

        for deck in self.decks:
            for card in deck.cards:
                self.cards.append(card)

        random.shuffle(self.cards)

    def count(self):
        return len(self.cards)

#Hand class
class Hand:

    def __init__(self):
        self.cards = []
        self.bet = 0

    def add_card(self, card):
        self.cards.append(card)

    def hand_value(self):
        value = 0
        for card in self.cards:
            value += card.value
        for card in self.cards:
            if value <= 11 and card.name == "Ace":
                value += 10
        return value

    def check_21(self):
        if self.hand_value() == 21:
            return True
        else:
            return False

    def check_bust(self):
        if self.hand_value() > 21:
            print("Bust!")
            return True
        else:
            return False

    def place_bet(self, bet=10):
        self.bet = bet

    def double_down(self):
        print("Player doubled down.")
        self.bet += self.bet

    def surrender(self):
        print("Player surrenders.")
        self.money -= (self.bet / 2)

    def __str__(self):
        for card in self.cards:
            print(card)
        print("Total value: " + str(self.hand_value()))
        return ""


#Player class

class Player:

    def __init__(self):
        self.hands = [Hand()]
        self.hand_count = 1
        self.insurance = 0
        self.money = 100

    def print_hands(self):
        for count in range(self.hand_count):
            print(self.hands[count])

    def player_turn(self, player_input, deck):
        if player_input == "1":     #player hits
            print("Player hits.")
            print()
            self.add_card(deck.draw_a_card())
            return True
        elif player_input == "2":   #player doubled down
            self.double_down()
            self.add_card(deck.draw_a_card())
            return True
        elif player_input == "3":   #player surrenders
            self.surrender()
            return False
        else:
            print("Player stands.")
            print()
            return False

    def buy_ins(self, ins):
        print("Player buys insurance.")
        self.insurance = ins

    def pay_ins(self):
        print("The player collects insurance.")
        self.money += (2 * self.insurance)

    def lose_ins(self):
        print("The player loses insurance.")
        self.money -= self.insurance

    def can_split(self, hand = 0):
        if self.hands[hand].cards[0].value == self.hands[hand].cards[1].value:
            return True
        else:
            return False

    def split_hand(self, deck):
        self.hands.append(Hand())
        self.hands[1].cards.append(self.hands[0].cards.pop())
        self.hand_count += 1
        for hand in range(self.hand_count):
            self.hands[hand].add_card(deck.draw_a_card())

    def player_wins(self):
        print("Player wins!")
        print(self)
        self.money += self.bet

    def player_loses(self):
        self.money -= self.bet

    def __str__(self):
        for hand in self.hands:
            print(hand)
        return ""

#Dealer class

class Dealer(Player):

    def __init__(self):
        self.hands = [Hand()]
        self.hand_count = 1

    def player_turn(self, deck, max_on_hit = 16):
        if self.hand_value() <= max_on_hit:
            print("Dealer hits.")
            print()
            self.add_card(deck.draw_a_card())
            return True
        else:
            print("Dealer stands.")
            print()
            return False

    def deal_hand(self, other, deck):
        for _ in range(2):
            other.hands[0].add_card(deck.draw_a_card())
            self.hands[0].add_card(deck.draw_a_card())

        print("Dealer's top card: ")
        print(self.hands[0].cards[0])
        print()

        print("Player's hand: ")
        other.print_hands()

        for count in range(other.hand_count):
            if other.can_split(count):
                split_input = input("Would you like to split? Y or N ")
                if split_input.lower() == "y":
                    player.split_hand(deck)
                    print("Player's hands: ")
                    other.print_hands()


    def compare_hands(self, other):
        if other > self.hand_value():
            other.player_wins()
        elif other == self.hand_value():
            print("It's a draw.")
        else:
            self.player_wins(other)

    def player_wins(self, other):
        print("Dealer wins!")
        print(self)
        other.player_loses()

    def has_ace(self):
        if self.hands[0].cards[0].name == "Ace":
            return True
        else:
            return False


##########################################

deck = Deck()
player = Player()
dealer = Dealer()

dealer.deal_hand(player, deck)

player.print_hands()
dealer.print_hands()

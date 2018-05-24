
#Create a game of Blackjack
#Actors: Card, Deck, Player, Dealer

#Card - hold info about the card, suite, type, and value

#Deck - holds a group of Cards, able to deliver a single called at a time, shuffles those cards when created
#   Collab: Card is an association, will be used by Player

#Player - will have a hand made up of cards taken from the deck, given to it by the Dealer.  Needs to be able to calculate
#the value of the hand and have the option to hit (draw another card) or stay.
#   Collab: Card is an association for the hand, dependancy on Dealer for cards

#Dealer - subtype of Player which has the additional function of dealing cards

#Rules:
#object of the game is to get closer to 21 than the dealerself.
#if you get 21 you auto win
#if less than 21 you can hit or stay
#if you go over 21 you auto lose

#Start of classes
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

#Player class

class Player:

    def __init__(self):
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def hand_value(self):
        value = 0
        for card in self.hand:
            value += card.value
        for card in self.hand:
            if value <= 11 and card.name == "Ace":
                value += 10
        return value

    def player_turn(self, player_input, deck):
        if player_input == "1":
            print("Player hits.")
            print()
            self.add_card(deck.draw_a_card())
            return True
        else:
            print("Player stands.")
            print()
            return False

    def check_21(self):
        if self == 21:
            return True
        else:
            return False

    def check_bust(self):
        if self > 21:
            return True
        else:
            return False

    def __eq__(self, value):
        return self.hand_value() == value

    def __lt__(self, value):
        return self.hand_value() < value

    def __gt__(self, value):
        return self.hand_value() > value

    def __str__(self):
        for card in self.hand:
            print(card)
        print("Total value: " + str(self.hand_value()))
        return ""

#Dealer class

class Dealer(Player):

    def __init__(self):
        self.hand = []

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

    def deal_hand(self, other):
        for _ in range(2):
            other.add_card(deck.draw_a_card())
            self.add_card(deck.draw_a_card())

"""
    def check_21(self, other):
        if other == 21 and self == 21:
            print("It's a tie.")
        elif other == 21:
            print("Player wins!")
        elif self == 21:
            print("Deal wins!")
"""





#Start of program

player = Player()
dealer = Dealer()

player_state = True
wants_to_play = True

player_win = False
player_bust = False
dealer_win = False
dealer_bust = False

#Start of game

while wants_to_play:

    deck = Deck()

    #Deal a hand
    dealer.deal_hand(player)

    #check for 21 at the beginning
    if player.check_21():
        print("Player wins!")
        break
    if dealer.check_21():
        print("Dealer wins!")
        break

    #Player's turn

    print("Player's turn. You have: ")
    print(player)

    while player_state:
        player_input = input("Enter 1 to hit or any to stand: ")
        player_state = player.player_turn(player_input, deck)
        if player.check_21():
            print("Player wins!")
            player_win = True
            break
        elif player.check_bust():
            print("Player busts, dealer wins!")
            player_bust = True
            break
        print("You have: ")
        print(player)

    if player_win:
        break

    #Reset state for dealer

    player_state = True

    #Dealer's turn

    print("Dealer's turn.  Dealer has: ")
    print(dealer)

    while player_state:
        player_state = dealer.player_turn(deck)
        print(dealer)

    #Everyone has stayed, need to compare
    if player > dealer.hand_value():
        print("Player wins!")
    elif player == dealer.hand_value():
        print("It's a draw.")
    else:
        print("Dealer wins!")

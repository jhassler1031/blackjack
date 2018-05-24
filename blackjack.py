
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
        return value


#Start of program

deck = Deck()

john = Player()

john.add_card(deck.draw_a_card())
john.add_card(deck.draw_a_card())

print(john.hand_value())

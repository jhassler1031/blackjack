
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
        self.money = 100
        self.bet = 0

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

    def player_wins(self):
        print("Player wins!")
        print(self)
        self.money += self.bet

    def player_loses(self):
        self.money -= self.bet

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






#Start of program




wants_to_play = True
player = Player()
dealer = Dealer()

#Start of game

while wants_to_play:

    #Initialize player hands and game control variables
    player.hand = []
    dealer.hand = []
    deck = Deck()
    player_state = True
    player_win = False
    player_bust = False
    dealer_win = False
    dealer_bust = False

    print(f"Player has ${player.money} in the bank.")

    while True:

        #Take bet
        while True:
            bet = int(input(f"Place your bet between $1-{player.money} (default is $10): "))
            if bet > 0 and bet <= player.money:
                player.place_bet(bet)
                break
            else:
                print("That is not a valid bet amount.")

        #Deal a hand
        dealer.deal_hand(player)

        #check for 21 at the beginning
        if player.check_21() and dealer.check_21():
            print("It's a draw.")
            break
        elif player.check_21():
            player.player_wins()
            break
        elif dealer.check_21():
            dealer.player_wins(player)
            break

        #Player's turn

        print("Player's turn. You have: ")
        print(player)

        while player_state:
            player_input = input("Enter 1 to hit or any to stand: ")
            player_state = player.player_turn(player_input, deck)
            if player.check_21():
                player.player_wins()
                player_win = True
                break
            elif player.check_bust():
                dealer.player_wins(player)
                player_bust = True
                break
            print("You have: ")
            print(player)

        if player_win:
            break
        elif player_bust:
            break

        #Reset state for dealer

        player_state = True

        #Dealer's turn

        print("Dealer's turn.  Dealer has: ")
        print(dealer)

        while player_state:
            player_state = dealer.player_turn(deck)
            if dealer.check_21():
                dealer.player_wins(player)
                dealer_win = True
                break
            elif dealer.check_bust():
                player.player_wins()
                dealer_bust = True
                break
            print(dealer)

        if dealer_win:
            break
        if dealer_bust:
            break

        #Everyone has stayed, need to compare

        dealer.compare_hands(player)
        break

    #Game over, check if the player would like to play again, and has funds to do so
    if player.money > 0:
        if (input("Would you like to play again?  (Y or N): ").lower()) != "y":
            wants_to_play = False
    else:
        print("Sorry, you're broke.")
        wants_to_play = False

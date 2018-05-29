
#Create a game of Blackjack
#Actors: Card, Deck, Player, Dealer, Shoe, Hand

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

from blackjack_classes import *

wants_to_play = True
player = Player()
dealer = Dealer()
deck = Shoe()

#Start of game

while wants_to_play:

    #Initialize player hands and game control variables
    player.hands = [Hand()]
    dealer.hands = [Hand()]
    #player_turn = 1
    player_state = True
    hand_state = True
    player_win = False
    player_bust = False
    dealer_win = False
    dealer_bust = False

    #Check if Shoe needs reshuffle
    if deck.count() <= 26:
        deck = Shoe()

    print(f"Player has ${player.money} in the bank.")

    #Begins a new game

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
        dealer.deal_hand(player, deck)

        print("Dealer's top card: ")
        print(dealer.hands[0].cards[0])
        print()

        print("Player's hand: ")
        player.print_hands()

        #Check if player wants insurance
        want_ins = ""

        if dealer.has_ace():
            want_ins = input("Would the player like to buy insurance? Y or N: ")
            if want_ins.lower() == "y":
                while True:
                    ins_amount = input("Enter amount for insurance (cannot be more than half your bet): ")
                    ins_amount = int(ins_amount)
                    if ins_amount > 0 and ins_amount < (player.bet / 2) + 1:
                        break
                    else:
                        print("Invalid amount.")
                player.buy_ins(ins_amount)

        #check dealer for 21 and insurance payout if purchased
        if player.hands[0].check_21() and dealer.hands[0].check_21():
            print("It's a draw.")
            if want_ins.lower() == "y":
                player.pay_ins()
            break  #breaks from game loop
        elif player.hands[0].check_21():
            player.player_wins()
            if want_ins.lower() == "y":
                player.lose_ins()
            break
        elif dealer.hands[0].check_21():
            if want_ins.lower() == "y":
                player.pay_ins()
            dealer.player_wins(player)
            break

        if want_ins.lower() == "y":
            player.lose_ins()

        #Player's turn

        #check for split
        for count in range(player.hand_count):
            if player.can_split(count):
                split_input = input("Would you like to split? Y or N ")
                if split_input.lower() == "y":
                    player.split_hand(deck)
                    print("Player's hands: ")
                    player.print_hands()

        #Check for double down or surrender
        player_input = input("""
Would the player like to double down (1)
Surrender (2))
Play on (Enter):
""")
        if player_input == "1":   #player doubled down
            player.double_down()
        elif player_input == "2":   #player surrenders
            player.surrender()
            player_state = False

        #Play hand(s)

        while player_state:
            hand_state = True
            for count in range(player.hand_count):
                print("Current hand: ")
                print(player.hands[count])
                while hand_state:
                    player_input = input("Enter 1 to hit or Enter to stand: ")

                    hand_state = player.player_turn(player_input, count, deck)

                    if player.hands[count].check_21():
                        player.player_wins()
                        player_win = True
                        break
                    elif player.hands[count].check_bust():
                        dealer.player_wins(player)
                        player_bust = True
                        break
                    print("You have: ")
                    print(player)
            break


        #End of player's turn
        if player.hand_count == 1:
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
            if dealer.hands[0].check_21():
                dealer.player_wins(player)
                dealer_win = True
                break
            elif dealer.hands[0].check_bust():
                player.player_wins()
                dealer_bust = True
                break
            print(dealer)

        if player.hand_count == 1:
            if dealer_win:
                break
            if dealer_bust:
                break

        #End of Dealer's turn

        #Everyone has stayed, need to compare
        for count in range(player.hand_count):
            dealer.compare_hands(player, count)
        break

    #Game over, check if the player would like to play again, and has funds to do so
    if player.money > 0:
        if (input("Would you like to play again?  (Y or N): ").lower()) != "y":
            wants_to_play = False
    else:
        print("Sorry, you're broke.")
        wants_to_play = False

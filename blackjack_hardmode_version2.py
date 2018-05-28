
from Blackjack_classes import *

wants_to_play = True
player = Player()
dealer = Dealer()
deck = Shoe()

#Start of game

while wants_to_play:

    #Initialize player hands and game control variables
    player.hand = []
    dealer.hand = []
    player_turn = 1
    player_state = True
    player_win = False
    player_bust = False
    dealer_win = False
    dealer_bust = False

    #Check if Shoe needs reshuffle
    if deck.count() <= 26:
        deck = Shoe()

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

        print("Dealer's top card: ")
        print(dealer.hand[0])
        print()

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

        #check for 21 at the beginning
        if player.check_21() and dealer.check_21():
            print("It's a draw.")
            break
        elif player.check_21():
            player.player_wins()
            break
        elif dealer.check_21():
            if want_ins.lower() == "y":
                player.pay_ins()
            dealer.player_wins(player)
            break

        if want_ins.lower() == "y":
            player.lose_ins()

        #Player's turn

        print("Player's turn. You have: ")
        print(player)

        while player_state:

            player_split = False

            if player_turn == 1:
                #if player has duplicate cards, offer to split
                if player.can_split():
                    split_input = input("Would you like to split? Y or N ")
                    if split_input.lower() == "y":
                        player.split_hand(deck)
                        player_split = True

                else:

                    player_input = input("""
1 to hit,
2 to double down,
3 to surrender,
Enter to stand: """)


            else:
                player_input = input("Enter 1 to hit or any to stand: ")

            player_state = player.player_turn(player_input, deck)

            if player_input == "3":
                break

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

            player_turn += 1

        #End of player's turn

        if player_win:
            break
        elif player_bust:
            break
        elif player_input == "3":
            break

#if player split, need to run through playing with split hand

        #start of split hand
        if player_split:

            player_state = True

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


        #End of player's split turn

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

        #End of Dealer's turn

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

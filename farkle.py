
rules = """RULES:
6 dice

Find first person, each player rolls one die, highest wins, ties must re-roll till one winner
During each roll, player must have at least one die that is playable
If more than one playable die(dice), player must choose which ones to keep or keep all
In order to get on the scoreboard, players must attain a cumulative score of 450 points during a single turn
  afterwards, a player could keep as little as 50 points (that being the lowest possible score) and up to as much as a
  player can achieve in a single turn.
All playable dice that are kept must be taken out of play and kept showing their playable value until the player has
  no more dice to roll.
If a player is on the scoreboard and is rolling but has 5 kept dice, that player can choose to stop and receive the
  current points or can roll the last die.
If a player has kept all playable dice and has no more dice to roll, the player must roll all 6 dice again.
If during the turn a player has no playable die(dice), the player farkles loses all the points from that turn
  and is next players turn.
At no time can a player add dice from one roll to another roll to change that roll. All rules are for individual rolls

PLAYABLE ROLLS:
  1 and 5:
      1 = 100
      5 = 50
 Triples:
      These rules apply to individual roll cases and cannot be combined with multiple rolls
      2 = 200
      3 = 300
      4 = 400
      5 = 500
      6 = 600
      1 = 1,100
      Each additional die that is the same as the triple adds 100 points per extra die up to 5 dice
      Note - If player rolls all 6 dice of the same number, they win
      If player gets two sets of Triples, then the player can choose to keep one or both Triples.
      In case player chooses both Triples, simply add the value of each Triple together for the score, however,
          the player must roll again.
  Pairs:
      Must have three sets of pairs in a single roll to count
      3 sets of pairs = 500
      Must roll again
  Straight:
      Must have the straight in a single roll to count as a straight
      1 - 6 = 1,500
      Must roll again

WINNING CONDITIONS:
  The first player to reach 10,000 points sets the game to end, but all players must roll until they beat the
  winning players score or farkle. If no other player beats the winning score, the player with the winning score wins.
  However, if another player beats the winning score than the player with the initial winning score rolls to beat the
  new score or farkle. This will go on until one of the players farkles, whoever did not farkle thus wins.
  Important - If at anytime a player rolls all 6 dice in a single roll that are the same number, that player wins."""

import random

SCORING = {"singles": {1: 100, 5: 50}, "triples": {2: 200, 3: 300, 4: 400, 5: 500, 6: 600, 1: 1100},
           "3 sets of pairs": 500, "straight": 1500, "six of a kind": "WIN"}
PLAYABLE_DICE = [[1], 100, [5], 50,
                 [2, 2, 2], 200, [3, 3, 3], 300, [4, 4, 4], 400, [5, 5, 5], 500, [6, 6, 6], 600, [1, 1, 1], 1100,
                 [2, 2, 2, 2], 300, [3, 3, 3, 3], 400, [4, 4, 4, 4], 500, [5, 5, 5, 5], 600, [6, 6, 6, 6], 700,
                 [1, 1, 1, 1], 1200, [2, 2, 2, 2, 2], 400, [3, 3, 3, 3, 3], 500, [4, 4, 4, 4, 4], 600,
                 [5, 5, 5, 5, 5], 700, [6, 6, 6, 6, 6], 800, [1, 1, 1, 1, 1], 1300,
                 [1, 2, 3, 4, 5, 6], 1500
                 ]

score_sheet = {}
# Add list of names to compete against. Each one with have a level of difficulty
# The 'AIs' will have a risk factor that is predetermined to figure how often they will hold after each roll
#   and to what type of dice they will select each roll
# Initial 'AI' will always hold any playable dice and stop rolling in a safe margin
# I suppose I could use a for loop with a range that selects a number between n and m and each 'AI' will have
#   set numbers attached to it that will force them to stop rolling.
# Will have to keep track of who is rolling in order to update score
run = True
num_dice = 6
kept_dice = []


did_farkle = "roll"
# Add a check if player on scoreboard, if player is not on scoreboard, they have to keep rolling. If they are
#   on the scoreboard, they will no longer be prompted.
# print(score_sheet)
# Solved - if player keeps anything other than single die i have to figure out how to keep them separated for scoring
# Solve - Tell player that if type stop, all kept dice will be will be scored and added to score.
show_rules = input("Would you like to know how to play? (y/n)?\n")
if show_rules == "y":
    print(rules)
    print("""All single playable dice, type each one in with a space between, no space at end
             If you have three or more of a kind, three sets of pairs, or a straight, type those in with no spaces
             If you have two three of a kinds, type them in with only one space between the two sets of triples
             """)
    start = input("Would you like to start now? (y/n)\n")
    if start == "y":
        name = input("What is your name?\n")
        score_sheet[name] = 0
else:
    name = input("What is your name?\n")
    score_sheet[name] = 0

while run:
    # When starting with 'AIs', have player roll one die to see who gets to go first.
    dice = []
    dice_count = {}
    for i in range(num_dice):
        dice.append(random.randrange(1, 7))
    #         adds random numbers to dice based on how many dice are available

    for i in range(len(dice)):
        dice_count[dice[i]] = dice.count(dice[i])
    #     adds how many dice of each specific value rolled to the dice_count dict

    # this next block checks for all playable dice in each roll and tells player if they have those kinds of dice
    #     otherwise it sends the code to a block that deals with farkle
    if len(dice) == 6:
        if (1 in dice_count or 5 in dice_count) or len(dice_count) == 2 or \
         len(dice_count) == 3 or len(dice_count) == 6:
            print("you have playable dice")
        elif len(dice) == 1:
            print("You Win!!")
            break
        else:
            did_farkle = "Farkle"
    elif len(dice) == 5:
        if (1 in dice_count or 5 in dice_count) or len(dice_count) == 3 or len(dice_count) == 2 or len(dice_count) == 1:
            print("you have playable dice")
        else:
            did_farkle = "Farkle"
    elif len(dice) == 4:
        if 1 in dice_count or 5 in dice_count or len(dice_count) == 1 or \
            (len(dice_count) == 2 and (dice_count.get(2) == 3 or dice_count.get(3) == 3 or
                                       dice_count.get(4) == 3 or dice_count.get(6) == 3)):
            print("you have playable dice")
        else:
            did_farkle = "Farkle"
    elif len(dice) == 3:
        if (1 in dice_count or 5 in dice_count) or len(dice_count) == 1:
            print("you have playable dice")
        else:
            did_farkle = "Farkle"
    elif len(dice) <= 2:
        if 1 in dice_count or 5 in dice_count:
            print("you have playable dice")
        else:
            did_farkle = "Farkle"
    print(*dice, sep=" ")
    # this prints out the new roll of dice
    # Put in a rolling... with a timer so it looks like it is rolling and not instant, sets a more comfortable pace


    if did_farkle == "roll":
        # this if statement looks at a state variable called did_farkle. If roll, carry on with the block below
        keep_dice = [str(input("What dice do you want to keep?\n")).split()]
#       Need to put in restrictions to numbers only, with spaces where necessary.
#       Need restrictions on only being able to pick playable dice
        # splits dice into a list inside a list
        add_spaces = [[" ".join(j)] if len(j) > 1 else [j] for i in keep_dice for j in i]
        split_multiples = [sub.split() for subl in add_spaces for sub in subl]
        # if more than one dice in sublist, this splits them into separated elements inside sublist
        int_conversion = [[int(x) for x in lst] for lst in split_multiples]
        for dice in int_conversion:
            kept_dice.append(dice)
        #     add the dice kept to kept dice
            for _ in dice:
                num_dice -= 1
        #         as the dice are kept, the amount of dice being rolled is lowered
        if num_dice == 0:
            num_dice += 6
        #     if all dice are kept and none left to roll, a new round is started by adding six dice to roll
        keep_rolling = input("Do you want to keep rolling? (y,n)\n")
        # Instead of keep_rolling, type stay at end of turn to tally score and move to next person
        if keep_rolling == "n":
            remaining_dice = 6 - num_dice
            num_dice = num_dice + remaining_dice
            # the above two lines reset the dice count first by finding out how many were kept then adding what is
            #   left by the quantity of what was kept back to 6
            score = 0
            for i in kept_dice:
                if i in PLAYABLE_DICE:
                    score += PLAYABLE_DICE[PLAYABLE_DICE.index(i) + 1]
                #     this goes through all the kept dice
                elif i not in PLAYABLE_DICE and len(i) == 6 and \
                    ((i.count(1) or i.count(2) or i.count(3) or i.count(4) or i.count(5) or i.count(6)) > 1):
                    score += 500
            for i in score_sheet:
                score_sheet["Drew"] += round(score)
            kept_dice.clear()
            print(score_sheet)
            print(f"You scored {round(score)} this round")
        elif keep_rolling == "y":
            continue
    elif did_farkle == "Farkle":
        remaining_dice = 6 - num_dice
        num_dice = num_dice + remaining_dice
        print(kept_dice)
        print("You Farkled")
        kept_dice.clear()
        did_farkle = "roll"
    # Solved - add the kept_dice conversion. use the list that you will copy from as the list
    #   that will decide how many times num_dice will be subtracted from


import random
import time
from collections import deque

SCORING = {"singles": {1: 100, 5: 50}, "triples": {2: 200, 3: 300, 4: 400, 5: 500, 6: 600, 1: 1100},
           "3 sets of pairs": 500, "straight": 1500, "six of a kind": "WIN"}
PLAYABLE_DICE = [[1], 100, [5], 50,
                 [2, 2, 2], 200, [3, 3, 3], 300, [4, 4, 4], 400, [5, 5, 5], 500, [6, 6, 6], 600, [1, 1, 1], 1100,
                 [2, 2, 2, 2], 300, [3, 3, 3, 3], 400, [4, 4, 4, 4], 500, [5, 5, 5, 5], 600, [6, 6, 6, 6], 700,
                 [1, 1, 1, 1], 1200, [2, 2, 2, 2, 2], 400, [3, 3, 3, 3, 3], 500, [4, 4, 4, 4, 4], 600,
                 [5, 5, 5, 5, 5], 700, [6, 6, 6, 6, 6], 800, [1, 1, 1, 1, 1], 1300,
                 [1, 2, 3, 4, 5, 6], 1500
                 ]

class Farkle:

    def __init__(self):
        self.score_sheet = {}
# Solved - Add list of names to compete against. Each one with have a level of difficulty
# Pending - The 'AIs' will have a risk factor that is predetermined to figure how often they will hold after each roll
#   and to what type of dice they will select each roll
# Initial 'AI' will always hold any playable dice and stop rolling in a safe margin
# Solved - I suppose I could use a for loop with a range that selects a number between n and m and each 'AI' will have
#   set numbers attached to it that will force them to stop rolling.
# Will have to keep track of who is rolling in order to update score
        self.num_dice = 6
        self.kept_dice = []
        self.organize = []
        self.sift = []
        self.opponents = ["Bill", "Ted", "Greg", "James", "Carl", "Tim", "Kyle", "Doug", "Peter", "Al", "Eddy"]
        self.difficulty = {"easy": [1, 2, 3, 4, 5, 6, 7, 8, 9], "medium": [1, 2, 3, 4, 5, 6, 7], "hard": [1, 2, 3, 4, 5]}
        self.comp_players = {}
        self.player_order = []
        self.score_sheet = {}
        self.whos_first = []
        self.player = ""
        self.current_player = ""
# Add a check if player on scoreboard, if player is not on scoreboard, they have to keep rolling. If they are
#   on the scoreboard, they will no longer be prompted.
# Solved - if player keeps anything other than single die i have to figure out how to keep them separated for scoring
# Solve - Tell player that if type stop, all kept dice will be will be scored and added to score.

    def main(self):
        """Starts the game and acts as the main menu"""
        print("Hello. Welcome to Farkle.")
        name = input("What is your name?\n")
        self.score_sheet[name] = 0
        self.player = name
        show_rules = input("Would you like to know how to play? (y/n)?\n")
        if show_rules == "y":
            return show_rules, Farkle.rules(self, show_rules)
        elif show_rules == "n":
            return show_rules, Farkle.rules(self, show_rules)
        else:
            if not show_rules.isalpha():
                print("Please type y for yes or n for no")
                Farkle.main(self)

    def rules(self, show_rules):
        """This lets user choose to see rules, but if not, the keep the dice rules still display"""
        if show_rules == "y":
            rules_file = open("FarkleRules.txt", "r", encoding="utf-8")
            for i in rules_file.readlines():
                print(i.strip("\n"))
            rules_file.close()
            start = input("Would you like to start now? (y/n)\n")
            if start == "y":
                Farkle.opponents_difficulty(self)
            elif start == "n":
                exit()
            else:
                if not start.isalpha():
                    print("Please type y for yes or n for no")
        elif show_rules == "n":
            keeping_dice_file = open("KeepingDice.txt", "r", encoding="utf-8")
            for i in keeping_dice_file.readlines():
                print(i.strip("\n"))
            keeping_dice_file.close()
            Farkle.opponents_difficulty(self)

    def opponents_difficulty(self):
        """Sets random difficulty for all possible opponents"""
        choice_of_comp_players = {}
        num = 1
        for name in self.opponents:
            for diff in random.choice(list(self.difficulty.items())):
                choice_of_comp_players[name] = diff
        dif = list(self.difficulty.keys())
        cp = list(choice_of_comp_players.values())
        dif_val = list(self.difficulty.values())
        # print(cp)
        for pl in cp:
            dif_position = dif_val.index(pl)
            print(num, self.opponents[num - 1], dif[dif_position])
            num += 1
        return choice_of_comp_players, Farkle.choose_opponents(self, choice_of_comp_players)

    def choose_opponents(self, choice_of_comp_players):
        """This let's player choose their opponents"""
        select_opponent = input("From the list above, choose up to 5 opponents using the "
                                "number next to their names with spaces between\n").split()
        for i in select_opponent:
            op = self.opponents[int(i) - 1]
            self.comp_players[op] = choice_of_comp_players[op]
            self.score_sheet[op] = 0
        Farkle.roll_for_first(self)
        # print(select_opponent)
        # print(self.comp_players)
        # print(choice_of_comp_players)

    def roll_for_first(self):
        """Automatically rolls a die for each comp including player and establishes who goes first"""
# Solved - I think I'll have to just make a list of the dice rolled in order of the people in the dict plus the player,
#   then iterate over the list, first checking for the highest number, then counting that number to see if any
#   duplicates and if so, make those duplicates re-roll until no more duplicates.
        for _ in self.score_sheet:
            dice = random.randrange(1, 7)
            self.whos_first.append(dice)

        highest_num = max(self.whos_first)
        highest_num_count = self.whos_first.count(max(self.whos_first))
        highest_rolls_index = {}

        for i, j in enumerate(self.whos_first):
            if j == highest_num and highest_num_count > 1:
                highest_rolls_index[i] = j
        # print(self.whos_first)
        # print(highest_rolls_index)

        if highest_rolls_index:
            for index in highest_rolls_index.keys():
                dice = random.randrange(1, 7)
                self.whos_first.pop(index)
                self.whos_first.insert(index, dice)
                highest_rolls_index[index] = dice
                # print(index)

        for index, _ in highest_rolls_index.items():
            if self.whos_first.count(max(highest_rolls_index.values())) <= 1:
                break
            else:
                dice = random.randrange(1, 7)
                self.whos_first.pop(index)
                self.whos_first.insert(index, dice)
                highest_rolls_index[index] = dice
                # print(index)
                # continue
        # print(self.whos_first)
        # print(highest_rolls_index)

        if not highest_rolls_index:
            rotate_player_order = deque(self.score_sheet)
            # print(rotate_player_order)
            rotate_player_order.rotate(len(self.whos_first) - self.whos_first.index(max(self.whos_first)))
            # print(rotate_player_order)
            rotate_player_order = list(rotate_player_order)
            # print(rotate_player_order)
            for i in rotate_player_order:
                self.player_order.append(i)
            self.current_player = self.player_order[0]
            if self.player_order[0] == self.player:
                print("You are first.")
            else:
                print(f"{self.player_order[0]} rolls first.")
            Farkle.roll_dice(self)
            # print(rotate_player_order)
            # print(self.player_order)
        else:
            c = max(highest_rolls_index, key=lambda key: highest_rolls_index[key])
            rotate_player_order = deque(self.score_sheet)
            # print(rotate_player_order)
            rotate_player_order.rotate(len(self.whos_first) - c)
            # print(rotate_player_order)
            rotate_player_order = list(rotate_player_order)
            for i in rotate_player_order:
                self.player_order.append(i)
            self.current_player = self.player_order[0]
            if self.player_order[0] == self.player:
                print("You are first.\n")
                time.sleep(.75)
                Farkle.roll_dice(self)
            else:
                print(f"{self.player_order[0]} rolls first.\n")
                time.sleep(.75)
                Farkle.roll_dice(self)
            # print(rotate_player_order)
            # print(self.player_order)

    def roll_dice(self):
        """This rolls the dice"""
        print(self.score_sheet)
        dice_count = {}
        dice = [random.randrange(1, 7) for _ in range(self.num_dice)]
        #         adds random numbers to dice based on how many dice are available
        for i in range(len(dice)):
            dice_count[dice[i]] = dice.count(dice[i])
        if self.current_player == self.player:
            input("Press r to roll\n")
            print("rolling...\n")
            time.sleep(1.25)
            print("You rolled:")
            return dice, dice_count, Farkle.farkle_check(self, dice, dice_count)
        else:
            print("Press r to roll")
            time.sleep(.25)
            print("r")
            print("rolling...\n")
            time.sleep(1.25)
            print("You rolled:")

        #     adds how many dice of each specific value rolled to the dice_count dict
            return dice, dice_count, Farkle.farkle_check(self, dice, dice_count)

    def farkle_check(self, dice, dice_count):
        """Checks to see if any player has playable dice or if farkle"""
        # this next block checks for all playable dice in each roll and tells player if they have those kinds of dice
        #     otherwise it sends the code to a block that deals with farkle
        print(*dice, "\n", sep=" ")
        if len(dice) == 6:
            if (1 in dice_count or 5 in dice_count) or len(dice_count) == 2 or \
             len(dice_count) == 3 or len(dice_count) == 6:
                if self.current_player == self.player:
                    Farkle.player_turn(self)
                else:
                    Farkle.comp_turn(self, dice, dice_count)
            elif len(dice) == 1:
                print("You Win!!")
                time.sleep(1.25)
                quit()
            else:
                time.sleep(.75)
                Farkle.farkled(self)
        elif len(dice) == 5:
            if (1 in dice_count or 5 in dice_count) or len(dice_count) == 2 or len(dice_count) == 1:
                if self.current_player == self.player:
                    Farkle.player_turn(self)
                else:
                    Farkle.comp_turn(self, dice, dice_count)
            else:
                time.sleep(.75)
                Farkle.farkled(self)
        elif len(dice) == 4:
            if 1 in dice_count or 5 in dice_count or len(dice_count) == 1 or \
                (len(dice_count) == 2 and (dice_count.get(2) == 3 or dice_count.get(3) == 3 or
                                           dice_count.get(4) == 3 or dice_count.get(6) == 3)):
                if self.current_player == self.player:
                    Farkle.player_turn(self)
                else:
                    Farkle.comp_turn(self, dice, dice_count)
            else:
                time.sleep(.75)
                Farkle.farkled(self)
        elif len(dice) == 3:
            if (1 in dice_count or 5 in dice_count) or len(dice_count) == 1:
                if self.current_player == self.player:
                    Farkle.player_turn(self)
                else:
                    Farkle.comp_turn(self, dice, dice_count)
            else:
                time.sleep(.75)
                Farkle.farkled(self)
        elif len(dice) <= 2:
            if 1 in dice_count or 5 in dice_count:
                if self.current_player == self.player:
                    Farkle.player_turn(self)
                else:
                    Farkle.comp_turn(self, dice, dice_count)
            else:
                time.sleep(.75)
                Farkle.farkled(self)

        # this prints out the new roll of dice
        # Put in a rolling... with a timer so it looks like it is rolling and not instant, sets a more comfortable pace

    def player_turn(self):
        stop_rolling = "roll"
        keep_dice = [str(input("What dice do you want to keep?\n")).split()]
        for i in keep_dice:
            for j in i:
                if j == "stop":
                    stop_rolling = i.pop(i.index(j))
        add_spaces = [[" ".join(j)] if len(j) > 1 else [j] for i in keep_dice for j in i]
        split_multiples = [sub.split() for subl in add_spaces for sub in subl]
        int_conversion = [[int(x) for x in lst] for lst in split_multiples]
        for dice in int_conversion:
            self.kept_dice.append(dice)
            for _ in dice:
                self.num_dice -= 1
        #         as the dice are kept, the amount of dice being rolled is lowered
        if self.num_dice == 0 and stop_rolling == "roll":
            self.num_dice += 6
            Farkle.roll_dice(self)
        elif self.num_dice > 0 and stop_rolling == "roll":
            Farkle.roll_dice(self)
        elif self.num_dice == 0 and stop_rolling == "stop":
            self.num_dice += 6
            stop_rolling = "roll"
            print("You rolled all the dice. You must continue rolling.\n")
            Farkle.roll_dice(self)
        elif self.num_dice > 0 and stop_rolling == "stop" and self.score_sheet[self.current_player] >= 450:
            remaining_dice = 6 - self.num_dice
            self.num_dice = self.num_dice + remaining_dice
            stop_rolling = "roll"
            Farkle.update_score(self, Farkle.current_score(self))
        elif self.num_dice > 0 and stop_rolling == "stop" and self.score_sheet[self.current_player] == 0:
            stop_rolling = "roll"
            Farkle.is_on_board(self, Farkle.current_score(self))


    def comp_turn(self, dice, dice_count):
        """Checks to see if comp player has """
        selected_dice = []
        print("What dice do you want to keep?\n")
        time.sleep(1.75)
        if len(dice) == 6:
            for i in dice:
                if len(dice_count) == 6:
                    # for straights
                    self.organize.append(i)
                    selected_dice.append(i)
                    self.num_dice -= 1
                elif len(dice_count) == 3 and dice_count[i] == 2 and all(dice_count[i] == 2 for i in dice_count):
                    # for three sets of pairs
                    self.organize.append(i)
                    selected_dice.append(i)
                    self.num_dice -= 1
                elif len(dice_count) == 2 and dice_count[i] == 3:
                    # for two threes of a kind
                    self.sift.append(i)
                    selected_dice.append(i)
                    self.num_dice -= 1
                    if i != self.sift[0]:
                        num = self.sift.pop()
                        self.organize.append(num)
                elif dice.count(i) >= 3:
                    self.organize.append(i)
                    selected_dice.append(i)
                    self.num_dice -= 1
                elif i == 1 or i == 5 in dice_count:
                    self.kept_dice.append([i])
                    selected_dice.append(i)
                    self.num_dice -= 1
        elif len(dice) == 5:
            for i in dice:
                if dice_count[i] >= 3:
                    self.organize.append(i)
                    selected_dice.append(i)
                    self.num_dice -= 1
                elif i == 1 or i == 5 in dice_count:
                    self.kept_dice.append([i])
                    selected_dice.append(i)
                    self.num_dice -= 1
        elif len(dice) == 4:
            for i in dice:
                if dice_count[i] >= 3:
                    self.organize.append(i)
                    selected_dice.append(i)
                    self.num_dice -= 1
                elif i == 1 or i == 5 in dice_count:
                    self.kept_dice.append([i])
                    selected_dice.append(i)
                    self.num_dice -= 1
        elif len(dice) == 3 or len(dice) == 2 or len(dice) == 1:
            for i in dice:
                if dice_count[i] == 3:
                    self.organize.append(i)
                    selected_dice.append(i)
                    self.num_dice -= 1
                elif i == 1 or i == 5 in dice_count:
                    self.kept_dice.append([i])
                    selected_dice.append(i)
                    self.num_dice -= 1
        self.organize.sort()

        if self.organize:
            self.kept_dice.append(self.organize[:])
        if self.sift:
            self.kept_dice.append(self.sift[:])

        self.organize.clear()
        self.sift.clear()
        print(f"{self.current_player} selected:")
        print(*selected_dice, sep=" ")
        if self.num_dice == 0:
            self.num_dice += 6
            Farkle.roll_dice(self)
        Farkle.comp_keep_rolling(self, Farkle.current_score(self))

    def comp_keep_rolling(self, score):
        chance = random.randint(1, 12)
        if (chance in self.comp_players[self.current_player]) and self.score_sheet[self.current_player] == 0:
            Farkle.current_score(self)
        elif chance in self.comp_players[self.current_player] and self.score_sheet[self.current_player] >= 450:
            print(f"{self.current_player} is stopping their turn.")
            remaining_dice = 6 - self.num_dice
            self.num_dice = self.num_dice + remaining_dice
            Farkle.update_score(self, Farkle.current_score(self))

    # def keep_dice(self):
    #     # if did_farkle == "roll":
    #     # this if statement looks at a state variable called did_farkle. If roll, carry on with the block below
    #     keep_dice = [str(input("What dice do you want to keep?\n")).split()]
    #
    #     #       Need to put in restrictions to numbers only, with spaces where necessary.
    #     #       Need restrictions on only being able to pick playable dice
    #     # splits dice into a list inside a list
    #     add_spaces = [[" ".join(j)] if len(j) > 1 else [j] for i in keep_dice for j in i]
    #     split_multiples = [sub.split() for subl in add_spaces for sub in subl]
    #     # if more than one dice in sublist, this splits them into separated elements inside sublist
    #     int_conversion = [[int(x) for x in lst] for lst in split_multiples]
    #     for dice in int_conversion:
    #         self.kept_dice.append(dice)
    #         #     add the dice kept to kept dice
    #         for _ in dice:
    #             self.num_dice -= 1
    #     #         as the dice are kept, the amount of dice being rolled is lowered
    #     if self.num_dice == 0:
    #         self.num_dice += 6
    #     #     if all dice are kept and none left to roll, a new round is started by adding six dice to roll
    #
    #     # keep_rolling = input("Do you want to keep rolling? (y,n)\n")
    #     # FIND NEW LOCATION
    #     pass


    def current_score(self):
        """Goes through all the kept dice and adds them to the score board. Also checks if score is at least 450
        before allowing player to stop rolling"""
        score = 0
        for i in self.kept_dice:
            if i in PLAYABLE_DICE:
                score += PLAYABLE_DICE[PLAYABLE_DICE.index(i) + 1]
            #     this goes through all the kept dice
            elif i not in PLAYABLE_DICE and len(i) == 6 and \
                    ((i.count(1) or i.count(2) or i.count(3) or i.count(4) or i.count(5) or i.count(6)) > 1):
                score += 500
        print(score, "current score")
        return score, Farkle.is_on_board(self, score)


    def is_on_board(self, score):
        print(score, "is on board")
        if (self.current_player == self.player or self.current_player != self.player)\
           and score < 450 and self.score_sheet[self.current_player] == 0:
            print("You are not on the board yet and need 450 to stop")
            Farkle.roll_dice(self)
        else:
            remaining_dice = 6 - self.num_dice
            self.num_dice = self.num_dice + remaining_dice
            Farkle.update_score(self, score)

    def update_score(self, score):
        print(score, "update score")
        self.score_sheet[self.current_player] = self.score_sheet[self.current_player] + score
        self.kept_dice.clear()
        # print(self.score_sheet)
        print(f"You scored {score} this turn\n")
        Farkle.winning_conditions(self)

    def farkled(self):
        remaining_dice = 6 - self.num_dice
        self.num_dice = self.num_dice + remaining_dice
        # print(self.kept_dice)
        print("You Farkled\n")
        self.kept_dice.clear()
        Farkle.next_player(self)
        # Solved - add the kept_dice conversion. use the list that you will copy from as the list
        #   that will decide how many times num_dice will be subtracted from

    def next_player(self):
        deck = deque(self.player_order)
        deck.rotate(-1)
        deck = list(deck)
        self.player_order.clear()
        for i in deck:
            self.player_order.append(i)
        self.current_player = self.player_order[0]
        if self.current_player == self.player:
            print("It is your turn")
        else:
            print(f"It is {self.current_player}'s turn")
        Farkle.roll_dice(self)

    def winning_conditions(self):
        # Find out how when one person breaks 10,000 points and another (or more) surpasses that player in one turn, to
        # Make a check, when first player breaks 10,000, if no other player beats that on their next turn, first player
        #   wins game. If other player(s) beat(s) first player, select all players that beat first and first player,
        #   remove all others from self.player_order and do that until no one can beat the current high score. Then,
        #   the current high score player wins.
        if self.score_sheet[self.current_player] >= 10000:
            self.score_sheet = {}
            self.num_dice = 6
            self.kept_dice = []
            self.organize = []
            self.sift = []
            self.comp_players = {}
            self.player_order = []
            self.score_sheet = {}
            self.whos_first = []
            if self.current_player == self.player:
                self.player = ""
                self.current_player = ""
                print(f"You win!! :) :)")
                time.sleep(1.13)
                Farkle.main(self)
            else:
                print(f"{self.current_player} wins! Sorry for the loss :(")
                self.player = ""
                self.current_player = ""
                time.sleep(1.13)
                Farkle.main(self)
        else:
            Farkle.next_player(self)


farkle = Farkle()
farkle.main()
# main
    # rules
    # main
# rules
    # opponents_difficulty
    # opponents_difficulty
# opponents_difficulty
    # choose_opponents
# choose_opponents
    # roll_for_first
# roll_for_first
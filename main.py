import tkinter as tk
from tkinter import *
from random import shuffle, sample
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import csv
from datetime import datetime


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.players = []
        self.pairings = []
        self.round = 1
        self.round_results = []
        self.pack()
        self.create_widgets()
        self.master.geometry('800x160')
        self.master.title('tournament')


        self.master.geometry('1200x700')
        self.master.configure(background='black')

    def create_widgets(self):

        # Add player button

        self.add_player_button = tk.Button(self, text="Add Player", command=self.add_player, width=40, bg='black', fg='black')
        self.add_player_button.grid(row=0, column=0, padx=20, pady=20) 
      #  self.add_player_button.place(relx=0.5, rely=0.25, anchor='center')

        # Add from list button
        self.add_from_list = tk.Button(self, text="Add from list", command=self.add_from_list, width=40)
        self.add_from_list.grid(row=1, column=0, padx=20, pady=20)

        # Show player list button
        self.show_players_button = tk.Button(self, text="Show Player List", command=self.show_player_list, width=40)
        self.show_players_button.grid(row=2, column=0, padx=20, pady=20)


        # Generate pairings button
        self.generate_pairings_button = tk.Button(self, text="Generate Pairings", command=self.generate_pairings, width=40)
        self.generate_pairings_button.grid(row=3, column=0, padx=20, pady=20)

        # Play game button        
        self.play_game_button = tk.Button(self, text="Who won?", command=self.play_game, width=40)
        self.play_game_button.grid(row=4, column=0, padx=20, pady=20)

        # Quit button
        self.quit_button = tk.Button(self, text="Quit", fg="red", command=self.master.destroy, width=40)
        self.quit_button.grid(row=5, column=0, padx=20, pady=20)

    def add_player(self):
        # Open a dialog box to get player name
        player_name = simpledialog.askstring("Add Player", "Enter player name:")
        if not player_name:
            messagebox.showerror("Error", "You did not type a name.")
            return

        # Check player name length
        if len(player_name) < 3 or len(player_name) > 10:
            messagebox.showerror("Error", "Invalid name type (3 - 10 characters)")
            return

        # Check if player name is already in CSV file
        try:
            with open('players.csv', mode='r') as file:
                reader = csv.reader(file)
                player_names = [row[0] for row in reader]
        except FileNotFoundError:
            # Create the players.csv file if it doesn't exist
            with open('players.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'Points'])
            player_names = []

        if player_name in player_names:
            messagebox.showerror("Error", "Player name already exists")
            return

        # Add player to list and CSV file
        self.players.append({"name": player_name, "points": 0})
        with open('players.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([player_name, 0])
        print(f"Added player {player_name} to CSV file")

    def add_from_list(self):
        # Read player names from CSV file

        try:
            with open('players.csv', mode='r') as file:
                reader = csv.reader(file)
                player_names = [row[0] for row in reader]
        except FileNotFoundError:
            messagebox.showinfo("Information", "Add first player to create list.")
            return

        with open('players.csv', mode='r') as file:
            reader = csv.reader(file)
            player_names = [row[0] for row in reader]

        # Create pop-up window with checkboxes to choose players
        top = tk.Toplevel(self)
        top.title("Choose Player")
        tk.Label(top, text="Select player(s):").pack()
        selected_players = []
        for player_name in player_names:
            var = tk.IntVar()
            chkbox = tk.Checkbutton(top, text=player_name, variable=var)
            chkbox.player_name = player_name
            chkbox.var = var
            chkbox.pack(anchor='w')

        # Add Accept button to pop-up window
        accept_button = tk.Button(top, text="Accept", command=lambda: self.add_selected_players(selected_players, top))
        accept_button.pack()

    def add_selected_players(self, selected_players, top):
        for chkbox in top.winfo_children():
            if isinstance(chkbox, tk.Checkbutton) and chkbox.var.get() == 1:
                player_name = chkbox.player_name
                # Check if player is already in the list
                if any(player["name"] == player_name for player in self.players):
                    messagebox.showwarning("Warning", f"{player_name} is already in the list.")
                else:
                    selected_players.append(player_name)
                    self.players.append({"name": player_name, "points": 0})
                    print(f"Added player {player_name}")
        top.destroy()

    def show_player_list(self):
        # Sort players based on their points in descending order
        sorted_players = sorted(self.players, key=lambda player: player['points'], reverse=True)

        # Construct the player list string with the sorted players
        player_list = "\n".join(
            [f"{i + 1}. {player['name']} ({player['points']} points)" for i, player in enumerate(sorted_players)])

        # Open a dialog box to show player list
        tk.messagebox.showinfo("Player Ranking", player_list)

    def generate_pairings(self):
        if len(self.players) < 3:
            tk.messagebox.showerror("Error", "At least 3 players are required to generate pairings.")
        else:
            # Shuffle player list
            shuffle(self.players)

            # Create pairings
            self.pairings = []
            num_players = len(self.players)
            for i in range(0, num_players, 2):
                if i + 1 == num_players:
                    # Odd number of players, so the last player gets a bye
                    self.players[i]["points"] += 1
                    self.pairings.append((self.players[i], None))
                else:
                    self.pairings.append((self.players[i], self.players[i + 1]))

            # Show pairings in a dialog box
            pairings_list = "\n".join(
                [f"{i + 1}. {pairing[0]['name']} vs. {pairing[1]['name'] if pairing[1] else 'BYE'}" for i, pairing in
                 enumerate(self.pairings)])
            tk.messagebox.showinfo(f"Round {self.round} Pairings", pairings_list)
            self.generate_pairings_button.config(state='disabled')
            # Increment round
            # self.round += 1

    def play_game(self):
        # Check if there are any pairings to play
        if not self.pairings:
            messagebox.showerror("Error", "No pairings to play")
            return

        # Create a new window for playing the game
        game_window = tk.Toplevel(self)

        # Left Frame for pairs and Radiobuttons
        left_frame = tk.Frame(game_window)
        left_frame.pack(side='left')

        # Right Frame for Accept button
        right_frame = tk.Frame(game_window)
        right_frame.pack(side='right')

        # Create variables to store winner choices
        winners = [tk.StringVar() for _ in range(len(self.pairings))]

        # Show all pairs and create radio buttons to select the winner for each pair
        for i, pairing in enumerate(self.pairings):
            # Create a label for the pair
            if pairing[1] is None:
                pair_label = tk.Label(left_frame, text=f"{pairing[0]['name']} has bye")
            else:
                pair_label = tk.Label(left_frame, text=f"{pairing[0]['name']} vs {pairing[1]['name']}")
            pair_label.pack()

            # Create radio buttons for each player
            player1_button = tk.Radiobutton(left_frame, text=pairing[0]['name'], variable=winners[i],
                                            value=pairing[0]['name'])
            player1_button.pack(anchor='w')
            if pairing[1] is not None:
                player2_button = tk.Radiobutton(left_frame, text=pairing[1]['name'], variable=winners[i],
                                                value=pairing[1]['name'])
                player2_button.pack(anchor='w')
            else:
                # If one player has bye, disable the radio button
                player1_button.config(state='disabled')

        # Create an "Accept" button to save the results and proceed to the next round
        accept_button = tk.Button(right_frame, text="Accept", command=lambda: self.accept_results(winners, game_window))
        accept_button.pack()
        self.generate_pairings_button.config(state='normal')

    def accept_results(self, winners, game_window):
        # Check if all pairs have been played
        if len(winners) != len(self.pairings):
            messagebox.showerror("Error", "Not all pairs have been played")
            return

        # Update the points for the winners and add the results to the round results
        for i, pairing in enumerate(self.pairings):
            winner_name = winners[i].get()
            for player in self.players:
                if player['name'] == winner_name:
                    player['points'] += 1
                    self.round_results.append({'pairing': pairing, 'winner': player})
                    break

        # Clear the pairings for the next round
        self.pairings = []

        # Show the round results
        round_results_str = "\n".join(
            [f"{result['pairing'][0]['name']} vs {result['pairing'][1]['name']}: {result['winner']['name']} wins" if
             result['winner'] is not None else f"{result['pairing'][0]['name']}: BYE" for
             result in self.round_results])
        messagebox.showinfo(f"Round {self.round} Results", round_results_str)

        # Write the round results to the CSV file
        with open('results.csv', mode='a', newline='') as file:
            writer = csv.writer(file)

            if file.tell() == 0:  # Check if the file is empty
                headers = ['index', 'round', 'matched players', 'winner', 'date', 'hour', 'minute']
                writer.writerow(headers)

            current_index = 1  # Start index from 1

            for result in self.round_results:
                pairing = result['pairing']
                winner = result['winner']
                current_time = datetime.now()

                if pairing[1] is None:  # Check if a player received a bye
                    bye_row = [
                        current_index,
                        self.round,
                        pairing[0]['name'],
                        'BYE',
                        current_time.strftime("%Y-%m-%d"),
                        current_time.strftime("%H"),
                        current_time.strftime("%M")
                    ]
                    writer.writerow(bye_row)
                else:
                    row = [
                        current_index,
                        self.round,
                        f"{pairing[0]['name']} vs {pairing[1]['name']}",
                        winner['name'] if winner is not None else 'BYE',
                        current_time.strftime("%Y-%m-%d"),
                        current_time.strftime("%H"),
                        current_time.strftime("%M")
                    ]
                    writer.writerow(row)

                current_index += 1  # Increment the index for the next row

        # Increment the round number and reset the round results
        self.round += 1
        self.round_results = []

        # Close the game window
        game_window.destroy()

    def export_results_to_csv(self):
        # Open the results.csv file in append mode
        with open('results.csv', mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write the header if the file is empty
            if file.tell() == 0:
                writer.writerow(['Round', 'Player 1', 'Player 2', 'Winner'])

            # Write the results for each pairing in the round
            for result in self.round_results:
                player1 = result['pairing'][0]['name']
                player2 = result['pairing'][1]['name'] if result['pairing'][1] else 'BYE'
                winner = result['winner']['name']
                writer.writerow([self.round, player1, player2, winner])

    def add_players_from_file(self):
        # Read players from file
        try:
            with open("players.csv", "r") as f:
                existing_players = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            existing_players = []

        # Create pop-up window with checkboxes for each player
        window = tk.Toplevel(self)
        window.title("Add Players")
        tk.Label(window, text="Select players to add:").grid(row=0, column=0, sticky="w")
        checkboxes = []
        for i, player in enumerate(existing_players):
            var = tk.BooleanVar()
            checkboxes.append(var)
            tk.Checkbutton(window, text=player, variable=var).grid(row=i+1, column=0, sticky="w")

    def generate_next_round(self):
        # Reset round results
        self.round_results = []

        # Check if the tournament is over
        if self.round > self.num_rounds:
            # Show final standings in a dialog box
            standings_list = "\n".join(
                [f"{i + 1}. {player['name']} ({player['points']} points)" for i, player in enumerate(self.players)])
            tk.messagebox.showinfo("Final Standings", standings_list)

            # Disable buttons
            self.add_player_button.config(state="disabled")
            self.show_players_button.config(state="disabled")
            self.generate_pairings_button.config(state="disabled")

            # Show a message that the tournament is over
            messagebox.showinfo("Tournament Over", "The tournament is over!")
            return

        # Shuffle players with the same number of points
        points_dict = {}
        for player in self.players:
            points = player['points']
            if points not in points_dict:
                points_dict[points] = []
            points_dict[points].append(player)
        players_list = []
        for points in sorted(points_dict.keys(), reverse=True):
            shuffle(points_dict[points])
            players_list.extend(points_dict[points])

        # Create pairings
        self.pairings = []
        num_players = len(players_list)
        for i in range(0, num_players, 2):
            if i + 1 == num_players:
                # Odd number of players, so the last player gets a bye
                players_list[i]["points"] += 1
                self.pairings.append((players_list[i], None))
            else:
                self.pairings.append((players_list[i], players_list[i + 1]))

        # Show pairings in a dialog box
        pairings_list = "\n".join(
            [f"{i + 1}. {pairing[0]['name']} vs. {pairing[1]['name'] if pairing[1] else 'BYE'}" for i, pairing in
             enumerate(self.pairings)])
        tk.messagebox.showinfo(f"Round {self.round} Pairings", pairings_list)

        # Increment round
        self.round += 1


root = tk.Tk()
app = Application(master=root)
app.mainloop()

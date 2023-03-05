import tkinter as tk
from random import shuffle, sample
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import csv


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

    def create_widgets(self):
        # Add player button

        self.add_player_button = tk.Button(self, text="Add Player", command=self.add_player)
        self.add_player_button.pack(side="top")

        # Add from list button
        self.add_from_list = tk.Button(self, text="Add from list", command=self.add_from_list)
        self.add_from_list.pack(side="top")

        # Show player list button
        self.show_players_button = tk.Button(self, text="Show Player List", command=self.show_player_list)
        self.show_players_button.pack(side="top")


        # Generate pairings button
        self.generate_pairings_button = tk.Button(self, text="Generate Pairings", command=self.generate_pairings)
        self.generate_pairings_button.pack(side="top")

        # Play game button
        self.play_game_button = tk.Button(self, text="Play Game", command=self.play_game)
        self.play_game_button.pack(side="top")

        # Quit button
        self.quit_button = tk.Button(self, text="Quit", fg="red", command=self.master.destroy)
        self.quit_button.pack(side="bottom")



    def add_from_list (self):
        # Read player names from CSV file
        with open('players.csv', mode='r') as file:
            reader = csv.reader(file)
            player_names = [row[0] for row in reader]

        # Create pop-up window with checkboxes to choose players
        top = tk.Toplevel(self)
        top.title("Choose Player")
        tk.Label(top, text="Select a player:").pack()
        selected_player = tk.StringVar()
        for player_name in player_names:
            tk.Radiobutton(top, text=player_name, variable=selected_player, value=player_name).pack(anchor='w')

            # Add player button
        def add_selected_player():
            player_name = selected_player.get()
            if player_name:
                # Add player to list
                self.players.append({"name": player_name, "points": 0})
                print(f"Added player {player_name}")



    # def add_player(self):
    #     # Load existing players from players.csv
    #     existing_players = []
    #     with open('players.csv', mode='r') as file:
    #         reader = csv.reader(file)
    #         for row in reader:
    #             existing_players.append(row[0])
    #
    #     # Open a dialog box to get player name or choose from existing players
    #     dialog = tk.Toplevel()
    #     dialog.title("Add Player")
    #
    #     dialog_label = tk.Label(dialog, text="Enter player name or choose from existing players:")
    #     dialog_label.grid(row=0, column=0, padx=10, pady=10)
    #
    #     player_name_var = tk.StringVar()
    #     player_name_entry = tk.Entry(dialog, textvariable=player_name_var)
    #     player_name_entry.grid(row=1, column=0, padx=10)
    #
    #     existing_players_var = tk.StringVar(value=existing_players)
    #     existing_players_cb = tk.OptionMenu(dialog, player_name_var, *existing_players_var.get())
    #     existing_players_cb.grid(row=2, column=0, padx=10, pady=10)
    #
    #     def add_player_callback():
    #         player_name = player_name_var.get().strip()
    #         if player_name:
    #             # Add player to list and CSV file
    #             self.players.append({"name": player_name, "points": 0})
    #             with open('players.csv', mode='a', newline='') as file:
    #                 writer = csv.writer(file)
    #                 writer.writerow([player_name, 0])
    #             print(f"Added player {player_name} to CSV file")
    #
    #         dialog.destroy()
    #
    #     add_button = tk.Button(dialog, text="Add", command=add_player_callback)
    #     add_button.grid(row=3, column=0, padx=10, pady=10)

    def add_player(self):
        # Open a dialog box to get player name
        player_name = simpledialog.askstring("Add Player", "Enter player name:")
        if player_name:
            # Check if player name is already in CSV file
            with open('players.csv', mode='r') as file:
                reader = csv.reader(file)
                player_names = [row[0] for row in reader]
                if player_name in player_names:
                    messagebox.showerror("Error", "Player name already exists")
                    return

            # Add player to list and CSV file
            self.players.append({"name": player_name, "points": 0})
            with open('players.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([player_name, 0])
            print(f"Added player {player_name} to CSV file")



    def show_player_list(self):
        # Sort players based on their points in descending order
        sorted_players = sorted(self.players, key=lambda player: player['points'], reverse=True)

        # Construct the player list string with the sorted players
        player_list = "\n".join(
            [f"{i + 1}. {player['name']} ({player['points']} points)" for i, player in enumerate(sorted_players)])

        # Open a dialog box to show player list
        tk.messagebox.showinfo("Player Ranking", player_list)


    def generate_pairings(self):
        # Shuffle player list
        shuffle(self.players)

        # Create pairings
        self.pairings = []
        num_players = len(self.players)
        for i in range(0, num_players, 2):
            if i+1 == num_players:
                # Odd number of players, so the last player gets a bye
                self.players[i]["points"] += 1
                self.pairings.append((self.players[i], None))
            else:
                self.pairings.append((self.players[i], self.players[i+1]))

        # Show pairings in a dialog box
        pairings_list = "\n".join([f"{i+1}. {pairing[0]['name']} vs. {pairing[1]['name'] if pairing[1] else 'BYE'}" for i, pairing in enumerate(self.pairings)])
        tk.messagebox.showinfo(f"Round {self.round} Pairings", pairings_list)

        # Increment round
        self.round += 1

    def play_game(self):
        # Loop through each pairing in self.pairings and prompt user for the winner
        self.round_results = []
        for pairing in self.pairings:
            player1 = pairing[0]
            player2 = pairing[1]

            if player2 is None:
                # Player 1 gets a bye
                winner = player1
                loser = None
            else:
                # Prompt user for winner
                winner_name = tk.simpledialog.askstring("Game Result",
                                                        f"Who won the game? {player1['name']} vs {player2['name']}")
                if winner_name:
                    if winner_name == player1['name']:
                        winner = player1
                        loser = player2
                    elif winner_name == player2['name']:
                        winner = player2
                        loser = player1
                    else:
                        messagebox.showerror("Error", "Invalid winner name")
                        return

            # Update points and show game result
            if loser is not None:
                winner['points'] += 1
                messagebox.showinfo("Game Result", f"{winner['name']} won the game!")
                self.round_results.append((winner['name'], loser['name'], 1))
            else:
                messagebox.showinfo("Game Result", f"{winner['name']} gets a bye!")

        # If all players have played, generate next round
        if len(self.round_results) == len(self.players) / 2:
            self.generate_pairings()

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




root = tk.Tk()
app = Application(master=root)
app.mainloop()

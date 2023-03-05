import tkinter as tk
from random import shuffle, sample
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox


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

    def add_player(self):
        # Open a dialog box to get player name
        player_name = simpledialog.askstring("Add Player", "Enter player name:")
        if player_name:
            self.players.append({"name": player_name, "points": 0})
            print(f"Added player {player_name}")

    def show_player_list(self):
        # Open a dialog box to show player list
        player_list = "\n".join([f"{i+1}. {player['name']} ({player['points']} points)" for i, player in enumerate(self.players)])
        tk.messagebox.showinfo("Player List", player_list)

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
        self.generate_pairings_button.config(state='disabled')
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
        self.generate_pairings_button.config(state='normal')

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

import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from random import shuffle, sample
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import csv
from datetime import datetime
import os


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.players = []
        self.pairings = []
        self.round = 1
        self.round_results = []
        self.pairing_history = []  # Maintain a history of player pairings for each round
        self.create_widgets()
        self.master.title('Tournament')
        self.master.geometry('1366x568')

        background_color = "black"
        self.master.configure(background=background_color)

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_columnconfigure(3, weight=1)

        # Dodawanie pustego wiersza na górze i dole okna
        empty_label1 = tk.Label(root)
        empty_label1.grid(row=0, column=0)
        empty_label2 = tk.Label(root)
        empty_label2.grid(row=5, column=0)

        # Ustawianie wagi dla wierszy
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=2)
        root.grid_rowconfigure(2, weight=2)
        root.grid_rowconfigure(3, weight=2)
        root.grid_rowconfigure(4, weight=2)
        root.grid_rowconfigure(5, weight=2)
        root.grid_rowconfigure(6, weight=1)

        # Wczytanie obrazka lewa strona
        file_path1 = "./wojownik_1.png"
        image1 = Image.open(file_path1)
        image1 = image1.resize((300, 320), Image.LANCZOS)  # Dostosowanie rozmiaru obrazka
        photo1 = ImageTk.PhotoImage(image1)

        # Tworzenie etykiety z obrazkiem i ustawienie pozycji
        self.label = Label(self.master, image=photo1)
        self.label.image = photo1
        self.label.grid(row=1, column=0, rowspan=4, padx=50, pady=20)

        # Wczytanie obrazka prawa strona
        file_path2 = "./wojownik_2.png"
        image2 = Image.open(file_path2)
        image2 = image2.resize((300, 320), Image.LANCZOS)  # Dostosowanie rozmiaru obrazka
        photo2 = ImageTk.PhotoImage(image2)

        # Tworzenie etykiety z obrazkiem i ustawienie pozycji
        self.label = Label(self.master, image=photo2)
        self.label.image = photo2
        self.label.grid(row=1, column=3, rowspan=4, padx=50, pady=20)

    def create_widgets(self):
        background_color = 'black'
        highlight_thickness = 5
        button_width = 25
        button_height = 3
        font_style = 'Arial'
        font_size = 18
        font_weight = 'bold'
        font_color1 = '#484a49'
        font_color2 = '#211a87'

        # Add player button
        self.add_player_button = tk.Button(self.master,  text="ADD NEW PLAYER", command=self.add_player,
                                           foreground=font_color2,
                                           highlightbackground=background_color,
                                           highlightcolor=background_color,
                                           highlightthickness=highlight_thickness,
                                           height=button_height,
                                           width=button_width,
                                           borderwidth=0,
                                           relief="flat",
                                           font=(font_style, font_size, font_weight))
        self.add_player_button.grid(row=1, column=1, padx=0, pady=0)

        # Add from list button
        self.add_from_list = tk.Button(self.master, text="ADD PLAYER FROM LIST", command=self.add_from_list,
                                       foreground=font_color2,
                                       highlightbackground=background_color,
                                       highlightcolor=background_color,
                                       highlightthickness=highlight_thickness,
                                       height=button_height,
                                       width=button_width,
                                       borderwidth=0,
                                       relief="flat",
                                       font=(font_style, font_size, font_weight))
        self.add_from_list.grid(row=2, column=1, padx=0, pady=0)

        # Show player list button
        self.show_players_button = tk.Button(self.master, text="SHOW PLAYERS LIST", command=self.show_player_list,
                                             foreground=font_color2,
                                             highlightbackground=background_color,
                                             highlightcolor=background_color,
                                             highlightthickness=highlight_thickness,
                                             height=button_height,
                                             width=button_width,
                                             borderwidth=0,
                                             relief="flat",
                                             font=(font_style, font_size, font_weight))
        self.show_players_button.grid(row=3, column=1, padx=0, pady=0)

        # temp button
        self.temp_button = tk.Button(self.master, text="TEMP", command=self.delete_csv_content,
                                     foreground='red',
                                     highlightbackground=background_color,
                                     highlightcolor=background_color,
                                     highlightthickness=highlight_thickness,
                                     height=button_height,
                                     width=button_width,
                                     borderwidth=0,
                                     relief="flat",
                                     font=(font_style, font_size, font_weight))
        self.temp_button.grid(row=4, column=1, padx=0, pady=0)

        # Generate pairings button
        self.generate_pairings_button = tk.Button(self.master, text="GENERATE PAIRINGS", command=self.generate_pairings,
                                                  foreground=font_color1,
                                                  highlightbackground=background_color,
                                                  highlightcolor=background_color,
                                                  highlightthickness=highlight_thickness,
                                                  height=button_height,
                                                  width=button_width,
                                                  borderwidth=0,
                                                  relief="flat",
                                                  font=(font_style, font_size, font_weight))
        self.generate_pairings_button.grid(row=2, column=2, padx=0, pady=0)

        # Play game button        
        self.play_game_button = tk.Button(self.master, text="ADD RESULTS", command=self.play_game,
                                          foreground=font_color1,
                                          highlightbackground=background_color,
                                          highlightcolor=background_color,
                                          highlightthickness=highlight_thickness,
                                          height=button_height,
                                          width=button_width,
                                          borderwidth=0,
                                          relief="flat",
                                          font=(font_style, font_size, font_weight))
        self.play_game_button.grid(row=3, column=2, padx=0, pady=0)

        # Show player list button with results
        self.show_players_button_results = tk.Button(self.master, text="SHOW CURRENT RESULTS", command=self.show_player_list,
                                             foreground=font_color1,
                                             highlightbackground=background_color,
                                             highlightcolor=background_color,
                                             highlightthickness=highlight_thickness,
                                             height=button_height,
                                             width=button_width,
                                             borderwidth=0,
                                             relief="flat",
                                             font=(font_style, font_size, font_weight))
        self.show_players_button_results.grid(row=4, column=2, padx=0, pady=0)

        # Quit button
        self.quit_button = tk.Button(self.master, text="QUIT", command=self.master.destroy,
                                     foreground='red',
                                     highlightbackground=background_color,
                                     highlightcolor=background_color,
                                     highlightthickness=highlight_thickness,
                                     height=button_height,
                                     width=button_width,
                                     borderwidth=0,
                                     relief="flat",
                                     font=(font_style, font_size, font_weight))
        self.quit_button.grid(row=5, column=2, padx=0, pady=0)


    def add_player(self):
        # Open a dialog box to get player name
        player_name = simpledialog.askstring("Add Player", "Enter player name:")
        if not player_name:
            messagebox.showerror("Error", "You did not type a name.")
            root.deiconify()
            return

        # Check player name length
        if len(player_name) < 3 or len(player_name) > 10:
            messagebox.showerror("Error", "Invalid name type (3 - 10 characters)")
            root.deiconify()
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
            root.deiconify()
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
            root.deiconify()
            return

        with open('players.csv', mode='r') as file:
            reader = csv.reader(file)
            player_names = [row[0] for row in reader]

        # Exclude the header row from the player names
        player_names = player_names[1:]

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
        if len(self.players) == 0:
            tk.messagebox.showerror("Error", "No players have been added.")
            root.deiconify()
        else:
            # Sort players based on their points in descending order
            sorted_players = sorted(self.players, key=lambda player: player['points'], reverse=True)

            # Construct the player list string with the sorted players
            player_list = "\n".join(
                [f"{i + 1}. {player['name']} ({player['points']} points)" for i, player in enumerate(sorted_players)])

            # Open a dialog box to show player list
            tk.messagebox.showinfo("Player Ranking", player_list)
            root.deiconify()

    def generate_pairings(self):
        if len(self.players) < 3:
            tk.messagebox.showerror("Error", "At least 3 players are required to generate pairings.")
            root.deiconify()
        else:
            # Shuffle player list
            shuffle(self.players)

            # Create pairings
            self.pairings = []
            num_players = len(self.players)
            used_players = []
            for i in range(0, num_players, 2):
                if i + 1 == num_players:
                    # Odd number of players, so the last player gets a bye
                    self.players[i]["points"] += 1
                    self.pairings.append((self.players[i], None))
                    used_players.append(self.players[i])
                else:
                    # Find the first available pairing
                    pairing_found = False
                    for j in range(i + 1, num_players):
                        if self.players[i] not in used_players and self.players[j] not in used_players:
                            self.pairings.append((self.players[i], self.players[j]))
                            used_players.extend([self.players[i], self.players[j]])
                            pairing_found = True
                            break

                    # If no available pairing is found, display an error message
                    if not pairing_found:
                        tk.messagebox.showerror("Error", "Unable to create pairings without repetitions.")
                        return

            # Show pairings in a dialog box
            pairings_list = "\n".join(
                [f"{i + 1}. {pairing[0]['name']} vs. {pairing[1]['name'] if pairing[1] else 'BYE'}" for i, pairing in
                 enumerate(self.pairings)])
            tk.messagebox.showinfo(f"Round {self.round} Pairings", pairings_list)
            self.generate_pairings_button.config(state='disabled')
            root.deiconify()
            # Increment round

    def play_game(self):
        # Check if there are any pairings to play
        if not self.pairings:
            messagebox.showerror("Error", "No pairings to play")
            root.deiconify()
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
        accept_button.grid(row=0, column=0)
        self.generate_pairings_button.config(state='normal')

        def check_selected_players():
            for winner in winners:
                if winner.get():
                    accept_button.config(state='normal')
                    return
            accept_button.config(state='disabled')

        # Call the check_selected_players function whenever a radio button is clicked
        for i in range(len(winners)):
            winners[i].trace('w', lambda *args, i=i: check_selected_players())

        # Initially disable the "Accept" button
        accept_button.config(state='disabled')

        self.add_player_button.config(state='disabled')
        self.add_from_list.config(state='disabled')

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
        root.deiconify()

    def export_results_to_csv(self):
        # Write the results to the CSV file
        with open('results.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            headers = ['Round', 'Matched Player 1', 'Matched Player 2', 'Winner']
            writer.writerow(headers)

            for result in self.results:
                pairing = result['pairing']
                winner = result['winner']

                if pairing[1] is None:  # Check if a player received a bye
                    bye_row = [
                        result['round'],
                        pairing[0]['name'],
                        'BYE',
                        'BYE'
                    ]
                    writer.writerow(bye_row)
                else:
                    row = [
                        result['round'],
                        pairing[0]['name'],
                        pairing[1]['name'],
                        winner['name'] if winner is not None else 'BYE'
                    ]
                    writer.writerow(row)

        messagebox.showinfo("Export Complete", "Results exported to results.csv")

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

    def delete_csv_content(self):
        try:
            os.remove("players.csv")
            messagebox.showinfo("Removal done.", "CSV file has been deleted.")
            root.deiconify()
        except FileNotFoundError:
            messagebox.showerror("File not found", "There is no CSV file")
            root.deiconify()
        except PermissionError:
            messagebox.showerror("Permission denied.")
            root.deiconify()

    # Example usage
    # delete_csv_content('path/to/your/file.csv')


root = tk.Tk()
app = Application(master=root)
app.mainloop()

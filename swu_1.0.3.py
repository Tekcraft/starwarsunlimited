#!/usr/bin/env python3

import json
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget, QScrollArea

__version__ = "1.0.3"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(600, 150)  # Adjusted minimum width
        self.setWindowTitle("Import Deck or Booster Pack v{}".format(__version__))

        # Create a central widget and layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)

        # Add the central widget to a scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.central_widget)
        self.setCentralWidget(self.scroll_area)

        # Add a label for instructions
        self.label = QLabel("Do you want to import a deck or a booster pack?")
        self.layout.addWidget(self.label)

        # Add buttons for importing
        self.deck_button = QPushButton('Deck')
        self.deck_button.clicked.connect(self.import_deck)
        self.layout.addWidget(self.deck_button)

        self.booster_button = QPushButton('Booster Pack')
        self.booster_button.clicked.connect(self.import_booster_pack)
        self.layout.addWidget(self.booster_button)

        # Add a label for displaying save status
        self.save_label = QLabel("")
        self.layout.addWidget(self.save_label)

    def import_deck(self):
        json_path, _ = QFileDialog.getOpenFileName(self, "Select JSON file", "", "JSON files (*.json)")
        if not json_path:
            print("No file selected. Exiting.")
            return

        self.process_cards(json_path, 1)

    def import_booster_pack(self):
        json_path, _ = QFileDialog.getOpenFileName(self, "Select JSON file", "", "JSON files (*.json)")
        if not json_path:
            print("No file selected. Exiting.")
            return

        self.process_cards(json_path, 2)

    def process_cards(self, json_path, choice):
        card_data = {}

        with open(json_path, 'r') as file:
            data = json.load(file)

        if choice == 1:  # Import deck
            for card in data.get('deck', []):
                card_id = card.get('id', '')
                count = card.get('count', 0)
                is_foil = "*Foil" in card_id
                card_key = (card_id.split('_')[0], card_id.split('_')[1], is_foil)

                if card_key in card_data:
                    card_data[card_key] += count
                else:
                    card_data[card_key] = count

        elif choice == 2:  # Import booster pack
            for obj in data['ObjectStates']:
                if 'CardCustom' in obj['Name']:
                    gm_notes = obj['GMNotes']
                    if '_' in gm_notes:
                        set_code, card_number = gm_notes.split('_')
                    else:
                        set_code = 'Unknown'
                        card_number = '000'

                    card_name = obj['Nickname']
                    is_foil = 'TRUE' if '*Foil' in card_name else 'FALSE'
                    card_key = (set_code, card_number, is_foil)

                    if card_key in card_data:
                        card_data[card_key] += 1
                    else:
                        card_data[card_key] = 1

        save_path, _ = QFileDialog.getSaveFileName(self, "Save CSV file", "", "CSV files (*.csv)")
        if not save_path:
            print("No save location selected. Exiting.")
            return

        csv_data = [('Set', 'CardNumber', 'Count', 'IsFoil')]
        for (set_code, card_number, is_foil), count in card_data.items():
            csv_data.append((set_code, card_number, count, is_foil))

        with open(save_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(csv_data)

        # Update the save status label
        self.save_label.setText(f"CSV file saved successfully at: {save_path}")

# Create an application
app = QApplication([])

# Create an instance of MainWindow and show the main window
main_win = MainWindow()
main_win.show()

# Run the application
app.exec_()


import json
import csv
from PyQt5.QtWidgets import QApplication, QFileDialog

def process_cards_to_csv():
    choice = input("Do you want to import a deck (1) or a booster pack (2) [1|2]: ")

    if choice == '1':
        # Load the JSON data from the uploaded file
        app = QApplication([])
        json_path, _ = QFileDialog.getOpenFileName(None, "Select JSON file", "", "JSON files (*.json)")
        if not json_path:
            print("No file selected. Exiting.")
            exit()

        # Dictionary to hold card data with counts and foil status
        card_data = {}

        # Extract card details from the JSON data
        with open(json_path, 'r') as file:
            data = json.load(file)

        for card in data.get('deck', []):
            card_id = card.get('id', '')
            count = card.get('count', 0)
            is_foil = "*Foil" in card_id
            card_key = (card_id.split('_')[0], card_id.split('_')[1], is_foil)

            if card_key in card_data:
                card_data[card_key] += count
            else:
                card_data[card_key] = count

        # Ask user where to save the CSV file
        save_path, _ = QFileDialog.getSaveFileName(None, "Save CSV file", "", "CSV files (*.csv)")
        if not save_path:
            print("No save location selected. Exiting.")
            exit()

        # Create CSV data with headers
        csv_data = [('Set', 'CardNumber', 'Count', 'IsFoil')]
        for (set_code, card_number, is_foil), count in card_data.items():
            csv_data.append((set_code, card_number, count, is_foil))

        # Write data to a CSV file
        with open(save_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(csv_data)

        print("CSV file saved successfully at:", save_path)

    elif choice == '2':
        # Load the JSON data from the uploaded file
        app = QApplication([])
        json_path, _ = QFileDialog.getOpenFileName(None, "Select JSON file", "", "JSON files (*.json)")
        if not json_path:
            print("No file selected. Exiting.")
            exit()

        # Dictionary to hold card data with counts and foil status
        card_data = {}

        # Extract card details from the JSON data
        with open(json_path, 'r') as file:
            data = json.load(file)

        for obj in data['ObjectStates']:
            if 'CardCustom' in obj['Name']:
                gm_notes = obj['GMNotes']
                if '_' in gm_notes:
                    set_code, card_number = gm_notes.split('_')
                else:
                    set_code = 'Unknown'  # Default value if format is unexpected
                    card_number = '000'   # Default value if format is unexpected

                card_name = obj['Nickname']
                is_foil = 'TRUE' if '*Foil' in card_name else 'FALSE'
                card_key = (set_code, card_number, is_foil)

                if card_key in card_data:
                    card_data[card_key] += 1
                else:
                    card_data[card_key] = 1

        # Ask user where to save the CSV file
        save_path, _ = QFileDialog.getSaveFileName(None, "Save CSV file", "", "CSV files (*.csv)")
        if not save_path:
            print("No save location selected. Exiting.")
            exit()

        # Create CSV data with headers
        csv_data = [('Set', 'CardNumber', 'Count', 'IsFoil')]
        for (set_code, card_number, is_foil), count in card_data.items():
            csv_data.append((set_code, card_number, count, is_foil))

        # Write data to a CSV file
        with open(save_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(csv_data)

        print("CSV file saved successfully at:", save_path)

    else:
        print("Invalid choice. Exiting.")
        exit()

# Example usage of the function
process_cards_to_csv()


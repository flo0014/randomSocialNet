
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QHBoxLayout, QDialog, QDialogButtonBox
import sqlite3

class KeywordManagementTab(QWidget):
    def __init__(self):
        super(KeywordManagementTab, self).__init__()
        self.initUI()
        self.load_mot_cles_from_db()

    def initUI(self):
        # Create a QVBoxLayout for the tab layout
        mot_cle_layout = QVBoxLayout()

        # Create QLineEdit for mot_cle input and a QPushButton for validation
        input_layout = QHBoxLayout()
        self.mot_cle_input = QLineEdit()
        self.validate_button = QPushButton("Valider")
        input_layout.addWidget(self.mot_cle_input)
        input_layout.addWidget(self.validate_button)

        # Create QListWidget for displaying validated mot_cles
        self.mot_cle_list = QListWidget()

        # Create buttons for editing and deleting mot_cles
        self.edit_button = QPushButton("Modifier")
        self.delete_button = QPushButton("Supprimer")

        # Connect the buttons' clicked signals to custom slots
        self.validate_button.clicked.connect(self.add_mot_cle_to_list)
        self.edit_button.clicked.connect(self.edit_selected_mot_cle)
        self.delete_button.clicked.connect(self.delete_selected_mot_cle)

        # Add widgets to layout
        mot_cle_layout.addLayout(input_layout)
        mot_cle_layout.addWidget(self.mot_cle_list)
        mot_cle_layout.addWidget(self.edit_button)
        mot_cle_layout.addWidget(self.delete_button)

        self.setLayout(mot_cle_layout)

    def add_mot_cle_to_list(self):
        # Get the text from mot_cle_input
        mot_cle = self.mot_cle_input.text()

        # Add the text to mot_cle_list
        self.mot_cle_list.addItem(mot_cle)

        # Clear the mot_cle_input
        self.mot_cle_input.clear()

        # Store the mot_cle in the database
        self.store_mot_cle_in_db(mot_cle)

    def edit_selected_mot_cle(self):
        # Get the selected mot_cle from the list
        selected_items = self.mot_cle_list.selectedItems()

        if selected_items:
            old_mot_cle = selected_items[0].text()

            # Open a QDialog to get the new mot_cle
            new_mot_cle, ok = self.show_edit_dialog(old_mot_cle)

            if ok:
                # Update the mot_cle in the list and database
                selected_items[0].setText(new_mot_cle)
                self.update_mot_cle_in_db(old_mot_cle, new_mot_cle)

    def delete_selected_mot_cle(self):
        # Get the selected mot_cle from the list
        selected_items = self.mot_cle_list.selectedItems()

        if selected_items:
            mot_cle_to_delete = selected_items[0].text()
            
            # Remove the mot_cle from the list
            self.mot_cle_list.takeItem(self.mot_cle_list.row(selected_items[0]))

            # Delete the mot_cle from the database
            self.delete_mot_cle_from_db(mot_cle_to_delete)

    def show_edit_dialog(self, old_mot_cle):
        dialog = QDialog()
        dialog.setWindowTitle("Modifier le mot-clé")
        dialog_layout = QVBoxLayout()
        input_edit = QLineEdit(old_mot_cle)
        dialog_layout.addWidget(input_edit)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dialog_layout.addWidget(button_box)
        dialog.setLayout(dialog_layout)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        ok = dialog.exec_()
        return input_edit.text(), ok == QDialog.Accepted

    def store_mot_cle_in_db(self, mot_cle):
        conn = sqlite3.connect('../database/app_data.db')
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO MotsCles (mot_cle) VALUES (?)", (mot_cle,))
            conn.commit()
        except sqlite3.IntegrityError:
            # Handle duplicate mot_cles if necessary
            pass

        conn.close()

    def update_mot_cle_in_db(self, old_mot_cle, new_mot_cle):
        conn = sqlite3.connect('../database/app_data.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE MotsCles SET mot_cle = ? WHERE mot_cle = ?", (new_mot_cle, old_mot_cle))
        conn.commit()

        conn.close()

    def delete_mot_cle_from_db(self, mot_cle):
        conn = sqlite3.connect('../database/app_data.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM MotsCles WHERE mot_cle = ?", (mot_cle,))
        conn.commit()

        conn.close()

    def load_mot_cles_from_db(self):
        conn = sqlite3.connect('../database/app_data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT mot_cle FROM MotsCles")
        mot_cles = cursor.fetchall()

        for mot_cle in mot_cles:
            self.mot_cle_list.addItem(mot_cle[0])

        conn.close()

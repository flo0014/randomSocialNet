
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QHBoxLayout, QDialog, QDialogButtonBox
import sqlite3

class KeywordManagementTab(QWidget):
    def __init__(self):
        super(KeywordManagementTab, self).__init__()
        self.initUI()
        self.load_keywords_from_db()

    def initUI(self):
        # Create a QVBoxLayout for the tab layout
        keyword_layout = QVBoxLayout()

        # Create QLineEdit for keyword input and a QPushButton for validation
        input_layout = QHBoxLayout()
        self.keyword_input = QLineEdit()
        self.validate_button = QPushButton("Valider")
        input_layout.addWidget(self.keyword_input)
        input_layout.addWidget(self.validate_button)

        # Create QListWidget for displaying validated keywords
        self.keyword_list = QListWidget()

        # Create buttons for editing and deleting keywords
        self.edit_button = QPushButton("Modifier")
        self.delete_button = QPushButton("Supprimer")

        # Connect the buttons' clicked signals to custom slots
        self.validate_button.clicked.connect(self.add_keyword_to_list)
        self.edit_button.clicked.connect(self.edit_selected_keyword)
        self.delete_button.clicked.connect(self.delete_selected_keyword)

        # Add widgets to layout
        keyword_layout.addLayout(input_layout)
        keyword_layout.addWidget(self.keyword_list)
        keyword_layout.addWidget(self.edit_button)
        keyword_layout.addWidget(self.delete_button)

        self.setLayout(keyword_layout)

    def add_keyword_to_list(self):
        # Get the text from keyword_input
        keyword = self.keyword_input.text()

        # Add the text to keyword_list
        self.keyword_list.addItem(keyword)

        # Clear the keyword_input
        self.keyword_input.clear()

        # Store the keyword in the database
        self.store_keyword_in_db(keyword)

    def edit_selected_keyword(self):
        # Get the selected keyword from the list
        selected_items = self.keyword_list.selectedItems()

        if selected_items:
            old_keyword = selected_items[0].text()

            # Open a QDialog to get the new keyword
            new_keyword, ok = self.show_edit_dialog(old_keyword)

            if ok:
                # Update the keyword in the list and database
                selected_items[0].setText(new_keyword)
                self.update_keyword_in_db(old_keyword, new_keyword)

    def delete_selected_keyword(self):
        # Get the selected keyword from the list
        selected_items = self.keyword_list.selectedItems()

        if selected_items:
            keyword_to_delete = selected_items[0].text()
            
            # Remove the keyword from the list
            self.keyword_list.takeItem(self.keyword_list.row(selected_items[0]))

            # Delete the keyword from the database
            self.delete_keyword_from_db(keyword_to_delete)

    def show_edit_dialog(self, old_keyword):
        dialog = QDialog()
        dialog.setWindowTitle("Modifier le mot-clé")
        dialog_layout = QVBoxLayout()
        input_edit = QLineEdit(old_keyword)
        dialog_layout.addWidget(input_edit)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dialog_layout.addWidget(button_box)
        dialog.setLayout(dialog_layout)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        ok = dialog.exec_()
        return input_edit.text(), ok == QDialog.Accepted

    def store_keyword_in_db(self, keyword):
        conn = sqlite3.connect('../database/app_data.db')
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO MotsCles (mot_cle) VALUES (?)", (keyword,))
            conn.commit()
        except sqlite3.IntegrityError:
            # Handle duplicate keywords if necessary
            pass

        conn.close()

    def update_keyword_in_db(self, old_keyword, new_keyword):
        conn = sqlite3.connect('database/app_data.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE MotsCles SET mot_cle = ? WHERE mot_cle = ?", (new_keyword, old_keyword))
        conn.commit()

        conn.close()

    def delete_keyword_from_db(self, keyword):
        conn = sqlite3.connect('../database/app_data.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM MotsCles WHERE mot_cle = ?", (keyword,))
        conn.commit()

        conn.close()

    def load_keywords_from_db(self):
        conn = sqlite3.connect('../database/app_data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT mot_cle FROM MotsCles")
        keywords = cursor.fetchall()

        for keyword in keywords:
            self.keyword_list.addItem(keyword[0])

        conn.close()

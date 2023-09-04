
# Import required modules
from sklearn.feature_extraction.text import TfidfVectorizer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from db_connect import connect_to_database  # Import the database connection function
import random
import numpy as np

class AIContentSourcingTab(QWidget):
    def __init__(self):
        super(AIContentSourcingTab, self).__init__()
        self.initUI()

    def initUI(self):
        # Create a QVBoxLayout for the tab layout
        layout = QVBoxLayout()

        # Create a QLabel to describe the functionality
        description_label = QLabel("L'IA vous propose les sources de données suivantes en fonction des mots-clés:")
        layout.addWidget(description_label)

        # Create a QListWidget to display AI-suggested sources
        self.suggested_sources_list = QListWidget()
        layout.addWidget(self.suggested_sources_list)

        # Create a QPushButton to trigger AI sourcing
        source_button = QPushButton("Obtenir des sources")
        source_button.clicked.connect(self.get_ai_suggested_sources)
        layout.addWidget(source_button)

        # Create a QPushButton to save selected sources
        save_button = QPushButton("Conserver les sources sélectionnées")
        save_button.clicked.connect(self.save_selected_sources)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def get_ai_suggested_sources(self):
        # Connect to the database to fetch keywords
        conn = connect_to_database("../database/app_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT keyword FROM keywords_table")  # Replace with your actual SQL query
        keywords = [item[0] for item in cursor.fetchall()]  # Convert the results to a list of keywords

        # Close the database connection
        conn.close()

        # Using TF-IDF to analyze the importance of each keyword
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(keywords)
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = np.array(tfidf_matrix.sum(axis=0)).flatten()

        # Combine feature names and their corresponding TF-IDF scores
        tfidf_dict = dict(zip(feature_names, tfidf_scores))
        sorted_keywords = sorted(tfidf_dict, key=tfidf_dict.get, reverse=True)

        # Simulate AI suggesting sources based on top keywords
        # (Replace this with actual AI logic later)
        sample_sources = [
            "Article: Importance of Insurance",
            "Google Alert: New Insurance Regulations",
            "RSS Feed: Daily Insurance News",
            "Article: Health Insurance Policies",
            "Google Alert: Business Insurance"
        ]
        for source in random.sample(sample_sources, 3):
            source_item = QListWidgetItem(source)
            source_item.setFlags(source_item.flags() | Qt.ItemIsUserCheckable)
            source_item.setCheckState(Qt.Unchecked)
            self.suggested_sources_list.addItem(source_item)

    def save_selected_sources(self):
        # Placeholder function to save selected sources
        # (Implement actual saving logic later)
        pass

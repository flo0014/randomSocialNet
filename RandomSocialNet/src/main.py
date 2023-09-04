from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from keyword_management_tab import KeywordManagementTab  # Assuming the KeywordManagementTab class is in this file
from ai_content_sourcing_tab import AIContentSourcingTab  # Assuming the AIContentSourcingTab class is in this file
import sys

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()

        self.setWindowTitle("My AI-Assisted Content Creator")
        self.setGeometry(200, 200, 800, 600)

        # Create a QWidget for the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a QVBoxLayout for the central widget layout
        central_layout = QVBoxLayout()

        # Create a QTabWidget
        tab_widget = QTabWidget()

        # Create tabs and add them to the QTabWidget
        tab1 = KeywordManagementTab()
        tab2 = AIContentSourcingTab()

        tab_widget.addTab(tab1, "Gestion des Mots-Clés")
        tab_widget.addTab(tab2, "Sourcing de Contenu par IA")

        # Add the QTabWidget to the QVBoxLayout
        central_layout.addWidget(tab_widget)

        # Set the QVBoxLayout as the layout for the central widget
        central_widget.setLayout(central_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_app = MyApp()
    my_app.show()
    sys.exit(app.exec_())

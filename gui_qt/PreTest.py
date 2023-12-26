import sys
import os
import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QGroupBox, QRadioButton, QMessageBox, QLineEdit, QHBoxLayout
from AudioPlayer import AudioPlayer
import csv

class HomeWindow(QWidget):
    def __init__(self, media_dir, results_dir):
        super().__init__()
        self.initUI(media_dir)
        self.results_dir = results_dir


    def initUI(self, media_dir):
        layout = QVBoxLayout()
        self.setLayout(layout)


        title_label = QLabel("<h1> Pre-test Survey </h1>")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Input field for test taker's name
        name_label = QLabel("<h3> Please enter your name below: </h3>")
        name_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setMinimumSize(200, 40)
        self.name_input.setPlaceholderText("Your Name")
        layout.addWidget(self.name_input)


        layout.addSpacing(20)
        motion_sickness = QLabel("<h3> Have you ever experienced motion sickness? (riding a crazy roller coaster doesn't count) </h3>")
        motion_sickness.setAlignment(Qt.AlignLeft)
        layout.addWidget(motion_sickness)

        # Radio buttons
        self.motion_sickness = QGroupBox()
        motion_sickness_layout = QVBoxLayout()

        self.motion_sickness_true = QRadioButton("Yes")
        motion_sickness_layout.addWidget(self.motion_sickness_true)

        self.motion_sickness_false = QRadioButton("No")
        motion_sickness_layout.addWidget(self.motion_sickness_false)

        self.motion_sickness.setLayout(motion_sickness_layout)
        layout.addWidget(self.motion_sickness)

        layout.addSpacing(20)
        eardrum_suck = QLabel("<h3> Have you ever experienced the eardrum suck effect when using ANC products? </h3>")
        eardrum_suck.setAlignment(Qt.AlignLeft)
        layout.addWidget(eardrum_suck)

        # Radio buttons
        self.eardrum_suck = QGroupBox()
        eardrum_suck_layout = QVBoxLayout()

        self.eardrum_suck_true = QRadioButton("Yes")
        eardrum_suck_layout.addWidget(self.eardrum_suck_true)

        self.eardrum_suck_false = QRadioButton("No")
        eardrum_suck_layout.addWidget(self.eardrum_suck_false)
        self.eardrum_suck.setLayout(eardrum_suck_layout)
        layout.addWidget(self.eardrum_suck)


        # List of audio folders
        self.audio_folders = sorted([os.path.join(media_dir,folder) for folder in os.listdir(media_dir) if os.path.isdir(os.path.join(media_dir, folder))])
        self.randomized_tests = random.sample(self.audio_folders, len(self.audio_folders))
        self.current_test_index = 0

        print(self.audio_folders)
        print(self.randomized_tests)


        layout.addSpacing(20)
        # Create a horizontal layout for centering the button
        button_layout = QHBoxLayout()

        # Add a spacer to push the button to the center
        button_layout.addStretch(1)

        start_button = QPushButton("Start Random Test")
        start_button.clicked.connect(self.start)
        
        start_button.setMinimumSize(200, 40)

        # Set the button's stylesheet for rounded corners
        start_button.setStyleSheet("""
            QPushButton {
                border: 0.5px solid;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 12pt;
            }
        """)
        # Add the button to the button layout
        button_layout.addWidget(start_button)
        button_layout.addStretch(1)
        # Add the button layout to the main layout
        layout.addLayout(button_layout)
        layout.addStretch(1)

    def start(self):
        self.name = self.name_input.text().strip()

        if not self.name:
            QMessageBox.warning(self, "Name Required", "Please enter your name to start the tests.")
            return
        
        if self.motion_sickness_true.isChecked():
            motion_sickness = self.motion_sickness_true.text()
        elif self.motion_sickness_false.isChecked():
            motion_sickness = self.motion_sickness_false.text()
        else:
            QMessageBox.warning(self, "Motion Sickness Question not answered", "Please answer the question before proceeding.")
            return
        

        if self.eardrum_suck_true.isChecked():
            eardrum_suck = self.motion_sickness_true.text()
        elif self.eardrum_suck_false.isChecked():
            eardrum_suck = self.motion_sickness_false.text()
        else:
            QMessageBox.warning(self, "Eardrum Suck Question not answered", "Please answer the question before proceeding.")
            return
        
        header = ["ID", "eardrum_suck", "motion_sickness"]
        row = [self.name, eardrum_suck, motion_sickness]

        survey_file = os.path.join(self.results_dir, "survey.csv")
        # Check if the file exists and is empty
        file_exists = os.path.isfile(survey_file) and os.path.getsize(survey_file) > 0

        # Write to CSV
        with open(survey_file, "a", newline="") as file:
            writer = csv.writer(file)
            
            # Write header only if the file is new or empty
            if not file_exists:
                writer.writerow(header)
            
            writer.writerow(row)

        self.start_random_test()
        
    def start_random_test(self):
        if self.current_test_index < len(self.randomized_tests):
            selected_folder = self.randomized_tests[self.current_test_index]
            self.audio_test = AudioPlayer(selected_folder, self)
            self.audio_test.show()
            self.hide()
        else:
            QMessageBox.information(self, "Thank You", "Thank you for participating in the tests!")
            self.reset_survey()
            self.current_test_index = 0  # Reset for next round
            self.randomized_tests = random.sample(self.audio_folders, len(self.audio_folders))
            self.show()



    def reset_survey(self):
        # Reset the QLineEdit for name
        self.name_input.clear()

        # Reset the radio buttons for motion sickness
        self.motion_sickness_true.setAutoExclusive(False)
        self.motion_sickness_false.setAutoExclusive(False)
        self.motion_sickness_true.setChecked(False)
        self.motion_sickness_false.setChecked(False)
        self.motion_sickness_true.setAutoExclusive(True)
        self.motion_sickness_false.setAutoExclusive(True)

        # Reset the radio buttons for eardrum suck
        self.eardrum_suck_true.setAutoExclusive(False)
        self.eardrum_suck_false.setAutoExclusive(False)
        self.eardrum_suck_true.setChecked(False)
        self.eardrum_suck_false.setChecked(False)
        self.eardrum_suck_true.setAutoExclusive(True)
        self.eardrum_suck_false.setAutoExclusive(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    home = HomeWindow("/Users/nptlinh/Desktop/BA-Code/gui_qt/media/transition", "/Users/nptlinh/Desktop/BA-Code/gui_qt/results/transition")
    home.show()
    sys.exit(app.exec_())

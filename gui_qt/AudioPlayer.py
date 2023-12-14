import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel, QSizePolicy
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import random
from handle_csv import read_header
import csv

class AudioPlayer(QWidget):
    def __init__(self, audio_folder, parent_window):
        super().__init__()
        self.initUI(audio_folder)
        self.test_name = os.path.basename(audio_folder)
        self.parent_window = parent_window


    def initUI(self, audio_folder):
        main_layout = QVBoxLayout()

        title_label = QLabel('Test #')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24pt; font-weight: bold;")
        main_layout.addWidget(title_label)


        definition_label = QLabel(
            "<h2>Eardrum Suck Definitions:</h2>"
            "<ul style='font-size: 18pt;'>"
            "<li>Pressure at the eardrum</li>"
            "<li>Vibration Sensation</li>"
            "<li>Dizzyness or Headaches</li>"
            "</ul>"
        )
        definition_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(definition_label)
        main_layout.addSpacing(20)


        # Horizontal layout for the sliders
        sliders_layout = QHBoxLayout()
        main_layout.addLayout(sliders_layout)

        self.player = QMediaPlayer()
        self.player.setVolume(100)
        self.player.mediaStatusChanged.connect(self.loop_audio)

        self.files, self.permutation = self.load_audio_files(audio_folder)
        self.playing = {filename: False for filename in self.files}
        self.currently_playing = None
        self.widget_refs = {}
        self.ratings = {}

        for index, filename in enumerate(self.permutation):
            vbox = QVBoxLayout()  # Vertical layout for each audio file's controls

            # Play button at the top
            play_button = QPushButton(f'Sample #{index+1}')
            play_button.setMinimumHeight(50)
            play_button.clicked.connect(lambda _, name=filename: self.play_audio(name))
            # Set stylesheet for rounded corners
            play_button.setStyleSheet(
                "QPushButton {"
                "   border-radius: 10px;" 
                "   background-color: grey;"
                "   color: white;"
                "   font-size: 10pt;"
                "}"
                "QPushButton:pressed {"
                "   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(200, 200, 200, 255), stop:1 rgba(150, 150, 150, 255));"
                "}"
            )
            vbox.addWidget(play_button)

            # Max label
            max_label = QLabel('Strong Sensation = 10')
            max_label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(max_label)

            # Slider
            slider = QSlider(Qt.Vertical)
            slider.setRange(0, 10)
            slider.valueChanged.connect(lambda value, name=filename: self.update_slider_label(name, value))
            slider.setTickPosition(QSlider.TicksLeft)  # Set tick marks to the left
            slider.setTickInterval(1)  # Set tick interval
            slider.setMinimumSize(30, 300)  # Minimum width and height
            vbox.addWidget(slider, alignment=Qt.AlignCenter)

            # Min label
            min_label = QLabel('None = 0')
            min_label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(min_label)

            # Value label
            value_label = QLabel('Actual Value: 0')
            value_label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(value_label)

            # Store references to the slider and value label
            self.widget_refs[filename] = {'slider': slider, 'rating': value_label}
            self.ratings[filename] = 0
            vbox.addStretch(1)
            sliders_layout.addLayout(vbox)

        main_layout.addSpacing(20)
        # Create a horizontal layout for centering the button
        button_layout = QHBoxLayout()

        # Add a spacer to push the button to the center
        button_layout.addStretch(1)

        self.complete_test_button = QPushButton("Submit Test")
        self.complete_test_button.clicked.connect(self.complete_test)

        self.complete_test_button.setMinimumSize(200, 50)

        # Set the button's stylesheet for rounded corners
        self.complete_test_button.setStyleSheet("""
            QPushButton {
                border: 0.5px solid white;
                border-radius: 10px;
                padding: 10px 20px;   
                font-size: 16pt;
            }
        """)
        # Add the button to the button layout
        button_layout.addWidget(self.complete_test_button)
        button_layout.addStretch(1)

        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)
        
        self.setLayout(main_layout)
        self.setWindowTitle("Audio Player")





    def load_audio_files(self, folder):
        file_list = sorted([file for file in os.listdir(folder) if file.endswith('.wav')])
        permutation = random.sample(file_list, len(file_list))
        return file_list, permutation



    def play_audio(self, filename):
        if self.playing.get(filename):
            self.player.stop()
            self.playing[filename] = False
            self.currently_playing = None
        else:
            if self.currently_playing:
                self.playing[self.currently_playing] = False
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.join(audio_folder, filename))))
            self.player.play()
            self.playing[filename] = True
            self.currently_playing = filename



    def loop_audio(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.player.play()



    def keyPressEvent(self, event):
        if event.key() >= Qt.Key_1 and event.key() <= Qt.Key_9:
            index = event.key() - Qt.Key_1
            if index < len(self.files):
                self.play_audio(self.files[index])
        elif event.key() == Qt.Key_Space:
            self.stop_all_audio()



    def stop_all_audio(self):
        if self.currently_playing:
            self.player.stop()
            self.playing[self.currently_playing] = False
            self.currently_playing = None



    def update_slider_label(self, filename, value):
        self.widget_refs[filename]['rating'].setText(f'Actual Value: {value}')
        self.ratings[filename] = value


    def complete_test(self):
        save_file = os.path.join(self.parent_window.results_dir, f"{self.test_name}.csv")
        header = read_header(save_file)
        file_written = True

        if header is None:
            header = ["ID"] + self.files
            file_written = False
        row = [self.parent_window.name] + [self.ratings[filename] for filename in header[1:]]

        

        # Write to CSV
        with open(save_file, "a", newline="") as file:
            writer = csv.writer(file)
            
            # Write header only if the file is new or empty
            if not file_written:
                writer.writerow(header)
            
            writer.writerow(row)

        self.parent_window.current_test_index += 1
        self.parent_window.start_random_test()
        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    audio_folder = "/Users/nptlinh/Desktop/BA-Code/testing_gui/media/airplane"
    ex = AudioPlayer(audio_folder)
    ex.show()
    sys.exit(app.exec_())

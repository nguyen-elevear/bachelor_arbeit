import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel, QSizePolicy, QTextEdit
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from ClickableVBox import ClickableVBoxLayout
import random
from handle_csv import read_header
import csv

class AudioPlayer(QWidget):
    def __init__(self, audio_folder, parent_window):
        super().__init__()
        self.test_name = os.path.basename(audio_folder)
        self.audio_folder = audio_folder
        self.test_type = os.path.basename(os.path.dirname(audio_folder))
        self.parent_window = parent_window
        self.currently_selected_slider = None
        self.initUI(audio_folder)
        self.setFocusPolicy(Qt.StrongFocus)


    def initUI(self, audio_folder):
        main_layout = QVBoxLayout()

        title_label = QLabel(f'Test {self.parent_window.current_test_index+1}')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24pt; font-weight: bold;")
        main_layout.addWidget(title_label)


        if self.test_type == "filter_pos":
            definition_label = QLabel(
                "<h2> Please rate the listening experience according to this criteria:</h2>"
                "<ul style='font-size: 12pt; margin-bottom: 10px;'>"
                "<li style='margin-bottom: 5px;'><strong><em>How strongly</em></strong> do you feel a sensation that is somewhat <strong><em>similar to a muffled/clogged/blocked ear</strong></em>?"
                "<ul style='margin-bottom: 5px;'>Example for this muffled/clogged/blocked ear sensation is when you are in an airplane or high speed elevator and you need to swallow to hear normal again</ul></li>"
                "<li style='margin-bottom: 5px;'><strong><em>How strongly </strong></em> do you feel <strong><em>dizzyness or a headache</strong></em>?</li>"
                "<li style='margin-bottom: 5px;'> <strong><em>10 = Strong Sensation</strong></em>, e.g. strong headache or feel like I need to swallow to pop my ear</li>"
                "<li style='margin-bottom: 5px;'> <strong><em>0 = None, just like normal</strong></em></li>"
                "<li style='margin-bottom: 5px;'> <strong><em>5 = The criterias above describe perfectly what I feel</strong></em></li>"
                "</ul>"
                
                "<h2> How to interact with the test interface: </h2>"
                "<ul style='font-size: 12pt; margin-bottom: 10px;'>"
                "<li style='margin-bottom: 5px;'><strong><em>Press the corresponding number on the keyboard</strong></em> to switch to the desired sample. You can do this to switch between the sample to compare them with each other</li>"
                "<li style='margin-bottom: 5px;'><strong><em>\"Reference Sample\"</strong></em> is what you suppose to give a 0, notice that it can be pereceived as louder than other sample, which mean you shouldn't evaluate based on loudness</li>"
                "<li style='margin-bottom: 5px;'>When you are listening to a sample, <strong><em>the corresponding slider can be moved using W and S key</strong></em> on the keyboard</li>"
                "</ul>"
            )
        else:
            definition_label = QLabel(
                "<h2> You will be presented with listening samples of different sound transitions, each is 3 seconds long and NOT looped. </h2>"
                "<h2>The transition happens at about half way of the sample. Please pay attention to your listening experience after the transition</h2>"
                "<h2> Please rate the listening experience according to this criteria:</h2>"
                "<ul style='font-size: 12pt; margin-bottom: 10px;'>"
                "<li style='margin-bottom: 5px;'><strong><em>How strongly</em></strong> do you feel a sensation that is somewhat <strong><em>similar to a muffled/clogged/blocked ear</strong></em>?"
                "<ul style='margin-bottom: 5px;'>Example for this muffled/clogged/blocked ear sensation is when you are in an airplane or high speed elevator and you need to swallow to hear normal again</ul></li>"
                "<li style='margin-bottom: 5px;'><strong><em>How strongly </strong></em> do you feel <strong><em>dizzyness or a headache</strong></em>?</li>"
                "<li style='margin-bottom: 5px;'> <strong><em>10 = Strong Sensation</strong></em>, e.g. strong headache or feel like I need to swallow to pop my ear</li>"
                "<li style='margin-bottom: 5px;'> <strong><em>0 = None, just like normal</strong></em></li>"
                "<li style='margin-bottom: 5px;'> <strong><em>5 = The criterias above describe perfectly what I feel</strong></em></li>"
                "</ul>"
                "<h2> How to interact with the test interface: </h2>"
                "<ul style='font-size: 12pt; margin-bottom: 10px;'>"
                "<li style='margin-bottom: 5px;'><strong><em>Press the corresponding number on the keyboard</strong></em> to switch to the desired sample. You can do this to switch between the sample to compare them with each other</li>"
                "<li style='margin-bottom: 5px;'> <strong><em>\"Reference Sample\"</strong></em> is what you suppose to give a 0, it doesn't have any transition</li>"
                "<li style='margin-bottom: 5px;'>When you are listening to a sample, <strong><em>the corresponding slider can be moved using W and S key</strong></em> on the keyboard</li>"
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

        if self.test_type == "filter_pos":
            self.player.mediaStatusChanged.connect(self.loop_audio)
        else:
            self.player.mediaStatusChanged.connect(self.reset_audio)

        self.files, self.permutation = self.load_audio_files(audio_folder)
        self.playing = {filename: False for filename in self.files}
        self.currently_playing = None
        self.widget_refs = {}
        self.ratings = {}

        for index, filename in enumerate(self.permutation):
            vbox = ClickableVBoxLayout()  # Vertical layout for each audio file's controls
            print (filename)
            if "passive" not in filename:
                # Play button at the top
                play_button = QPushButton(f'Sample #{index+1}')
            else:
                play_button = QPushButton(f'Reference Sample')
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
            vbox.addSpacing(20)

            if "passive" not in filename:
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
                slider.setMinimumSize(30, 200)  # Minimum width and height
                slider.setMaximumHeight(300)
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

        # Comment Box
        self.comment_box = QTextEdit()
        self.comment_box.setPlaceholderText("Additional Comments about the samples (if any): ")
        self.comment_box.setMinimumHeight(50)
        main_layout.addWidget(self.comment_box)
        self.comment_box.setFocusPolicy(Qt.ClickFocus)

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
                border: 0.5px solid;
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
        for index, element in enumerate(permutation):
            if "passive" in element:
                reference_index = index
                break
        permutation[0], permutation[reference_index] = permutation[reference_index], permutation[0]

        return file_list, permutation



    def play_audio(self, filename):
        if self.playing.get(filename):
            self.player.stop()
            self.playing[filename] = False
            self.currently_playing = None
        else:
            if self.currently_playing:
                self.playing[self.currently_playing] = False
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.join(self.audio_folder, filename))))
            self.player.play()
            self.playing[filename] = True
            self.currently_playing = filename



    def loop_audio(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.player.play()



    def keyPressEvent(self, event):
        if not self.comment_box.hasFocus():
            key = event.key()
            if key >= Qt.Key_1 and key <= Qt.Key_9:
                index = event.key() - Qt.Key_1
                print(event.key())
                if index < len(self.files):
                    self.play_audio(self.permutation[index])
                    self.currently_selected_slider = self.permutation[index]
            elif key == Qt.Key_0:
                print(event.key())
                self.stop_all_audio()
            elif key == Qt.Key_W or key == Qt.Key_S:
                self.adjust_slider(key)
        else:
            super().keyPressEvent(event)


    def stop_all_audio(self):
        if self.currently_playing:
            self.player.stop()
            self.playing[self.currently_playing] = False
            self.currently_playing = None



    def update_slider_label(self, filename, value):
        self.widget_refs[filename]['rating'].setText(f'Actual Value: {value}')
        self.ratings[filename] = value


    def complete_test(self):
        self.stop_all_audio()
        save_file = os.path.join(self.parent_window.results_dir, f"{self.test_name}.csv")
        header = read_header(save_file)
        file_written = True
        comments = self.comment_box.toPlainText()

        if header is None:
            header = ["ID"] + [file for file in self.files if "passive" not in file] + ["comments"]
            file_written = False
        row = [self.parent_window.name] + [self.ratings[filename] for filename in header[1:]] + [comments]

        

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



    def adjust_slider(self, key):
        if self.currently_selected_slider and self.currently_selected_slider in self.widget_refs.keys():
            slider = self.widget_refs[self.currently_selected_slider]['slider']
            current_value = slider.value()
            if key == Qt.Key_W:
                slider.setValue(min(current_value + 1, slider.maximum()))
            elif key == Qt.Key_S:
                slider.setValue(max(current_value - 1, slider.minimum()))



    def reset_audio(self):
        self.playing[self.currently_playing] = False
        self.currently_playing = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    audio_folder = "/Users/nptlinh/Desktop/BA-Code/gui_qt/media/filter_pos/airplane"
    ex = AudioPlayer(audio_folder, None)
    ex.show()
    sys.exit(app.exec_())

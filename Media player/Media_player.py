from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QStyle, QSlider, QFileDialog  #library for graphics application and get button, 
"""QHBoxLayout arranges widgets horizontally, 
side by side, while QVBoxLayout arranges widgets vertically, 
one above the other"""

from PyQt5.QtGui import QIcon #library for getting icon 
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent # for design function in media player
from PyQt5.QtMultimediaWidgets import QVideoWidget # be used to display video in their application with basic controls such as play/pause/reload and volume adjustment
from PyQt5.QtCore import Qt, QUrl # support getting file location
import sys

class Window(QWidget): #create window display
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("video-player-icon-15.ico")) #set the window icon
        self.setWindowTitle("PyMedia Player") #set title for media player
        self.setGeometry(500, 100, 700, 500) #set the appearing position and width, height of window media

        self.setStyleSheet("background-color: LightBlue") #set background color 

        self.create_MediaPlayer() # display media player

    def create_MediaPlayer(self): #create media player
        
        videowidget = QVideoWidget()

        self.media_Player = QMediaPlayer()

        self.openBtn = QPushButton('Open Video') # button open video
        self.openBtn.setStyleSheet("background-color: white; color: blue; border-color: green;") # set color for background, text, border of button
        self.openBtn.clicked.connect(self.open_file) #click open button to open file and choose video

        self.playBtn = QPushButton() #play and pause button
        self.playBtn.setEnabled(False) # set play button as False
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))# set shape of play button
        self.playBtn.clicked.connect(self.play_video) # use function play_video to play or pause video

        self.slider = QSlider(Qt.Horizontal) # creates a horizontal slider and Qt.Horizontal specifies the orientation of the slider
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position) # when slider move, call function set_position

        hbox = QHBoxLayout() # create a hbox to arrange widgets horizontally, side by side
        hbox.setContentsMargins(0,0,0,0) # set size of media box
        hbox.addWidget(self.openBtn) # add button open to media box
        hbox.addWidget(self.playBtn) # add button play to media box
        hbox.addWidget(self.slider) #add slider to hbox

        vbox = QVBoxLayout() # create a vbox to arranges widgets vertically, one above the other
        vbox.addWidget(videowidget) # to control the position and size of the widget within the layout
        vbox.addLayout(hbox) # add hbox to arrange it in display

        self.media_Player.setVideoOutput(videowidget) #set the video output of the media player to the videowidget

        self.setLayout(vbox) # set vbox in display

        self.media_Player.stateChanged.connect(self.mediastate_changed) # set icon of play button: change from play/pause to play/pause
        self.media_Player.positionChanged.connect(self.position_changed) #to update the position of the slider or display the current playback time
        self.media_Player.durationChanged.connect(self.duration_changed)
        """to set the range of the slider to match the duration of the media that is being played, 
        so that the thumb of the slider can be moved along the track 
        to represent the current position of the media playback."""

    def open_file(self): #Open file media to display video
        filename, _ = QFileDialog.getOpenFileName(self, "Open video") # choose file to open 

        if filename != '':
            self.media_Player.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    def play_video(self): 
        if self.media_Player.state() == QMediaPlayer.PlayingState:#to see if it is currently playing media
            self.media_Player.pause()
        else:
            self.media_Player.play()

    def mediastate_changed(self): # to change icon of play button
        if self.media_Player.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position): 
        self.slider.setValue(position) #to set the value of the slider to the specified position argument.

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.media_Player.setPosition(position) #to change the current position of the media playback to the specified value.

app = QApplication([])
window = Window()
window.show() # Show window
sys.exit(app.exec()) 

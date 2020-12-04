# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from PyQt5 import QtWidgets, QtGui, QtCore
from UI.Label import Ui_MainWindow
import ffmpeg
import pytube
import sys
import threading
import os
import subprocess

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

class MergeThread (threading.Thread):
   def __init__(self, threadID, audio_file_name, video_file_name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.audio_file_name = audio_file_name
      self.video_file_name = video_file_name

   def run(self):
      print ("Starting " + self.name)
      # Get lock to synchronize threads
      input_audio = ffmpeg.input(self.audio_file_name)
      input_video = ffmpeg.input(self.video_file_name)
      ffmpeg.concat(input_video, input_audio, a=1, v=1).output('./finish.mp4').run()




def merge_video(audio_file_name, video_file_name):
    input_audio = ffmpeg.input(audio_file_name)
    input_video = ffmpeg.input(video_file_name)
    ffmpeg.concat(input_video, input_audio, a=1, v=1).output('./finish.mp4').run()
    #subprocess.run(['python3','ff.py'])

def percent(self, tem, total):
    perc = (float(tem) / float(total)) * float(100)
    return perc

#def progress_function(self, stream, chunk, file_handle, bytes_remaining):
#    size = video.filesize
#    p = 0
#    while p <= 100:
#        progress = p
#        print
#        str(p) + '%'
#        p = percent(bytes_remaining, size)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_dl.clicked.connect(self.dlbuttonClicked)
        self.ui.pushButton_getlists.clicked.connect(self.glbuttonClicked)

    def dlbuttonClicked(self):
        print('start to download')
        print('select : ', self.ui.comboBox_videoformat.currentText())
        tmp = self.ui.comboBox_videoformat.currentText()
        video_info = tmp.split('"')
        print(video_info)
        video_tag = video_info[1]
        self.yt.streams.get_by_itag(video_tag).download(output_path='./', filename='video')
        tmp = self.ui.comboBox_audioformat.currentText()
        audio_info = tmp.split('"')
        audio_tag = audio_info[1]
        self.yt.streams.get_by_itag(audio_tag).download(output_path='./', filename='audio')
        mt = MergeThread(1, './audio.webm', './video.webm')
        mt.start()
        #merge_video('./audio.webm', './video.webm')
        #t = threading.Thread(target=merge_video('./audio.webm', './video.webm'))
        #t.start()

    def glbuttonClicked(self):
        print('start to get lists')
        videolink = self.ui.textEdit_url.toPlainText()
        print('videolink : ', videolink)
        yt = pytube.YouTube(videolink)
        self.yt = yt

        stream_count = yt.streams.count()
        streams = str(yt.streams.all())
        stream = streams.split(',')

        audio_streams = str(yt.streams.filter(subtype='webm',only_audio=True).all)
        audio_stream = audio_streams.split(',')
        print(audio_streams)
        self.ui.comboBox_audioformat.addItems(audio_stream)


        video_streams = str(yt.streams.filter(subtype='webm', only_video=True).all)
        video_stream = video_streams.split(',')
        print(video_streams)
        self.ui.comboBox_videoformat.addItems(video_stream)

        #yt.streams.get_by_itag(247).download('./')
        #progress_streams = str(yt.streams.filter(progressive=True).all)
        #progress_stream = progress_streams.split(',')
        #print("progress streams : ", progress_streams)
        #self.ui.comboBox_videoformat.addItems(progress_stream)

        #yt.streams.get_by_itag(135).download('./')
        #yt.streams.get_lowest_resolution().download('./')

        #adapter_streams = str(yt.streams.filter(adaptive=True))
        #print("adapter_stream: ", adapter_streams)
        #for i in range(len(stream)):
            #print('a : ', stream[i])
            #self.ui.comboBox_videoformat.addItems(stream)
        #yt.streams.first().download('./')



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

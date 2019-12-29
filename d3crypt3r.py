from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5.QtMultimedia import QSound
import os
import sys
import time
import algorithm

FROM_SPLASH,_ = loadUiType(os.path.join(os.path.dirname(__file__),"./assests/splash.ui"))
FROM_MAIN,_ = loadUiType(os.path.join(os.path.dirname(__file__),"./assests/main_screen.ui"))

class ThreadProgress(QThread):

    mysignal = pyqtSignal(int)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.ThreadActiveFlag = True

    def run(self):
        i = 0
        while (i<101 and self.ThreadActiveFlag):
            time.sleep(0.03)
            self.mysignal.emit(i)
            if (i>=26 and i<30):
                time.sleep(0.3)

            if (i>=35 and i<40):
                time.sleep(0.3)

            if (i>=76 and i<81):
                time.sleep(0.1)

            if (i>=95 and i<101):
                time.sleep(0.4)

            i +=1

    def killthread(self):
        self.ThreadActiveFlag = False
        self.wait()


class ThreadProgress2(QThread):

    def __init__(self,num,tar,UpdateTime,UpdateCount,List,Total,Lucky,Five,parent = None):
        QThread.__init__(self, parent)
        self.ThreadActiveFlag = True
        self.num = num
        self.tar = tar
        self.UpdateTime = UpdateTime
        self.UpdateCount = UpdateCount
        self.addItem = List.addItem
        self.clearList = List.clear
        self.CountList = List.count
        self.UpdateTotal = Total
        self.Lucky = Lucky
        self.Five = Five

    def run(self):
        if self.CountList() > 0:
            self.clearList()

        self.Target = int(self.tar)
        self.Result, self.Time, self.Count = algorithm.Solve(self.Target, self.num)

        self.isEmpty = not bool(len(self.Result))

        if self.isEmpty:
            self.Time = 0
            self.Count = 0

        self.UpdateTotal(len(self.Result))
        self.UpdateTime(self.Time)
        self.UpdateCount(self.Count)

        if self.isEmpty:
            self.addItem("NO RESULT!!!")

        if not self.isEmpty:

            if self.Five.isChecked():
                self.Result = self.Result[:5]

            elif self.Lucky.isChecked() and not self.Five.isChecked():
                self.temp = self.Result[0]
                self.Result = []
                self.Result.append(self.temp)

            for i in self.Result:
                self.addItem(i)

class MusicThread(QThread):

    mysignal = pyqtSignal(bool)

    def __init__(self,MusicCheck,parent=None):
        QThread.__init__(self, parent)
        self.ThreadActiveFlag = True
        self.MusicCheck = MusicCheck

    def run(self):
        while self.ThreadActiveFlag:
            time.sleep(0.05)
            if self.MusicCheck.isChecked():
                i = True
            else:
                i = False
            self.mysignal.emit(i)

    def killthread(self):
        self.ThreadActiveFlag = False
        self.wait()

class Main(QMainWindow,FROM_MAIN):

    switch_window = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        pixmap = QPixmap("./assests/hacettepe_small.png")
        pixmap1 = QPixmap("./assests/im1.png")
        pixmap2 = QPixmap("./assests/im2.png")
        pixmap3 = QPixmap("./assests/im3.png")

        self.hctp.setPixmap(pixmap.scaled(61, 90))
        self.im1.setPixmap(pixmap2.scaled(150, 150))
        self.im2.setPixmap(pixmap1.scaled(150, 150))
        self.im3.setPixmap(pixmap3.scaled(150, 150))
        self.pushButton.clicked.connect(self.decrypt)
        self.numbers.returnPressed.connect(self.pushButton.click)
        self.target.returnPressed.connect(self.pushButton.click)
        self.music = QSound("./assests/sound.wav")
        self.i_last = False
        self.MusicThread = MusicThread(self.check_music)
        self.MusicThread.mysignal.connect(self.playMusic)
        self.MusicThread.start()

    @pyqtSlot(int)
    def progress(self, i):
        self.progressBar.setValue(i)
        if i == 100:
            self.hide()
            self.login()

    @pyqtSlot(bool)
    def playMusic(self,i):
        if self.i_last != i:
            if i:
                self.music.play()
            else:
                self.music.stop()
        self.i_last = i


    def login(self):
        self.switch_window.emit()

    def decrypt(self):
        try:
            if self.thread.isRunning():
                self.thread.quit()
        except:
            pass
        if len(self.numbers.text())>0 and len(self.target.text()) > 0:
            for i in self.numbers.text():
                if not i in ["0","1","2","3","4","5","6","7","8","9"," ",","]:
                    QMessageBox.critical(self, "ERROR", "Numbers input format must be like '1,5,78,124,646,3,543'")
                    return False

            if not self.target.text().isnumeric():
                QMessageBox.critical(self, "ERROR", "Target input must be Integer")
                return False

            try:
                self.Num = list(map(int, self.numbers.text().split(",")))
            except ValueError:
                QMessageBox.critical(self, "ERROR", "Numbers input format must be like '1,5,78,124,646,3,543'")
                return False

            self.thread = ThreadProgress2(self.Num,self.target.text(),self.time.display,self.count.display,self.list,self.total.display,self.check_lucky,self.check_5)
            self.thread.start()

        else:
            QMessageBox.critical(self, "ERROR", "Numbers and Target fields can not be empty.")



class Intro(QMainWindow,FROM_SPLASH):

    switch_window = pyqtSignal()

    def __init__(self, parent=None):

        super(Intro, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        pixmap = QPixmap("./assests/background.jpg")
        self.splah_image_2.setPixmap(pixmap.scaled(640, 480))
        pixmap = QPixmap("./assests/hacettepe_black.png")
        self.splah_image.setPixmap(pixmap.scaled(217, 320))
        self.thread = ThreadProgress(self)
        self.thread.mysignal.connect(self.progress)
        self.thread.start()

    @pyqtSlot(int)
    def progress(self, i):
        self.progressBar.setValue(i)
        if i == 100:
            self.hide()
            self.login()

    def login(self):
        self.switch_window.emit()


class Controller:

    def __init__(self):
        self.icon = QIcon('./assests/icon.png')
        pass

    def show_intro(self):
        self.login = Intro()
        self.login.setWindowIcon(self.icon)
        self.login.switch_window.connect(self.show_main)
        self.login.show()

    def show_main(self):
        self.login.close()
        self.window = Main()
        self.window.setWindowIcon(self.icon)
        self.window.show()


    def ExitHandler(self):
        self.login.thread.killthread()
        quit()


class App:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.controller = Controller()
        self.controller.show_intro()
        self.app.aboutToQuit.connect(self.controller.ExitHandler)
        sys.exit(self.app.exec_())

APP = App()
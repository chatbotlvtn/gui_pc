import sys, os
import requests
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
import openpyxl
import cv2
from rasa_nlu_speech import speech_recognize, nlu
from rasa_ans import response
from bai26nox import *
from pyzbar.pyzbar import decode
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
faceCascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")

class MainWindow(QMainWindow):
    ab = 0
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        self.timer = QTimer()
        self.timer.timeout.connect(self.viewCam)
        self.controlTimer()

        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.showTime)
        self.controlTimer1()

        self.player = QMediaPlayer()
        self.uic.btn_speak.clicked.connect(self.listen)
        self.uic.btn_del.clicked.connect(self.xoa_het)
        self.uic.confirm_btn.clicked.connect(self.confirm)
        self.uic.search_btn.clicked.connect(self.find)

        self.uic.kethon_btn.clicked.connect(self.ket_hon)
        self.uic.giamho_btn.clicked.connect(self.giam_ho)
        self.uic.ngheo_btn.clicked.connect(self.ngheo)
        self.uic.dichuc_btn.clicked.connect(self.di_chuc)
        self.uic.nvqs_btn.clicked.connect(self.nvqs)

        self.uic.kethon_tamtru.clicked.connect(self.kethon_tamtru)
        self.uic.tu_y_kethon.clicked.connect(self.tu_y_kethon)
        self.uic.thgian_nghi_kh.clicked.connect(self.thgian_nghi_kh)
        self.uic.hoan_nvqs.clicked.connect(self.hoan_nvqs)
        self.uic.congchung_dichuc.clicked.connect(self.congchung_dichuc)
        self.uic.dk_giamho.clicked.connect(self.dk_giamho)

    # view camera
    def viewCam(self):
        # read image in BGR format
        ret, img = self.cap.read()
        # convert image to RGB format
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        self.uic.lbdisplay.setPixmap(QPixmap.fromImage(qImg))

        ImageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        np_face = faceCascade.detectMultiScale(ImageGray, 1.1, 4)
        rcv_val = self.printing(np_face)
        qr_code =self.read_code(img)
        if ((rcv_val !=None) and (self.ab ==0)):
            self.playAudioFile("greet.mp3")
            self.ab=1
        elif ((rcv_val ==None) and (self.ab ==1)):
            self.ab = 0
        if qr_code != None:
            self.data_dis(qr_code)

    def read_code(self,img):
        for code in decode(img):
            data = code.data.decode('utf-8')
            return data

    def data_dis (self, data):
        split_data = data.split("|")
        dob_trc = list(split_data[3])
        dob_nam = ''.join(dob_trc[4:8])
        dob_sau = dob_trc[0] + dob_trc[1] + "/" + dob_trc[2] + dob_trc[3] + "/" + dob_nam
        self.uic.nameLineEdit.setText(split_data[2])
        self.uic.sexLineEdit.setText(split_data[4])
        self.uic.DOBLineEdit.setText(dob_sau)
        self.uic.addLineEdit.setText(split_data[5])
        self.uic.cccdLineEdit.setText(split_data[0])

    def playAudioFile(self, name):
        full_file_path = os.path.join(os.getcwd(), name)
        url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    def printing(self, np_hinh):
        for (x,y,w,h) in np_hinh:
            return x

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(20)
            # update control_bt text
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text

    def check_internet(self):
        url = "https://www.geeksforgeeks.org"
        timeout = 10
        try:
            request = requests.get(url, timeout=timeout)
            self.result = True
        except (requests.ConnectionError, requests.Timeout) as exception:
            self.result = False
        return self.result

    def listen (self):
        internet = self.check_internet()
        if internet == True:
            self.playAudioFile("listening.mp3")
            self.timer.timeout.disconnect(self.viewCam)
            self.heard = speech.bot_listen()
            self.feedback()

        else:
            a = QMessageBox()
            a.setText('Không có Internet, bạn vui lòng tìm kiếm bằng cách nhập vào ô phía dưới')
            b = a.exec_()

    def pop(self,i):
        btn = i.text()
        if btn == 'OK':
            intention = rasa_module.rasa_nlu(self.heard)
            reply = replies.user_ans(intention)
            # title = replies.task(intention)
            self.uic.textBrowser.setText(reply)
            self.playAudioFile("result.mp3")
            self.timer.timeout.connect(self.viewCam)
        else:
            self.timer.timeout.connect(self.viewCam)

    def feedback (self):
        if self.heard != None:
            a = QMessageBox()
            a.setText(self.heard)
            a.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
            a.buttonClicked.connect(self.pop)
            b = a.exec_()

        else:
            a = QMessageBox()
            a.setText('Vui lòng thử lại')
            a.setStandardButtons(QMessageBox.Ok)
            a.buttonClicked.connect(self.start_cam)
            b = a.exec_()

    def start_cam(self):
        self.timer.timeout.connect(self.viewCam)

    def get_update(self):
        wb = openpyxl.load_workbook('ds1.xlsx')
        i = 2;
        cell_cccd = "%s%s" % ("B", i)
        Sheet1 = wb['Sheet1']
        d = Sheet1[cell_cccd].value
        while d != None:
            i = i + 1
            cell_cccd = "%s%s" % ("B", i)
            d = Sheet1[cell_cccd].value
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        cell_time = "%s%s" % ("A", i)
        cell_name = "%s%s" % ("C", i)
        cell_dob = "%s%s" % ("D",i)
        cell_sex = "%s%s" % ("E", i)
        cell_add = "%s%s" % ("F",i)
        cell_task = "%s%s" % ("G",i)
        Sheet1[cell_cccd].value = self.uic.cccdLineEdit.text()
        Sheet1[cell_name].value = self.uic.nameLineEdit.text()
        Sheet1[cell_dob].value = self.uic.DOBLineEdit.text()
        Sheet1[cell_sex].value = self.uic.sexLineEdit.text()
        Sheet1[cell_add].value = self.uic.addLineEdit.text()
        Sheet1[cell_time].value = dt_string
        Sheet1[cell_task].value = self.uic.thTCLineEdit.text()
        wb.close()
        wb.save('ds1.xlsx')

        a = QMessageBox()
        a.setText('Hệ thống đã ghi lại thông tin của bạn')
        b = a.exec_()

    def confirm(self):
        if self.uic.thTCLineEdit.text() != "":
            self.get_update()
        else:
            a = QMessageBox()
            a.setText('Vui lòng nhập đủ thông tin')
            b = a.exec_()

    def xoa_het(self):
        self.uic.nameLineEdit.setText("")
        self.uic.sexLineEdit.setText("")
        self.uic.DOBLineEdit.setText("")
        self.uic.addLineEdit.setText("")
        self.uic.cccdLineEdit.setText("")
        self.uic.textBrowser.setText("Bạn có thể nói hoặc chọn các chức năng bên dưới để được hỗ trợ nhé! Khi đã đồng ý thì chọn 'Xác nhận' phía trên.")
        self.uic.thTCLineEdit.setText("")
        self.uic.line_search.setText("")

    def showTime(self):
            now = datetime.now()
            date = now.strftime("%d/%m/%Y")
            tim = now.strftime("%H:%M:%S")
            self.uic.ngYLineEdit.setText(date)
            self.uic.thIGianLineEdit.setText(tim)
    def controlTimer1(self):
        if not self.timer1.isActive():
            self.timer1.start(1000)
        else:
            self.timer1.stop()

    def find(self):
        a = self.uic.line_search.text()
        if a!="":
            intention = rasa_module.rasa_nlu(a)
            reply = replies.user_ans(intention)
            self.uic.textBrowser.setText(reply)
            self.playAudioFile("result.mp3")
        else:
            a = QMessageBox()
            a.setText('Vui lòng nhập thông tin bạn cần tìm')
            a.setStandardButtons(QMessageBox.Ok)
            b = a.exec_()


    def ket_hon(self):
        f = replies.ket_hon_re()
        self.uic.textBrowser.setText(f)
        self.uic.thTCLineEdit.setText("Đăng ký kết hôn")
    def nvqs(self):
        f = replies.nvqs_re()
        self.uic.textBrowser.setText(f)
        self.uic.thTCLineEdit.setText("Đăng ký nghĩa vụ quân sự")
    def ngheo(self):
        f = replies.ho_ngheo_re()
        self.uic.textBrowser.setText(f)
        self.uic.thTCLineEdit.setText("Đăng ký xác nhận hộ nghèo")
    def giam_ho(self):
        f = replies.giam_ho_re()
        self.uic.textBrowser.setText(f)
        self.uic.thTCLineEdit.setText("Đăng ký giám hộ")
    def di_chuc(self):
        f= replies.di_chuc_re()
        self.uic.textBrowser.setText(f)
        self.uic.thTCLineEdit.setText("Chứng thực di chúc")
    def kethon_tamtru(self):
        f = replies.kethon_tamtru()
        self.uic.textBrowser.setText(f)
    def tu_y_kethon (self):
        f = replies.tu_y_kethon()
        self.uic.textBrowser.setText(f)
    def thgian_nghi_kh (self):
        f = replies.thgian_nghi_kh()
        self.uic.textBrowser.setText(f)
    def hoan_nvqs (self):
        f = replies.hoan_nvqs()
        self.uic.textBrowser.setText(f)
    def congchung_dichuc (self):
        f = replies.congchung_dichuc()
        self.uic.textBrowser.setText(f)
    def dk_giamho (self):
        f = replies.dk_giamho()
        self.uic.textBrowser.setText(f)

speech = speech_recognize()
rasa_module = nlu()
replies = response()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())
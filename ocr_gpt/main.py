import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, pyqtSlot
from firstpage import Ui_Form

from chat import Ui_Form as Ui_Chat
from PyQt5.QtGui import QCursor, QPainterPath, QRegion, QFont, QImage, QPixmap
from new_task import Ui_Dialog
from PyQt5.QtCore import QTimer
import asyncio

import time
import pyautogui
import os, subprocess
from PIL import ImageGrab
import pyperclip
import pytesseract
from pytesseract import Output
import tensorflow as tf
import keras
from keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import cv2
import pygetwindow as gw
import pickle
import numpy as np
import matplotlib.pyplot as plt

from socket import *

import wmi
import subprocess
import re

import win32api
import win32net
from gptProcess import new_task

with open("labels.pkl", "rb") as f:
    labels = pickle.load(f)

print(labels)

# Load the saved CNN model.
cnn_model = tf.keras.models.load_model('saved_model')


class ChatBox(QWidget):
    def __init__(self, text, avatar, parent=None):
        super().__init__()
        self.ui = Ui_Chat()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        if avatar=="user":
            self.ui.avatar.setPixmap(QPixmap(":/assets/user.png"))
            self.ui.chat_user.setText("Linda")
        else:
            self.ui.avatar.setPixmap(QPixmap(":/assets/robot.png"))
            self.ui.chat_user.setText("OSVisualInstruct")

        self.ui.chat_content.setText(text)
        self.ui.chat_time.setText(time.strftime("%Y-%m-%d %H:%M:%S"))
        
        

class CustomCheckBox(QWidget):
    def __init__(self, text, parent=None):
        super(CustomCheckBox, self).__init__(parent)

        # Create a horizontal layout
        layout = QHBoxLayout()
        # Create the checkbox
        self.checkbox = QCheckBox()
        self.checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:unchecked {
                image: url(:/assets/unchecked.png);
            }
            QCheckBox::indicator:checked {
                image: url(:/assets/checked.png);
            }
            QCheckBox::indicator:checked:hover {
                image: url(:/assets/checkhover.png);
            }
            QCheckBox::indicator:unchecked:hover {
                image: url(:/assets/uncheckhover.png);
            }
            QCheckBox {
                color: #fff;
            }
        """)

        # Create the label
        self.label = QLabel(text)
        font = QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel{\n"
        "    color: #fff;\n"
        "}")
        # Add the checkbox and label to the layout
        layout.addWidget(self.checkbox)
        layout.addWidget(self.label, 1)

        # Set the layout for the custom checkbox
        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.stackedWidget.setCurrentIndex(0)
        radius = 30.0
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), radius, radius)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)

        self.scrgrab = None

        self.dlg = ChildDlg()
        self.dlg.hide()
        self.ui.plus_new_task_button.clicked.connect(self.clickDlg)
        self.ui.home_button.clicked.connect(self.closeDlg)
        self.dlg.saveClicked.connect(self.saveTask)
        self.ui.expanded.clicked.connect(self.showTaskList)

        #set screenshot
        self.screenShotFlag = True
        self.ui.switch_checkbox.stateChanged.connect(self.setScreenShot)

        #Show process modal.
        self.modal = ModalDialog()
        self.modal.hide()

        #Captured screenshot
        self.ui.pushButton.clicked.connect(self.click_capture)

        self.showTaskListFlag = False
        # checkbox_layout = QVBoxLayout(self.ui.listWidget)

        # Set the checkbox_widget layout to the QVBoxLayout
        # self.ui.listWidget.setLayout(checkbox_layout)

        # add timer
        self.timer = QTimer(self)

        self.timer.timeout.connect(self.update_screen)
        self.start_timer()

    def start_timer(self):
        self.timer.start(4000)


    def update_screen(self):
        if(self.screenShotFlag):
            # self.capture_screenshot()
            self.updateComputerVision()
            # self.perform_predict(os.path.join(os.getcwd(), "screenshot.png"))
            # self.perform_ocr(os.path.join(os.getcwd(), "screenshot.png"))


    def closeDlg(self):
        self.dlg.hide()

    def updateComputerVision(self):
        if self.scrgrab:
            qimage = QImage(self.scrgrab.tobytes(), self.scrgrab.width, self.scrgrab.height, QImage.Format_RGB888)
            # Load the .png file
            image_path = "processed_img.png"
            pixmap = QPixmap(image_path)         
            # pixmap = QPixmap.fromImage(qimage)
            if not pixmap.isNull():
                self.ui.screen_label.setPixmap(pixmap)
            # print(self.scrgrab.width, self.scrgrab.height, QImage.Format_RGB888)
    
    def setScreenShot(self):
        if(not self.screenShotFlag):
            if self.scrgrab:
                qimage = QImage(self.scrgrab.tobytes(), self.scrgrab.width, self.scrgrab.height, QImage.Format_RGB888).rgbSwapped()
                self.ui.screen_label.setPixmap(QPixmap.fromImage(qimage))
            self.screenShotFlag = True
        else:
            self.ui.screen_label.setPixmap(QPixmap())
            self.screenShotFlag = False
    
    def showTaskList(self):
        if(self.showTaskListFlag):
            self.ui.listWidget.hide()
            self.showTaskListFlag = False
        else:
            self.ui.listWidget.show()
            self.showTaskListFlag = True

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moveFlag = True
            self.movePosition = event.globalPos() - self.pos()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            event.accept()

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.moveFlag:
            self.move(event.globalPos() - self.movePosition)
            event.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.moveFlag = False
        self.setCursor(Qt.CrossCursor)

    def clickDlg(self):
        self.dlg.show()
    
    def saveTask(self, task_name):
        custom_checkbox = CustomCheckBox(task_name)
        list_item = QListWidgetItem()
        list_item.setSizeHint(custom_checkbox.sizeHint())
        self.ui.listWidget.addItem(list_item)
        self.ui.listWidget.setItemWidget(list_item, custom_checkbox)

    def saveConversation(self, conversation, avatar):
        chat = ChatBox(conversation, avatar)
        list_item = QListWidgetItem()
        list_item.setSizeHint(chat.size())
        self.ui.chat_list.addItem(list_item)
        self.ui.chat_list.setItemWidget(list_item, chat)
        print(self.ui.chat_list.count())
        

    @pyqtSlot()
    def click_capture(self):

        # self.modal.label.setText("Processing")
        # self.modal.show()
        # self.ui.pushButton.setEnabled(False)
        # self.textbox.setPlainText("")

        # self.update()
        # time.sleep(0.1)
        # t_start = time.perf_counter()
        prompt = self.ui.message_content.toPlainText()
        print(prompt)
        
        self.saveConversation(prompt, "user")
        self.saveConversation("Taking screenshot to understand desktop environement...\nSending request to Chat-gpt-3.5-turbo to build out sub-tasks...", "gpt")
        time.sleep(3)
        


        subtaskList = new_task(prompt)
        for subtask in subtaskList:
            self.saveTask(subtask)
        print(subtaskList)

        self.capture_screenshot()
        self.perform_ocr(os.path.join(os.getcwd(), "screenshot.png"))
        

        # self.perform_predict(os.path.join(os.getcwd(), "screenshot.png"))

        # self.button.setEnabled(True)
        # self.label.setText("The OCR result has been copied to your clipboard.\nLast run: {:.2f} seconds".format(time.perf_counter() - t_start))

        self.update()

    def capture_screenshot(self):
        # width, height= pyautogui.size()
        # window_rect = (0, 0, width, height)


        # Get all the open windows
        windows = gw.getAllWindows()
        
        # Get the second window (index 1)
        curWindow = windows[2]
        # window = windows[2]

        titleList = gw.getAllTitles()

        title = titleList[3]
        print(title)
        # window.activate()


        # Get the position and size of the second window frame
        # window_rect = (window.left, window.top, window.width, window.height)


        # curWindow.activate()
        ##
        window = pyautogui.getActiveWindow()
        window_rect = window.left, window.top, window.width, window.height
        print(window_rect)
        self.scrgrab = pyautogui.screenshot(region=window_rect)
        self.scrgrab.save(r'screenshot.png')







    def perform_predict(self, filename):

        image = cv2.imread(filename)

        # Resize the image to the desired shape
        resized_image = cv2.resize(image, (212, 212))
        resized_image = np.array(resized_image)
        # print(resized_image.shape)
        # Expand the dimensions to match the model input shape
        input_image = np.expand_dims(resized_image, axis=0)
        # print(input_image.shape)


        # Make a prediction using the CNN model.
        pred = cnn_model.predict(input_image)

        # print(pred)

        # Display the prediction.
        idx = 0
        predicted_label = labels[np.argmax(pred[idx])]
        # print(predicted_label)

    def perform_ocr(self, filename):
        
        img = cv2.imread(filename)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # cv2.Canny(gray_img, 100, 200)


        d = pytesseract.image_to_data(img, output_type=Output.DICT)
        # print(d.keys())
        n_boxes = len(d['text'])
        for i in range(n_boxes):
            if int(d['conf'][i]) > 60:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        imageNames = os.listdir('./buttons')
        
        for imageName in imageNames:
            try:
                button7location = pyautogui.locateOnScreen('./buttons/'+imageName, confidence=0.9)
                print('postion:', button7location)
                button7point = pyautogui.center(button7location)
                button7x, button7y = button7point
                print(button7x, button7y)
                pyautogui.moveTo(button7x, button7y)
                time.sleep(0.5)
                img = cv2.rectangle(img, (button7location.left, button7location.top), (button7location.left + button7location.width, button7location.top+button7location.height), (0, 0, 255), 2)
            except Exception as e:
                continue
            # button7location = pyautogui.locateOnScreen('./buttons/'+imageName, confidence=0.6)
            
            # pyautogui.click(button7x, button7y)
        cv2.imshow('img', img)
        cv2.imwrite('processed_img.png', img)
        cv2.waitKey(0)




class ChildDlg(QWidget):
    i = 0
    saveClicked = pyqtSignal(str)
    def __init__(self):
        super().__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        radius = 20.0
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), radius, radius)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
 
        self.ui.start_task_label.mousePressEvent = self.status
        self.ui.close_button.clicked.connect(self.hide)
        self.ui.save_button.clicked.connect(self.saveTask)
    def status(self, event):
        if event.button() == Qt.LeftButton:
            self.i = not self.i
        if self.i == False:
            self.ui.start_task_label.setStyleSheet("QLabel{\n"
                "    background:#828080;\n"
                "    color: #fff;\n"
                "    border-radius: 19px;\n"
                "}")
            self.ui.start_task_label.setText("Stop Task")
        else:
            self.ui.start_task_label.setStyleSheet("QLabel{\n"
                "    background:#d68620;\n"
                "    color: #fff;\n"
                "    border-radius: 19px;\n"
                "}")
            self.ui.start_task_label.setText("Start Task")

    def saveTask(self) :
        self.saveClicked.emit(self.ui.task_description.toPlainText())

class ModalDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Task is processing...')
        
        # Add your widgets to the dialog
        layout = QVBoxLayout()
        self.label = QLabel("")
        layout.addWidget(self.label)
        childLayout = QHBoxLayout()
        childLayout.addWidget(QPushButton('OK'))
        childLayout.addWidget(QPushButton('Cancel'))
        layout.addLayout(childLayout)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

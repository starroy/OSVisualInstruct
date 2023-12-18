import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRectF, pyqtSignal
from firstpage import Ui_Form
from PyQt5.QtGui import QCursor, QPainterPath, QRegion, QFont
from new_task import Ui_Dialog


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

        self.dlg = ChildDlg()
        self.dlg.hide()
        self.ui.plus_new_task_button.clicked.connect(self.clickDlg)
        self.ui.home_button.clicked.connect(self.closeDlg)
        self.dlg.saveClicked.connect(self.saveTask)
        self.ui.expanded.clicked.connect(self.showTaskList)
        self.showTaskListFlag = True
        # checkbox_layout = QVBoxLayout(self.ui.listWidget)

        # Set the checkbox_widget layout to the QVBoxLayout
        # self.ui.listWidget.setLayout(checkbox_layout)


    def closeDlg(self):
        self.dlg.hide()
    
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

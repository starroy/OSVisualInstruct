
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QCheckBox, QVBoxLayout, QWidget

app = QApplication([])

# Create a widget
widget = QWidget()

# Create a layout
layout = QVBoxLayout(widget)

# Create a checkbox
checkbox = QCheckBox("Toggle Animation")
layout.addWidget(checkbox)

# Create a label to display the animation
label = QLabel()
layout.addWidget(label)

# Load the images for checked and unchecked states
unchecked_image = QPixmap("D:\Development/11_10/assets/Switch1.png")
checked_image = QPixmap("D:\Development/11_10/assets/Switch 2.png")

# Set the initial state of the checkbox
checkbox.setChecked(False)

# Function to update the label image based on checkbox state
def update_label_image(state):
    if state == Qt.Checked:
        label.setPixmap(checked_image)
        animate_toggle()
    else:
        label.setPixmap(unchecked_image)

# Function to animate the toggle effect
def animate_toggle():
    animation = QPropertyAnimation(label, b"geometry")
    animation.setDuration(500)
    animation.setStartValue(label.geometry())
    animation.setEndValue(label.geometry().adjusted(0, 0, 0, 20))
    # animation.setEasingCurve(Qt.Edges)
    animation.start()

# Connect the checkbox stateChanged signal to the update_label_image slot
checkbox.stateChanged.connect(update_label_image)

# Set the style sheet for the checkbox
checkbox.setStyleSheet("""
    QCheckBox::indicator {
        width : 40px;
        height : 20px;
    }
    QCheckBox::indicator:unchecked {
        image: url(:/assets/Switch1.png);
    }
    QCheckBox::indicator:checked {
        image: url(:/assets/Switch 2.png);
    }
    QCheckBox{
        color : #fff;
    }
""")

# Show the widget
widget.show()

# Start the application event loop
app.exec_()

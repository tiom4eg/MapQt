from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import requests

coordX = float(input("Type latitude (up to 6 digits after point): "))
coordY = float(input("Type longitude (up to 6 digits after point): "))
spn = 1


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(785, 480)
        self.pixmapHolder = QtWidgets.QLabel(Form)
        self.pixmapHolder.setGeometry(QtCore.QRect(15, 15, 600, 450))
        self.pixmapHolder.setText("")
        self.pixmapHolder.setObjectName("pixmapHolder")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(620, 10, 160, 141))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.rb = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.rb.setObjectName("rb")
        self.verticalLayout.addWidget(self.rb)
        self.rb2 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.rb2.setObjectName("rb2")
        self.verticalLayout.addWidget(self.rb2)
        self.rb3 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.rb3.setObjectName("rb3")
        self.verticalLayout.addWidget(self.rb3)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(620, 160, 161, 28))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.rb.setText(_translate("Form", "схема"))
        self.rb2.setText(_translate("Form", "спутник"))
        self.rb3.setText(_translate("Form", "гибрид"))
        self.pushButton.setText(_translate("Form", "Показать"))



class App(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.type = "map"
        self.loadImage()
        self.pushButton.clicked.connect(self.run)
        self.radio_buttons = [self.rb, self.rb2, self.rb3]

    def keyPressEvent(self, event):
        global spn, coordX, coordY
        if event.key() == QtCore.Qt.Key_PageUp:
            if spn != 179.5:
                spn += 0.5
                self.loadImage()
        elif event.key() == QtCore.Qt.Key_PageDown:
            if spn != 0.5:
                spn -= 0.5
                self.loadImage()
        elif event.key() == QtCore.Qt.Key_Left:
            if -180 < coordX <= -179.5:
                coordX = 179.5
            else:
                coordX -= 0.5
            self.loadImage()
        elif event.key() == QtCore.Qt.Key_Right:
            if 179.5 <= coordX < 180:
                coordX = -179
            else:
                coordX += 0.5
            self.loadImage()
        elif event.key() == QtCore.Qt.Key_Up:
            if 89.5 <= coordY < 90:
                coordY = -89
            else:
                coordY += 0.5
            self.loadImage()
        elif event.key() == QtCore.Qt.Key_Down:
            if -90 < coordY <= -89.5:
                coordY = 89
            else:
                coordY -= 0.5
            self.loadImage()

    def loadImage(self):
        request = f"https://static-maps.yandex.ru/1.x/?ll={coordX},{coordY}&spn={spn},{spn}&l=map"
        response = requests.get(request)
        if not response:
            print("Request error:")
            print(request)
            print("HTTP", response.status_code, "(" + response.reason + ")")
            sys.exit(1)
        with open("map.png", "wb") as file:
            file.write(response.content)
            file.close()
            self.pixmap = QtGui.QPixmap("map.png")
            self.pixmapHolder.setPixmap(self.pixmap)
            print("set!")
            print(spn, coordX, coordY)
            print(request)

    def run(self):
        if self.rb.isChecked():
            self.type = "map"
        if self.rb2.isChecked():
            self.type = "sat"
        if self.rb3.isChecked():
            self.type = "sat,skl"
        self.loadImage()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    exe = App()
    exe.show()
    sys.exit(app.exec())

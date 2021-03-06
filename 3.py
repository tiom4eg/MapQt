from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import requests

coordX = float(input("Type latitude (up to 6 digits after point): "))
coordY = float(input("Type longitude (up to 6 digits after point): "))
spn = 1


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(630, 480)
        self.pixmapHolder = QtWidgets.QLabel(Form)
        self.pixmapHolder.setGeometry(QtCore.QRect(15, 15, 600, 450))
        self.pixmapHolder.setText("")
        self.pixmapHolder.setObjectName("pixmapHolder")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Карта"))


class App(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loadImage()

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    exe = App()
    exe.show()
    sys.exit(app.exec())


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
        global spn
        if event.key() == QtCore.Qt.Key_PageUp:
            spn += 0.5
            self.loadImage()
        elif event.key() == QtCore.Qt.Key_PageDown:
            spn -= 0.5
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
            self.pixmap = QtGui.QPixmap("map.png")
            self.pixmapHolder.setPixmap(self.pixmap)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    exe = App()
    exe.show()
    sys.exit(app.exec())

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import requests

spn = 1


def func(toponym):
    size = toponym["boundedBy"]["Envelope"]["lowerCorner"].split()
    size1 = toponym["boundedBy"]["Envelope"]["upperCorner"].split()
    return str(abs(float(size[0]) - float(size1[0])) / 2), str(abs(float(size[1]) - float(size1[1])) / 2)


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
        self.line = QtWidgets.QLineEdit(Form)
        self.line.setGeometry(QtCore.QRect(620, 200, 161, 22))
        self.line.setObjectName("line")

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
        self.address = "Moscow"
        self.loadImage()
        self.pushButton.clicked.connect(self.run)
        self.radio_buttons = [self.rb, self.rb2, self.rb3]


    def keyPressEvent(self, event):
        global spn, coordX, coordY
        if event.key() == QtCore.Qt.Key_PageUp:
            spn += 0.5
            self.loadImage()
        elif event.key() == QtCore.Qt.Key_PageDown:
            spn -= 0.5
            self.loadImage()
        elif event.key() == QtCore.Qt.Key_Left:
            coordX -= 0.5
            self.loadImage()
        elif event.key() == QtCore.Qt.Key_Right:
            coordX += 0.5
            self.loadImage()
        elif event.key() == QtCore.Qt.Key_Up:
            coordY += 0.5
            self.loadImage()
        elif event.key() == QtCore.Qt.Key_Down:
            coordY -= 0.5
            self.loadImage()

    def loadImage(self):
        print(self.address)
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": self.address,
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)

        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

        delta, delta1 = func(toponym)[0], func(toponym)[1]

        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join([delta, delta1]),
            "l": self.type,
            "pt": ",".join([toponym_longitude, toponym_lattitude])
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        self.map_file = "map.png"
        with open("map.png", "wb") as file:
            file.write(response.content)
            file.close()
            self.pixmap = QtGui.QPixmap("map.png")
            self.pixmapHolder.setPixmap(self.pixmap)

    def run(self):
        if self.rb.isChecked():
            self.type = "map"
        if self.rb2.isChecked():
            self.type = "sat"
        if self.rb3.isChecked():
            self.type = "sat,skl"
        self.address = self.line.text()
        if self.address == "":
            self.address = "Moscow"
        self.loadImage()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = App()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

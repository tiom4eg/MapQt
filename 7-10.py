# Первая заповедь кода - не трогай, пока работает
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import requests


# DO NOT TOUCH
def cutRectangle(toponym):
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
        self.resetButton = QtWidgets.QPushButton(Form)
        self.resetButton.setGeometry(QtCore.QRect(620, 230, 161, 25))
        self.resetButton.setObjectName("resetButton")
        self.addressLabel = QtWidgets.QTextEdit(Form)
        self.addressLabel.setGeometry(QtCore.QRect(620, 260, 161, 70))
        self.addressLabel.setObjectName("addressLabel")
        self.addressLabel.setReadOnly(True)
        self.isPostCBox = QtWidgets.QCheckBox(Form)
        self.isPostCBox.setGeometry(QtCore.QRect(620, 340, 161, 20))
        self.isPostCBox.setObjectName("addressLabel")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Карта"))
        self.rb.setText(_translate("Form", "Cхема"))
        self.rb2.setText(_translate("Form", "Cпутник"))
        self.rb3.setText(_translate("Form", "Гибрид"))
        self.pushButton.setText(_translate("Form", "Показать"))
        self.resetButton.setText(_translate("Form", "Сброс"))
        self.isPostCBox.setText(_translate("Form", "Показывать индекс"))


class App(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.type = "map"
        self.search = "Moscow"
        self.coordX, self.coordY = 37.622504, 55.753215
        self.pX, self.pY = 37.622504, 55.753215
        self.spnX, self.spnY = 1, 1
        self.address = "Россия, Москва"
        self.isPost = False
        self.loadImage()
        self.pushButton.clicked.connect(self.run)
        self.resetButton.clicked.connect(self.reset)
        self.isPostCBox.clicked.connect(self.switchPost)
        self.radio_buttons = [self.rb, self.rb2, self.rb3]

    # Processing key manipulations | tiom4eg
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_PageUp:
            if self.spnX < 180 - min(self.spnX / self.spnY, 1) * 0.1 and self.spnY < 180 - min(self.spnY / self.spnX, 1) * 0.1:
                self.spnX, self.spnY = self.spnX + min(self.spnX / self.spnY, 1) * 0.1,\
                                       self.spnY + min(self.spnY / self.spnX, 1) * 0.1
                self.loadImage()
        elif event.key() == QtCore.Qt.Key_PageDown:
            if self.spnX > min(self.spnX / self.spnY, 1) * 0.1 and self.spnY > min(self.spnY / self.spnX, 1) * 0.1:
                self.spnX, self.spnY = self.spnX - min(self.spnX / self.spnY, 1) * 0.1,\
                                       self.spnY - min(self.spnY / self.spnX, 1) * 0.1
                self.loadImage()
        elif event.key() == QtCore.Qt.Key_Left:
            if -180 < self.coordX <= -179.9:
                self.coordX = 179.9
            else:
                self.coordX -= 0.1
            self.loadImage()
        elif event.key() == QtCore.Qt.Key_Right:
            if 179.9 <= self.coordX < 180:
                self.coordX = -179.9
            else:
                self.coordX += 0.1
            self.loadImage()
        elif event.key() == QtCore.Qt.Key_Up:
            if 89.9 <= self.coordY < 90:
                self.coordY = -89.9
            else:
                self.coordY += 0.1
            self.loadImage()
        elif event.key() == QtCore.Qt.Key_Down:
            if -90 < self.coordY <= -89.9:
                self.coordY = 89.9
            else:
                self.coordY -= 0.1
            self.loadImage()

    # Load image with geocode&static | Ju5t_Nick
    def loadImage(self):
        # Get map with static and show it
        mapRequest = f'http://static-maps.yandex.ru/1.x/?ll={self.coordX},{self.coordY}' \
                         f'&spn={self.spnX},{self.spnY}&l={self.type}&pt={self.pX},{self.pY}'
        response = requests.get(mapRequest)
        with open("map.png", "wb") as file:
            file.write(response.content)
            file.close()
            self.pixmap = QtGui.QPixmap("map.png")
            self.pixmapHolder.setPixmap(self.pixmap)
        self.addressLabel.setText(self.address)

    def newCoords(self):
        # Get coords from geocode
        coordsRequest = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b" \
                        f"&geocode={self.search}&format=json"
        response = requests.get(coordsRequest)
        json_response = response.json()
        geoObject = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        address = geoObject["metaDataProperty"]["GeocoderMetaData"]["text"]
        if self.isPost:
            try:
                address = f'{address}\nПочтовый индекс: {geoObject["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]}'
            except KeyError:
                # Object's post index doesn't exist at all.
                pass
        longitude, latitude = geoObject["Point"]["pos"].split(" ")
        delta, delta1 = cutRectangle(geoObject)
        # Converting map coords to class coords for moving/scaling
        self.coordX, self.coordY, self.spnX, self.spnY = float(longitude), float(latitude), float(delta), float(delta1)
        self.pX, self.pY = float(longitude), float(latitude)
        self.address = address
        self.loadImage()

    def run(self):
        if self.rb.isChecked():
            self.type = "map"
        if self.rb2.isChecked():
            self.type = "sat"
        if self.rb3.isChecked():
            self.type = "sat,skl"
        self.search = self.line.text()
        if self.search == "":
            self.search = "Moscow"
        self.newCoords()

    def reset(self):
        self.type = "map"
        self.search = "Moscow"
        self.coordX, self.coordY = 37.622504, 55.753215
        self.pX, self.pY = 37.622504, 55.753215
        self.spnX, self.spnY = 1, 1
        self.line.setText("")
        self.address = "Россия, Москва"
        self.loadImage()

    def switchPost(self):
        self.isPost = ~self.isPost
        self.newCoords()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = App()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

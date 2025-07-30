from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, Qt, QPropertyAnimation, QEasingCurve)
from PySide6.QtGui import (QColor, QPainter, QPainterPath, QIcon)
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
import res_rc
import sys
import speedtest

res_rc.qInitResources()  # Добавляем вызов инициализации ресурсов

class SpeedTestApp(QMainWindow):
    def __init__(self):
        super(SpeedTestApp, self).__init__()
        self.ui = Ui_SpeedTest()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.ui.exitButton.clicked.connect(self.close)  # Подключаем кнопку выхода к слоту закрытия приложения

        # Устанавливаем фиксированный размер окна
        self.setFixedSize(250, 370)

        # Убираем стандартное меню Windows и делаем окно прозрачным
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Добавляем анимацию для кнопок
        self.add_animation(self.ui.exitButton, QRect((250 - 40) // 2, 310, 40, 40))
        self.add_animation(self.ui.pushButton, QRect(30, 230, 191, 50))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 24, 24)  # Закругляем углы на 24 пикселя
        painter.setClipPath(path)
        painter.fillPath(path, QColor(0, 0, 0, 0))  # Прозрачный фон
        painter.end()

    def add_animation(self, button, original_rect):
        button.animation = QPropertyAnimation(button, b"geometry")
        button.animation.setDuration(200)
        button.animation.setEasingCurve(QEasingCurve.OutBounce)
        button.original_rect = original_rect

        button.enterEvent = lambda event: self.animate_button_enter(button)
        button.leaveEvent = lambda event: self.animate_button_leave(button)

    def animate_button_enter(self, button):
        button.animation.stop()
        button.animation.setStartValue(button.geometry())
        button.animation.setEndValue(QRect(button.original_rect.x() - 5, button.original_rect.y() - 5, button.original_rect.width() + 10, button.original_rect.height() + 10))
        button.animation.start()

    def animate_button_leave(self, button):
        button.animation.stop()
        button.animation.setStartValue(button.geometry())
        button.animation.setEndValue(button.original_rect)
        button.animation.start()

    def on_pushButton_clicked(self):
        st = speedtest.Speedtest()
        st.get_best_server()
        d = round(st.download() / (10**6), 2)
        u = round(st.upload() / (10**6), 2)
        self.ui.label_3.setText(QCoreApplication.translate("SpeedTest", f"\u0421\u043a\u043e\u0440\u043e\u0441\u0442\u044c \u043e\u0442\u0434\u0430\u0447\u0438: {d} Mbps", None))
        self.ui.label_2.setText(QCoreApplication.translate("SpeedTest", f"\u0421\u043a\u043e\u0440\u043e\u0441\u0442\u044c \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0438: {u} Mbps", None))

class Ui_SpeedTest(object):
    def setupUi(self, SpeedTest):
        if SpeedTest.objectName():
            SpeedTest.setObjectName(u"SpeedTest")
        SpeedTest.resize(250, 370)
        self.centralwidget = QWidget(SpeedTest)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet("background:transparent;")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 250, 370))
        self.widget.setStyleSheet("background:transparent;")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 250, 370))
        self.label.setStyleSheet(u"background-image: url(:/image/Project/images/purple_gradient_intense.png);\n"
"border-radius: 20px;")  # Устанавливаем прозрачный фон
        self.label.setScaledContents(False)
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(30, 230, 191, 50))
        self.pushButton.setStyleSheet(u"background-color: rgba(61, 61, 61, 170);\n"
"color: rgb(193, 193, 193);\n"
"font: 20pt \"Segoe UI Variable\";\n"
"border-radius: 20px;")
        self.horizontalLayoutWidget = QWidget(self.widget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 280, 251, 91))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutWidget = QWidget(self.widget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 30, 251, 181))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"background-color: rgba(61, 61, 61, 170);\n"
"color: rgb(193, 193, 193);\n"
"font: 12pt \"Segoe UI Variable\";\n"
"border-radius: 20px;\n"
"padding-left: 5px;")
        self.label_2.setWordWrap(True)  # Устанавливаем перенос текста

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"background-color: rgba(61, 61, 61, 170);\n"
"color: rgb(193, 193, 193);\n"
"font: 12pt \"Segoe UI Variable\";\n"
"border-radius: 20px;\n"
"padding-left: 5px;")
        self.label_3.setWordWrap(True)  # Устанавливаем перенос текста

        self.verticalLayout.addWidget(self.label_3)

        # Добавляем кнопку выхода
        self.exitButton = QPushButton(self.widget)
        self.exitButton.setObjectName(u"exitButton")
        self.exitButton.setGeometry(QRect((250 - 40) // 2, 310, 40, 40))  # Смещаем кнопку вверх и устанавливаем по центру оси X
        self.exitButton.setStyleSheet(u"background-color: rgba(255, 0, 0, 170);\n"
"border-radius: 20px;")
        self.exitButton.setIcon(QIcon(":/image/Project/images/exit_icon.png"))

        SpeedTest.setCentralWidget(self.centralwidget)

        self.retranslateUi(SpeedTest)

        QMetaObject.connectSlotsByName(SpeedTest)
    # setupUi

    def retranslateUi(self, SpeedTest):
        SpeedTest.setWindowTitle(QCoreApplication.translate("SpeedTest", u"SpeedTest", None))
        self.label.setText("")
        self.pushButton.setText(QCoreApplication.translate("SpeedTest", u"\u041d\u0430\u0447\u0430\u0442\u044c \u0442\u0435\u0441\u0442", None))
        self.label_3.setText(QCoreApplication.translate("SpeedTest", u"\u0421\u043a\u043e\u0440\u043e\u0441\u0442\u044c \u043e\u0442\u0434\u0430\u0447\u0438: ", None))
        self.label_2.setText(QCoreApplication.translate("SpeedTest", u"\u0421\u043a\u043e\u0440\u043e\u0441\u0442\u044c \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0438:", None))
        self.exitButton.setText("")
    # retranslateUi

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeedTestApp()
    window.show()
    sys.exit(app.exec())

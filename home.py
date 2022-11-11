import random
import sys

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class Color(QWidget):  # подключение цветов

    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(400, 600)
        self.setWindowTitle("My App")

        layout = QGridLayout()
        # layout.setStyleSheet('background: black; color: white;')
        self.letters = []
        self.word = self.GenerateWord()
        self.button1 = QPushButton(self.word)
        self.button2 = QPushButton("Проверить")
        self.x = 0
        self.y = 0
        self.button1.clicked.connect(self.OnChangeWord)
        self.button2.clicked.connect(self.onCheck)

        layout.addWidget(self.button1, 0, 5, 2, 2)

        for i in range(1, 7):
            self.letters.append([])
            for j in range(1, 6):
                te = QTextEdit()
                te.setStyleSheet('font-size: 50px;padding:0;')
                te.setMaximumSize(50, 50)
                # te.setV
                te.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                te.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                # te.setAlignment(Qt.AlignmentFlag.AlignCenter)
                te.setReadOnly(True)
                self.letters[i - 1].append(te)
                layout.addWidget(te, i + 1, j + 1)

        layout.addWidget(self.button2, 8, 3, 4, 3)
        widget = QWidget()
        widget.setStyleSheet('background: black; color: white;')
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def keyPressEvent(self, e):
        if e.key() == 16777219:
            if self.x == 0:
                return
            self.x -= 1
            self.letters[self.y][self.x].setText("")
            return
        if e.key() == 16777220:
            self.onCheck()
            return
        if self.x > 4 or e.key() < 1040 or e.key() > 1071:
            return

        self.letters[self.y][self.x].setText(e.text())
        self.x += 1

    def onCheck(self):
        if self.x < 5:
            return

        userlet = ""
        for x in range(0, 5):
            let = self.letters[self.y][x]
            userlet += let.toPlainText()
        print(userlet)
        f = open('words.txt', 'r', encoding="utf-8")
        exist = False
        for line in f:

            if userlet == line.strip():
                exist = True
                break

        f.close()

        if not exist:
            layout = QVBoxLayout()
            dlg = QDialog(self)
            dlg.setWindowTitle("Warning!")
            message = QLabel("Введенное слово не существует")
            layout.addWidget(message)
            dlg.setLayout(layout)
            dlg.exec()
            return

        for x in range(0, 5):
            let = self.letters[self.y][x]
            # print(let.toPlainText())

            if let.toPlainText() in self.word:
                let.setStyleSheet(' background: white; color: black')
                if self.word[x] == let.toPlainText():
                    let.setStyleSheet(' background: #fedd2c; color: black')
            else:
                let.setStyleSheet(' background: #5f5f5f;')

        self.y += 1
        self.x = 0

        if userlet == self.word:
            layout = QVBoxLayout()
            dlg = QDialog(self)
            dlg.setWindowTitle("WIN!")
            dlg.setFixedSize(200, 100)
            dlg.setStyleSheet('font-size: 20px;')
            message = QLabel("Поздравляю! \nВы угадали слово")
            layout.addWidget(message)
            dlg.setLayout(layout)
            dlg.exec()

            app.exit()

        elif self.y == 6:
            layout = QVBoxLayout()
            dlg = QDialog(self)
            dlg.setWindowTitle("Lose!")
            dlg.setFixedSize(200, 100)
            dlg.setStyleSheet('font-size: 20px;')
            message = QLabel("Не сегодня)")
            layout.addWidget(message)
            dlg.setLayout(layout)
            dlg.exec()
            app.exit()

    def GenerateWord(self):

        x = random.randint(0, 2128)
        f = open('words.txt', 'r', encoding="utf-8")
        c = 0
        for line in f:
            c += 1
            if c > x:
                world = line.strip()
                break
        f.close()
        return world

    def OnChangeWord(self):
        self.word = self.GenerateWord()
        self.button1.setText(self.word)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

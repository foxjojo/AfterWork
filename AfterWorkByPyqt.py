# 打包指令  pyinstaller -F XX.py -w
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import time
app = QApplication([])
app.setApplicationName("摸鱼计时器")
window = QWidget()
window.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
background = QLabel()

gifPath = os.getcwd()+"/background.gif"
if os.path.exists(gifPath):
    move = QMovie(gifPath)
    move.start()
    if move.currentImage().width() > move.currentImage().height():
        move.setScaledSize(
            QSize(120, 120 * move.currentImage().height() / move.currentImage().width()))
    else:
        move.setScaledSize(
            QSize(120 * move.currentImage().width() / move.currentImage().height(), 120))

    background.setMovie(move)
    background.setFixedSize(QSize(280, 120))
else:
    background.setFixedSize(QSize(120, 120))
# background.setStyle(QTStyle.Popup)
# 这里用QSS定义QLabel内颜色
app.setStyleSheet(
    "QLabel{color:#FF8C00;}")

cusTimes = ''
if(os.path.exists("time.txt")):
    with open(r"time.txt", "r", encoding="utf-8") as f:
        cusTimes = f.read().replace('：', ':')

if(cusTimes != ''):
    tip = QLabel("-------距离"+cusTimes+"-------")
else:
    tip = QLabel("-------距离下班-------")
tip.setAlignment(Qt.AlignCenter)
#tip.setFont(QFont('Times', 20))
remainS = QLabel()
# remainS.setStyleSheet("color:#FF8C00;font-size:17px")
remainS.setAlignment(Qt.AlignCenter)

remainM = QLabel()
# remainM.setStyleSheet("color:#FF8C00;font-size:17px")

remainM.setAlignment(Qt.AlignCenter)
remainH = QLabel()
# remainH.setStyleSheet("color:#FF8C00;font-size:17px")

remainH.setAlignment(Qt.AlignCenter)
tip1 = QLabel("-------距离发薪日-------")
# tip1.setStyleSheet("color:#FF8C00;font-size:17px")
tip1.setAlignment(Qt.AlignCenter)
if(cusTimes == ''):
    tip1.setVisible(True)
else:
    tip1.setVisible(False)

remainPayRemunerationD = QLabel()
# remainPayRemunerationD.setStyleSheet("color:#FF8C00;font-size:17px")
remainPayRemunerationD.setAlignment(Qt.AlignCenter)

if(cusTimes == ''):
    remainPayRemunerationD.setVisible(True)
else:
    remainPayRemunerationD.setVisible(False)

if(cusTimes != ''):
    todayAfterWorkTime = time.strftime(
        "%Y-%m-%d ", time.localtime()) + cusTimes
else:
    todayAfterWorkTime = time.strftime(
        "%Y-%m-%d ", time.localtime()) + "18:00:00"

todayAfterWorkTimestamp = time.mktime(
    time.strptime(todayAfterWorkTime, "%Y-%m-%d %H:%M:%S"))
remunerationDTimestamp = 0
if(time.localtime(time.time()).tm_mon+1 > 12):
    remunerationD = (str)(time.localtime(
        time.time()).tm_year+1)+" 1 5 9:00:00"
else:
    remunerationD = (str)(time.localtime(time.time()).tm_year) + \
        " "+(str)(time.localtime(time.time()).tm_mon+1) + " 5 9:00:00"
remunerationDTimestamp = time.mktime(
    time.strptime(remunerationD, "%Y %m %d %H:%M:%S"))


def UpdateTime():
    global todayAfterWorkTimestamp
    global remunerationDTimestamp
    s = todayAfterWorkTimestamp - time.time()
    if(s < 0):
        if(cusTimes != ''):
            remainS.setText("计时结束")
            remainM.setText("计时结束")
            remainH.setText("计时结束")
        else:
            remainS.setText("已经下班了还不快滚！")
            remainM.setText("已经下班了还不快滚！")
            remainH.setText("已经下班了还不快滚！")
    else:
        remainS.setText("还剩"+"{:.0f}".format(s)+"秒")
        remainM.setText("约为"+"{:.0f}".format(s/60)+"分钟")
        remainH.setText("约为"+"{:.1f}".format(s/60/60)+"小时")
        d = ((remunerationDTimestamp - time.time())/60/60/24)
        remainPayRemunerationD.setText("{:.0f}".format(d)+"天")
        if s < -43200:
            todayAfterWorkTimestamp += 86400


mainLayout = QHBoxLayout()
layout = QVBoxLayout()

mainLayout.addWidget(background)
layout.setAlignment(Qt.AlignRight)
layout.addWidget(tip)
layout.addWidget(remainS)
layout.addWidget(remainM)
layout.addWidget(remainH)
layout.addWidget(tip1)
layout.addWidget(remainPayRemunerationD)

th = QTimer()
th.timeout.connect(UpdateTime)
th.start(1000)

background.setLayout(layout)
window.setLayout(mainLayout)
window.show()
window.setFixedSize(window.width(), window.height())
app.exec()

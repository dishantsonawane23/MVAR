from software_v2 import Ui_MainWindow  # importing our generated file
from PyQt5 import QtCore,QtGui,QtWidgets,uic, QtTest
from PyQt5.QtWidgets import QApplication,QMainWindow,QLabel,QDesktopWidget,QFileDialog
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtCore import QThread ,pyqtSlot,pyqtSignal,Qt
import thread
import sys
import time
import numpy as np
sys.path.remove(sys.path[1])
import cv2
class mywindow(QtWidgets.QMainWindow):
	status = pyqtSignal(bool)
	switch = pyqtSignal(bool)
	def __init__(self):
		super(mywindow, self).__init__()
		self.ui = Ui_MainWindow()

		self.th = thread.Thread(self)

		self.link()

		self.running = False

		self.th.ThreadBool = True

		self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)

		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

		self.qtRectangle = self.frameGeometry()

		self.centerPoint = QDesktopWidget().availableGeometry().center()

		self.qtRectangle.moveCenter(self.centerPoint)

		self.move(self.qtRectangle.topLeft())

		self.ui.setupUi(self)

		self.ui.stackedWidget.setStyleSheet("background-color: rgb(57, 158, 229);")

		self.ui.centralwidget.setStyleSheet("background-color: rgb(255,255 , 255);")

		self.ui.frame_3.setStyleSheet("background-color: rgb(57, 158, 229);")

		self.ui.exit.clicked.connect(self.exitbtn)

		self.ui.stackedWidget.setCurrentIndex(0)

		self.ui.detailbtn.clicked.connect(self.threadvidstr)

		self.ui.radiusButton.clicked.connect(self.radius)

		self.ui.heightButton.clicked.connect(self.height)

		self.ui.choicefromimg.clicked.connect(self.browseImg)

	def mousePressEvent(self, event):

		if event.buttons() == QtCore.Qt.LeftButton:

			self.dragPos = event.globalPos()

			event.accept()

	def mouseMoveEvent(self, event):

		if event.buttons() == QtCore.Qt.LeftButton:

			self.move(self.pos() + event.globalPos() - self.dragPos)

			self.dragPos = event.globalPos()

			event.accept()

	def link(self):
		self.status.connect(self.th.runThread)

		self.switch.connect(self.th.switch)

	@pyqtSlot(QImage)
	def setImage(self,image):

		self.ui.label.setPixmap(QPixmap.fromImage(image))

	@pyqtSlot(int)
	def radiusin(self,val):
		self.ui.pr3.display(val)
		
		self.ui.pr4.display(pow(val,2)*3.14)

	@pyqtSlot(int)
	def wigth(self,val):
		self.ui.pr1.display(val)
	
	@pyqtSlot(int)
	def height(self,val):
		self.ui.pr2.display(val)

	
	@pyqtSlot(str)
	def sta(self,arg):
		self.ui.pr6.setText(arg)


	def threadvidstr(self):
		self.th.changePixmap.connect(self.setImage)

		self.th.changeRadius.connect(self.radiusin)

		self.th.changewidth.connect(self.wigth)

		self.th.changehight.connect(self.height)

		self.th.changeStatus.connect(self.sta)

		self.th.start()

		self.status.emit(True)

	def exitbtn(self):
		self.status.emit(False)
		time.sleep(1)
		sys.exit()

	def radius(self):
		self.switch.emit(True)

	def height(self):
		self.switch.emit(False)

	def browseImg(self):
		self.status.emit(False)
		fname = QFileDialog.getOpenFileName(self, 'Open file','', "Image files (*.jpg *.gif *.jpeg *.png)")
		imagePath = fname[0]
		img = cv2.imread(imagePath)
		frame= img
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,20,param1=70,param2=55,minRadius=0,maxRadius=0)
		if circles is not None:
			circles = np.uint16(np.around(circles))
			for i in circles[0,:]:
				cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
							# draw the center of the circle
				cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
				self.ui.pr3.display(i[2])
				self.ui.pr4.display(3.14*i[2]*i[2])

		#img = cv2.rectangle(img, (40,130), (350,220), (0,0,255), 2) 
		rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		h, w, ch = rgbImage.shape
		bytesPerLine = ch * w
		convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
		p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
		self.ui.label.setPixmap(QPixmap.fromImage(p))
		self.ui.pr6.setText("Circle")
		

app = QtWidgets.QApplication([])

application = mywindow()

application.show()

sys.exit(app.exec())

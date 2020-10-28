from PyQt5 import QtCore
from PyQt5.QtCore import QThread ,pyqtSignal ,Qt,pyqtSlot
from PyQt5.QtGui import QPixmap,QImage
import sys
sys.path.remove(sys.path[1])
import cv2
import numpy as np
class Thread(QThread):
	changePixmap = pyqtSignal(QImage)
	changeRadius = pyqtSignal(int)
	changewidth = pyqtSignal(int)
	changehight = pyqtSignal(int)
	changeStatus = pyqtSignal(str)
	QThread.ThreadBool = True
	QThread.switch = True

	def run(self):
		cap =  cv2.VideoCapture(0)
		while (QThread.ThreadBool):
			ret,frame =cap.read()
			if ret:
				if(QThread.switch):
					gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
					frame = cv2.medianBlur(frame,5)
					circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,20,param1=70,param2=55,minRadius=0,maxRadius=0)
					if circles is not None:
						circles = np.uint16(np.around(circles))
						for i in circles[0,:]:
							cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
							# draw the center of the circle
							cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
							self.changeRadius.emit(i[2])
					rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
					h, w, ch = rgbImage.shape
					bytesPerLine = ch * w
					convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
					p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
					self.changePixmap.emit(p)
					self.changeStatus.emit("Circle")
				else:
					img = frame
					gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
					edges = cv2.Canny(gray, 75, 150)
					lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, maxLineGap=250)
					ret,thresh = cv2.threshold(gray,127,255,1)
					contours,h = cv2.findContours(thresh,1,2)
					for cnt in contours:
						approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
						x, y, w, h = cv2.boundingRect(cnt)
						self.changewidth.emit(h)
						self.changehight.emit(w)
						# draw a green rectangle to visualize the bounding rect
						cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
					rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
					h, w, ch = rgbImage.shape
					bytesPerLine = ch * w
					convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
					p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
					self.changePixmap.emit(p)
					self.changeStatus.emit("Width")

	@pyqtSlot(bool)
	def runThread(self,f_t):
		QThread.ThreadBool = f_t

	def switch(self,switchKey):
		QThread.switch = switchKey



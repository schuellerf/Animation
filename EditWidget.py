# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- Animation workbench
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------
from PySide import QtCore, QtGui
from say import *

class _EditWidget(QtGui.QWidget):
	'''double clicked dialog''' 
	def __init__(self, dialer,obj,menu,noclose,*args):
		QtGui.QWidget.__init__(self, *args)
		obj.widget=self
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.vollabel =QtGui.QLabel( "<b>"+obj.Object.Label+"</b>")
		self.obj=obj

		self.obj.start()

		if dialer:
			dial = QtGui.QDial()
			dial.setNotchesVisible(True)
			self.dial=dial
			dial.setMinimum(-100)
			dial.setMaximum(100)

			edi = QtGui.QLineEdit()
			edi.setText("0")
			dial.setValue(0)
			dial.valueChanged.connect(lambda: edi.setText(f"{dial.value()} %"))
			edi.textChanged.connect(lambda:dial.setValue(int(edi.text().strip("%"))))
			dial.valueChanged.connect(lambda: obj.dialer(dial.value() / 100))


		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.vollabel)

		for m in menu:
			bt=QtGui.QPushButton(m[0])
			bt.clicked.connect(m[1])
			layout.addWidget(bt)

		if dialer:
			layout.addWidget(dial)
			layout.addWidget(edi)

		if not noclose:
			self.pushButton02 = QtGui.QPushButton("close")
			self.pushButton02.clicked.connect(self.close2)
			layout.addWidget(self.pushButton02)

		self.setLayout(layout)
		try:
			self.setWindowTitle(obj.Object.target.Label)
		except:
			pass
	def keyPressEvent(self, e):
		print(f"{e} / {QtCore.Qt.Key_Escape}")
		if e.key() == QtCore.Qt.Key_Escape:
			self.close2()
		# Consume the event so that it is not repeated at EditableText level
		e.accept()

	def closeEvent(self, event):
		self.close2()
		event.accept()

	def close2(self):
		sayErr("close2")
		self.hide()
		say("2")
		say(self.obj)
		self.obj.close()
		FreeCAD.tt=self.obj
		self.obj.Object.ViewObject.Visibility=False
		say("done")

class EditWidget(_EditWidget):
	def __init__(self, obj,menu,noclose,*args):
		_EditWidget.__init__(self, True, obj,menu,noclose,*args)

class EditNoDialWidget(_EditWidget):
	def __init__(self, obj,menu,noclose,*args):
		_EditWidget.__init__(self, False, obj,menu,noclose,*args)

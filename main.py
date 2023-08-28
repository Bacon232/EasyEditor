import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from PyQt5.QtGui import QPixmap 


from PIL import Image
from PIL.ImageQt import ImageQt # для перевода графики из Pillow в Qt 
from PIL import ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)
app = QApplication([])
win = QWidget()
win.setWindowTitle('Easy Editor')
win.resize(700, 500)
lb_image = QLabel('Картинка')
btn_dir = QPushButton('Папка')
lw_files = QListWidget()

btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_flip = QPushButton('Зеркало')
btn_sharp = QPushButton('Разкость')
btn_bw = QPushButton('Ч/Б')
row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image)
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)
row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)



workdir = ''
def filter(files, extensions):
   result = list()
   for filename in files:
      for ext in extensions:
         if filename.endswith(ext):
            result.append(filename)
   return result         

def chooseWorkDir():
   global workdir
   workdir = QFileDialog.getExistingDirectory()

def showFileNameList():
   extensions = ['.jpg', '.jpeg', '.png', '.gif']
   chooseWorkDir()
   filenames = filter(os.listdir(workdir), extensions)

   lw_files.clear()
   for filename in filenames:
      lw_files.addItem(filename)
   
btn_dir.clicked.connect(showFileNameList)

class ImageProcessor:
   def __init__(self):
      self.image = None
      self.dir = None
      self.filename = None
      self.save_dir = 'Modified/'
   
   def loadimage(self, filename):
      self.filename = filename
      fullname = os.path.join(workdir, filename)
      self.image = Image.open(fullname)
   
   def saveImage(self):
      path = os.path.join(workdir, self.save_dir)
      if not(os.path.exists(path) or os.path.isdir(path)):
         os.mkdir(path)
      fullname = os.path.join(path, self.filename)
      self.image.save(fullname)
   
   def do_bw(self):
      self.image = self.image.convert('L')
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)

   def do_left(self):
      self.image = self.image.transpose(Image.ROTATE_90)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)

   def do_right(self):
      self.image = self.image.transpose(Image.ROTATE_270)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)

   def do_flip(self):
      self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)

   def do_blur(self):
      self.image = self.image.filter(SHARPEN)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)

   def showImage(self, path):
      lb_image.hide()
      pixmapimage = QPixmap(path)
      w,h = lb_image.width(), lb_image.height()
      pixmapimage = pixmapimage.scaled(w,h, Qt.KeepAspectRatio)
      lb_image.setPixmap(pixmapimage)
      lb_image.show()
      
def showshoosenimage():
   if lw_files.currentRow() >= 0:
      filename = lw_files.currentItem().text()
      workimage.loadimage(filename)
      workimage.showImage(os.path.join(workdir, workimage.filename))



workimage =  ImageProcessor()
lw_files.currentRowChanged.connect(showshoosenimage)
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_flip.clicked.connect(workimage.do_flip)
btn_sharp.clicked.connect(workimage.do_blur)


win.show()
app.exec()

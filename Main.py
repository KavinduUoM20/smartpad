from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QFontDialog, QColorDialog
from PyQt6.QtCore import QFileInfo , Qt
from PyQt6.QtGui import QFont
import sys
from Smartpad import Ui_MainWindow
from PyQt6.QtPrintSupport import QPrinter,QPrintDialog,QPrintPreviewDialog

class SmartpadMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.actionSave.triggered.connect(self.saveFile)
        self.actionNew.triggered.connect(self.fileNew)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionPrint.triggered.connect(self.printFile)
        self.actionPrint_Preview.triggered.connect(self.previewDialog)
        self.actionExport_PDF.triggered.connect(self.exportPDF)
        self.actionQuit.triggered.connect(self.quit)

        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionPaste.triggered.connect(self.textEdit.paste)

        self.actionBold.triggered.connect(self.textBold)
        self.actionItalic.triggered.connect(self.textItalic)
        self.actionUnderline.triggered.connect(self.textUnderl)

        self.actionLeft.triggered.connect(self.alignLeft)
        self.actionRight.triggered.connect(self.alignRight)
        self.actionCenter.triggered.connect(self.alignCenter)
        self.actionJustify.triggered.connect(self.alignJustify)

        self.actionFont.triggered.connect(self.fontDialog)
        self.actionColor.triggered.connect(self.colorDialog)
        self.actionAbout_Smartpad.triggered.connect(self.about)

    def maySave(self):
        if not self.textEdit.document().isModified():
            return True
        res = QMessageBox.warning(self, "Application", "The document has been modified.\n Do you want to save changes?",
                                  QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
        if res == QMessageBox.StandardButton.Save:
            return self.saveFile()
        if res == QMessageBox.StandardButton.Cancel:
            return False
        return True

    def saveFile(self):
        filename = QFileDialog.getSaveFileName(self, "Save File")
        if filename[0]:
            f = open(filename[0], 'w')
            with f:
                text = self.textEdit.toPlainText()
                f.write(text)
                QMessageBox.about(self, "Save File", "File has been saved.")

    def fileNew(self):
        if self.maySave():
            self.textEdit.clear()

    def openFile(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File","/home")
        if fileName[0]:
            f=open(fileName[0],'r')
            with f:
                data = f.read()
                self.textEdit.setText(data)

    def printFile(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer)

        if dialog.exec()==QPrintDialog.DialogCode.Accepted:
            self.textEdit.print(printer)

    def previewDialog(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        previewDialog = QPrintPreviewDialog(printer,self)
        previewDialog.paintRequested.connect(self.printPreview)
        previewDialog.exec()

    def printPreview(self,printer):
        self.textEdit.print(printer)

    def exportPDF(self):
        fn, _ =QFileDialog.getSaveFileName(self,'Export PDF',"File.pdf")
        if fn != "":
            if QFileInfo(fn).suffix()== "": fn+='.pdf'
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(fn)
            self.textEdit.document().print(printer)

    def quit(self):
        self.close()

    def textBold(self):
        font=QFont()
        font.setBold(True)
        self.textEdit.setFont(font)

    def textItalic(self):
        font = QFont()
        font.setItalic(True)
        self.textEdit.setFont(font)

    def textUnderl(self):
        font = QFont()
        font.setUnderline(True)
        self.textEdit.setFont(font)

    def alignLeft(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def alignRight(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignRight)

    def alignCenter(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def alignJustify(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignJustify)

    def fontDialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)

    def colorDialog(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextColor(color)

    def about(self):
        QMessageBox.about(self,"About Smartpad", "This is a simple notepad application built with Python.\n Application By: Kavindu Senevirathne")

app = QApplication(sys.argv)
smart = SmartpadMainWindow()
sys.exit(app.exec())

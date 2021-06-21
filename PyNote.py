from PyQt5 import QtCore
from PyQt5.QtCore import QFileInfo, Qt, QRegExp, QSettings
from PyQt5.QtGui import QIcon, QFont, QColor, QTextCharFormat, QSyntaxHighlighter
from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PyQt5.QtWidgets import QAction, QApplication, QDesktopWidget
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QWidget, QFileDialog
from PyQt5.QtWidgets import QStatusBar, QToolBar, QFontDialog, QColorDialog
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QTextEdit, QMenu, QMenuBar
import os
import sys
import runcode

__author__ = "AV"
__version__ = 1.2


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setEnabled(True)
        self.setStyleSheet("")
        self.path = None
        self.settings = QSettings("PyNote", "settings")
        self.setWindowIcon(QIcon("./assets/icon.ico"))

        try:
            self.resize(self.settings.value("size"))
            self.move(self.settings.value("position"))
        except:
            self.resize(1508, 785)
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())
        self.filterTypes = "All files (*.*);; " \
                           "Text Document (*.txt);; " \
                           "Python (*.py);; " \
                           "Markdown (*.md);; " \
                           "Batch file (*.bat;*.cmd;*.nt)"
        self.centralwidget = QWidget(self)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.horizontalLayout = QHBoxLayout(self)
        self.textEdit = QTextEdit(self.centralwidget)
        config = open("config.ini", "r").read()
        if config == "0":
            config2 = open("config.ini", "w")
            font_name = "Ms Shell Dlg 2"
            font_size = 12
            self.textEdit.setFont(QFont(font_name, font_size))
            config2.write("1")
            config2.close()
        else:
            self.textEdit.setFont(QFont(self.settings.value("font")))
        self.textEdit.setAcceptRichText(False)
        self.horizontalLayout.addWidget(self.textEdit)
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 2)
        self.toggle_wrap_text()
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1508, 23))
        self.menuFile = QMenu(self.menubar)
        self.menuEdit = QMenu(self.menubar)
        self.menuFormat = QMenu(self.menubar)
        self.menuHelp = QMenu(self.menubar)
        self.menuRun = QMenu(self.menubar)
        self.menuStyle = QMenu(self.menubar)
        self.menuView = QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.textEdit.cursorPositionChanged.connect(self.CursorPosition)
        self.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(self)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.insertToolBarBreak(self.toolBar)
        self.actionNew = QAction(self)
        self.actionNew.setIcon(QIcon("./assets/new_file.ico"))
        self.actionNew.triggered.connect(self.New)
        self.actionOpen = QAction(self)
        self.actionOpen.setIcon(QIcon("./assets/open.ico"))
        self.actionOpen.triggered.connect(self.openA)
        self.actionVoice = QAction(self)
        self.actionVoice.setIcon(QIcon("./assets/voice.ico"))
        self.actionVoice.triggered.connect(self.VoiceA)
        self.actionSave = QAction(self)
        self.actionSave.setIcon(QIcon("./assets/save.ico"))
        self.actionSave.triggered.connect(self.save_as)
        self.actionPrint = QAction(self)
        self.actionPrint.setIcon(QIcon("./assets/print.ico"))
        self.actionPrint.triggered.connect(self.printA)
        self.actionExit = QAction(self)
        self.actionExit.setIcon(QIcon("./assets/exit.ico"))
        self.actionExit.triggered.connect(self.close)
        self.actionSave_as = QAction(self)
        self.actionSave_as.setIcon(QIcon("./assets/save.ico"))
        self.actionSave_as.triggered.connect(self.file_saveAs)
        self.actionUndo = QAction(self)
        self.actionUndo.setIcon(QIcon("./assets/undo.ico"))
        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo = QAction(self)
        self.actionRedo.setIcon(QIcon("./assets/redo.ico"))
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionCut = QAction(self)
        self.actionCut.setIcon(QIcon("./assets/cut.ico"))
        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionCopy = QAction(self)
        self.actionCopy.setIcon(QIcon("./assets/copy.ico"))
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionPaste = QAction(self)
        self.actionPaste.setIcon(QIcon("./assets/paste.ico"))
        self.actionPaste.triggered.connect(self.textEdit.paste)
        self.actionDelete = QAction(self)
        self.actionDelete.setIcon(QIcon("./assets/delete.ico"))
        self.actionDelete.triggered.connect(self.textEdit.cut)
        self.actionSelect_all = QAction(self)
        self.actionSelect_all.triggered.connect(self.textEdit.selectAll)
        self.actionFont = QAction(self)
        self.actionFont.setIcon(QIcon("./assets/font.ico"))
        self.actionFont.triggered.connect(self.fontA)
        self.actionColor = QAction(self)
        self.actionColor.setIcon(QIcon("./assets/color.ico"))
        self.actionColor.triggered.connect(self.colorA)
        self.actionTheme = QAction(self)
        self.actionTheme.setIcon(QIcon("./assets/theme.ico"))
        self.actionHelp = QAction(self)
        self.actionHelp.setIcon(QIcon("./assets/info.ico"))
        self.actionHelp.triggered.connect(self.about)
        self.actionBold = QAction(self)
        self.actionBold.setIcon(QIcon("./assets/bold.ico"))
        self.actionBold.triggered.connect(self.Bold)
        self.actionItalic = QAction(self)
        self.actionItalic.setIcon(QIcon("./assets/italic.ico"))
        self.actionItalic.triggered.connect(self.Italic)
        self.actionExport_as_pdf = QAction(self)
        self.actionExport_as_pdf.setIcon(QIcon("./assets/export_as pdf.ico"))
        self.actionExport_as_pdf.triggered.connect(self.export_as_pdf)
        self.actionWrap = QAction(self)
        self.actionWrap.setIcon(QIcon("./assets/wrap.ico"))
        self.actionWrap.triggered.connect(self.toggle_wrap_text)
        self.actionunderline = QAction(self)
        self.actionunderline.setIcon(QIcon("./assets/underline.ico"))
        self.actionunderline.triggered.connect(self.Underline)
        self.actionPrint_Preview = QAction(self)
        self.actionPrint_Preview.setIcon(QIcon("./assets/print_preview.ico"))
        self.actionPrint_Preview.triggered.connect(self.print_preview)
        self.actionLeft = QAction(self)
        self.actionLeft.setIcon(QIcon("./assets/left.ico"))
        self.actionLeft.triggered.connect(self.Left)
        self.actionCenter = QAction(self)
        self.actionCenter.setIcon(QIcon("./assets/center.ico"))
        self.actionCenter.triggered.connect(self.Center)
        self.actionRight = QAction(self)
        self.actionRight.setIcon(QIcon("./assets/right.ico"))
        self.actionRight.triggered.connect(self.Right)
        self.actionRun = QAction(self)
        self.actionRun.setIcon(QIcon("./assets/run.ico"))
        self.actionRun.triggered.connect(self.run_script)
        self.actionjustify = QAction(self)
        self.actionjustify.setIcon(QIcon("./assets/center.ico"))
        self.actionjustify.triggered.connect(self.Justify)
        self.actionZoom_In = QAction(self)
        self.actionZoom_In.setIcon(QIcon("./assets/zoom_in.ico"))
        self.actionZoom_In.triggered.connect(self.textEdit.zoomIn)
        self.actionZoom_Out = QAction(self)
        self.actionZoom_Out.setIcon(QIcon("./assets/zoom_out.ico"))
        self.actionZoom_Out.triggered.connect(self.textEdit.zoomOut)
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addAction(self.actionExport_as_pdf)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addAction(self.actionPrint_Preview)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionSelect_all)
        self.menuEdit.addAction(self.actionDelete)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionVoice)
        self.menuFormat.addAction(self.actionFont)
        self.menuFormat.addAction(self.actionColor)
        self.menuFormat.addSeparator()
        self.menuFormat.addAction(self.actionWrap)
        self.menuHelp.addAction(self.actionHelp)
        self.menuStyle.addAction(self.actionBold)
        self.menuStyle.addAction(self.actionItalic)
        self.menuStyle.addAction(self.actionunderline)
        self.menuStyle.addSeparator()
        self.menuStyle.addAction(self.actionLeft)
        self.menuStyle.addAction(self.actionCenter)
        self.menuStyle.addAction(self.actionRight)
        self.menuStyle.addAction(self.actionjustify)
        self.menuStyle.addSeparator()
        self.menuStyle.addAction(self.actionTheme)
        self.menuView.addAction(self.actionZoom_In)
        self.menuView.addAction(self.actionZoom_Out)
        self.menuRun.addAction(self.actionRun)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuFormat.menuAction())
        self.menubar.addAction(self.menuStyle.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("PyNote", "PyNote"))
        self.menuFile.setTitle(_translate("PyNote", "File"))
        self.menuEdit.setTitle(_translate("PyNote", "Edit"))
        self.menuFormat.setTitle(_translate("PyNote", "Format"))
        self.menuHelp.setTitle(_translate("PyNote", "About"))
        self.menuRun.setTitle(_translate("PyNote", "Run"))
        self.menuStyle.setTitle(_translate("PyNote", "Style"))
        self.menuView.setTitle(_translate("PyNote", "View"))
        self.toolBar.setWindowTitle(_translate("PyNote", "toolBar"))
        self.actionNew.setText(_translate("PyNote", "New"))
        self.actionNew.setShortcut(_translate("PyNote", "Ctrl+N"))
        self.actionOpen.setText(_translate("PyNote", "Open"))
        self.actionOpen.setShortcut(_translate("PyNote", "Ctrl+O"))
        self.actionVoice.setText(_translate("PyNote", "Voice Recognition"))
        self.actionVoice.setShortcut(_translate("PyNote", "Ctrl+Shift+V"))
        self.actionSave.setText(_translate("PyNote", "Save"))
        self.actionSave.setShortcut(_translate("PyNote", "Ctrl+S"))
        self.actionPrint.setText(_translate("PyNote", "Print"))
        self.actionPrint.setShortcut(_translate("PyNote", "Ctrl+P"))
        self.actionExit.setText(_translate("PyNote", "Exit"))
        self.actionExit.setShortcut(_translate("PyNote", "Ctrl+W"))
        self.actionSave_as.setText(_translate("PyNote", "Save As..."))
        self.actionSave_as.setShortcut(_translate("PyNote", "Ctrl+Shift+S"))
        self.actionUndo.setText(_translate("PyNote", "Undo"))
        self.actionUndo.setShortcut(_translate("PyNote", "Ctrl+Z"))
        self.actionRedo.setText(_translate("PyNote", "Redo"))
        self.actionRedo.setShortcut(_translate("PyNote", "Ctrl+Y"))
        self.actionCut.setText(_translate("PyNote", "Cut"))
        self.actionCut.setShortcut(_translate("PyNote", "Ctrl+X"))
        self.actionCopy.setText(_translate("PyNote", "Copy"))
        self.actionCopy.setShortcut(_translate("PyNote", "Ctrl+C"))
        self.actionPaste.setText(_translate("PyNote", "Paste"))
        self.actionPaste.setShortcut(_translate("PyNote", "Ctrl+V"))
        self.actionDelete.setText(_translate("PyNote", "Delete"))
        self.actionDelete.setShortcut(_translate("PyNote", "Del"))
        self.actionSelect_all.setText(_translate("PyNote", "Select all"))
        self.actionSelect_all.setShortcut(_translate("PyNote", "Ctrl+A"))
        self.actionFont.setText(_translate("PyNote", "Font"))
        self.actionFont.setShortcut(_translate("PyNote", "Ctrl+F"))
        self.actionColor.setText(_translate("PyNote", "Color"))
        self.actionColor.setShortcut(_translate("PyNote", "Ctrl+E"))
        self.actionTheme.setText(_translate("PyNote", "Theme"))
        self.actionHelp.setText(_translate("PyNote", "About"))
        self.actionHelp.setShortcut(_translate("PyNote", "Ctrl+,"))
        self.actionBold.setText(_translate("PyNote", "Bold"))
        self.actionBold.setShortcut(_translate("PyNote", "Ctrl+G"))
        self.actionItalic.setText(_translate("PyNote", "Italic"))
        self.actionItalic.setShortcut(_translate("PyNote", "Ctrl+I"))
        self.actionExport_as_pdf.setText(_translate("PyNote", "Export as pdf"))
        self.actionExport_as_pdf.setShortcut(_translate("PyNote", "Ctrl+Shift+E"))
        self.actionWrap.setText(_translate("PyNote", "Word Wrap"))
        self.actionunderline.setText(_translate("PyNote", "Underline"))
        self.actionunderline.setShortcut(_translate("PyNote", "Ctrl+U"))
        self.actionPrint_Preview.setText(_translate("PyNote", "Print Preview"))
        self.actionPrint_Preview.setShortcut(_translate("PyNote", "Ctrl+Shift+P"))
        self.actionLeft.setText(_translate("PyNote", "Left"))
        self.actionCenter.setText(_translate("PyNote", "Center"))
        self.actionRight.setText(_translate("PyNote", "Right"))
        self.actionRun.setText(_translate("PyNote", "Run module"))
        self.actionRun.setShortcut(_translate("PyNote", "F5"))
        self.actionjustify.setText(_translate("PyNote", "Justify"))
        self.actionZoom_In.setText(_translate("PyNote", "Zoom In"))
        self.actionZoom_In.setShortcut(_translate("PyNote", "Ctrl++"))
        self.actionZoom_Out.setText(_translate("PyNote", "Zoom Out"))
        self.actionZoom_Out.setShortcut(_translate("PyNote", "Ctrl+-"))
        self.toolBar.addAction(self.actionRun)
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionExport_as_pdf)
        self.toolBar.addAction(self.actionPrint)
        self.toolBar.addAction(self.actionUndo)
        self.toolBar.addAction(self.actionRedo)
        self.toolBar.addAction(self.actionCopy)
        self.toolBar.addAction(self.actionPaste)
        self.toolBar.addAction(self.actionVoice)
        self.toolBar.addAction(self.actionZoom_In)
        self.toolBar.addAction(self.actionZoom_Out)
        self.toolBar.addAction(self.actionColor)
        self.toolBar.addAction(self.actionFont)
        self.toolBar.addAction(self.actionBold)
        self.toolBar.addAction(self.actionItalic)
        self.toolBar.addAction(self.actionunderline)
        self.toolBar.addAction(self.actionRight)
        self.toolBar.addAction(self.actionLeft)
        self.toolBar.addAction(self.actionCenter)
        self.toolBar.addAction(self.actionHelp)
        self.toolBar.addAction(self.actionExit)
        self.toolBar.setMovable(True)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.textEdit.setStyleSheet("QTextEdit{"
                                    "background-color: #ffffff;"
                                    "color: #000000;"
                                    "}"
                                    "QTextEdit{"
                                    "border: 1px;"
                                    "}")
        QtCore.QMetaObject.connectSlotsByName(self)
        self.statusbar.showMessage("Line: 0 | Column:0")
        self.update_title()
        self.show()

    def VoiceA(self):
        message = QMessageBox.warning(self, "Voice recognition beta",
                                      "Warning, voice recognition is in beta, it might not work,\n"
                                      "Do you want to continue?",
                                      QMessageBox.Ok | QMessageBox.Cancel)

    def CursorPosition(self):
        line = self.textEdit.textCursor().blockNumber()
        col = self.textEdit.textCursor().columnNumber()
        linecol = ("Line: " + str(line) + " | " + "Column: " + str(col))
        self.statusbar.showMessage(linecol)

    def Highlighter_py(self):
        e = []
        if self.path is not None:
            for i in self.path:
                e.append(i)
            if e[-1] == "y":
                if e[-2] == "p":
                    if e[-3] == ".":
                        self.highlighter = Highlighter(self.textEdit.document())
            else:
                pass
        else:
            pass

    def Highlighter_java(self):
        e = []
        if self.path is not None:
            for i in self.path:
                e.append(i)
            if e[-1] == "a":
                if e[-2] == "v":
                    if e[-3] == "a":
                        if e[-4] == "j":
                            if e[-5] == ".":
                                self.highlighter = Highlighter2(self.textEdit.document())
            else:
                pass
        else:
            pass

    def about(self):
        message = QMessageBox.about(self, "About", "PyNote is a simple text editor wrote in python!")

    def Bold(self):
        if self.textEdit.fontWeight() == QFont.Bold:
            self.textEdit.setFontWeight(QFont.Normal)
        else:
            self.textEdit.setFontWeight(QFont.Bold)

    def Italic(self):
        state = self.textEdit.fontItalic()
        self.textEdit.setFontItalic(not state)

    def Underline(self):
        state = self.textEdit.fontUnderline()
        self.textEdit.setFontUnderline(not state)

    def Left(self):
        self.textEdit.setAlignment(Qt.AlignLeft)

    def Right(self):
        self.textEdit.setAlignment(Qt.AlignRight)

    def Center(self):
        self.textEdit.setAlignment(Qt.AlignCenter)

    def Justify(self):
        self.textEdit.setAlignment(Qt.AlignJustify)

    def New(self):
        if self.textEdit.document().isModified():
            message = QMessageBox.question(self, "Save file", "Save file \"{}\"?".format(
                os.path.basename(self.path) if self.path else "New file"),
                                           QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if message == QMessageBox.Yes:
                self.save_as()
                if self.path is not None:
                    self.path = None
                    self.update_title()
                    self.textEdit.clear()
            elif message == QMessageBox.No:
                self.path = None
                self.update_title()
                self.textEdit.clear()
            else:
                pass
        else:
            self.path = None
            self.update_title()
            self.textEdit.clear()

    def fontA(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)

    def save_as(self):
        if self.path is None:
            self.file_saveAs()
        else:
            try:
                text = self.textEdit.toPlainText()
                with open(self.path, "w") as f:
                    f.write(text)
                    f.close()
                    self.update_title()
            except Exception as e:
                self.dialog_message(str(e))

    def file_saveAs(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save file as",
            "",
            "Text Document (*.txt);;All files (*.*);;  Python (*.py);; Markdown (*.md);; Batch file (*.bat;*.cmd;*.nt)"
        )
        text = self.textEdit.toPlainText()
        if not path:
            return
        else:
            try:
                with open(path, "w") as f:
                    f.write(text)
                    f.close()
                    self.update_title()
                    self.Highlighter_py()
                    self.Highlighter_java()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path
                self.update_title()
                self.Highlighter_py()
                self.Highlighter_java()

    def export_as_pdf(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Export as pdf", None, "PDF file (*.pdf)")
        if QFileInfo(fn).suffix() == "": fn += ".pdf"
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(fn)
        self.textEdit.document().print_(printer)

    def run_script(self):
        e = []
        if self.path is not None:
            for i in self.path:
                e.append(i)
            if e[-1] == "y":
                if e[-2] == "p":
                    if e[-3] == ".":
                        e = os.path.basename(self.path).split(".")
                        py = str(e[0]) + ".py"
                        runcode.run(self.path)
            else:
                # il file non è .py, quindi chiedere se salvare come {titolo}.py
                e = os.path.basename(self.path).split(".")
                py = str(e[0]) + ".py"
                message = QMessageBox.question(self, "Save as python file?",
                                               "The current document is not a python file,\n"
                                               "OK to save as \"{}\" and run".format(
                                                   py),
                                               QMessageBox.Ok | QMessageBox.Cancel)
                if message == QMessageBox.Ok:
                    try:
                        if self.textEdit.document().isModified():
                            self.save_as()
                        else:
                            pass
                        self.setWindowTitle("{0} - PyNote".format(py))
                        try:
                            text = self.textEdit.toPlainText()
                            split_dir = str(self.path).split(".")
                            self.path = split_dir[0] + ".py"
                            with open(self.path, "w") as f:
                                f.write(text)
                                f.close()
                                self.update_title()
                                self.Highlighter_py()
                                self.Highlighter_java()
                            runcode.run(self.path)
                        except Exception as e:
                            self.dialog_message(str(e))

                    except:
                        pass
                else:
                    pass
        else:
            # il file non è stato salvato
            # prima di essere eseguito deve essere salvato e mostrare il file dialog con solo estensione .py
            message = QMessageBox.question(self, "Save before run?", "Source must be saved, OK to save?",
                                           QMessageBox.Ok | QMessageBox.Cancel)
            if message == QMessageBox.Ok:
                try:
                    path, _ = QFileDialog.getSaveFileName(self, "Save python file", None, "Python file (*.py)")
                    text = self.textEdit.toPlainText()
                    if not path:
                        return
                    else:
                        try:
                            with open(path, "w") as f:
                                f.write(text)
                                f.close()
                                self.update_title()
                                self.Highlighter_py()
                                self.Highlighter_java()
                        except Exception as e:
                            self.dialog_message(str(e))
                        else:
                            self.path = path
                            self.update_title()
                            self.Highlighter_py()
                            self.Highlighter_java()
                    runcode.run(self.path)
                except:
                    pass

    def printA(self):
        try:
            printer = QPrinter(QPrinter.HighResolution)
            print_p = QPrintPreviewDialog(printer, self)
            print_p.paintRequested.connect(self.print_preview)
        except:
            message = QMessageBox.critical(self, "Error", "No printer detected!",
                                           QMessageBox.Ok)

    def print_preview(self, printer):
        try:
            self.textEdit.print_(printer)
        except:
            message = QMessageBox.critical(self, "Error", "No printer detected!",
                                           QMessageBox.Ok)

    def colorA(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextColor(color)

    def savePosAndSize(self):
        self.settings.setValue("size", self.size())
        self.settings.setValue("position", self.pos())
        self.settings.setValue("font", self.textEdit.font())

    def close(self):
        if self.textEdit.document().isModified():
            choice = QMessageBox.question(self, "Save file", "Save file \"{}\"?".format(
                os.path.basename(self.path) if self.path else "New file"),
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if choice == QMessageBox.No:
                self.savePosAndSize()
                sys.exit()
            elif choice == QMessageBox.Yes:
                self.savePosAndSize()
                self.save_as()
                if self.path is not None:
                    sys.exit()
            else:
                pass
        else:
            self.savePosAndSize()
            sys.exit()

    def closeEvent(self, event):
        if self.textEdit.document().isModified():
            choice = QMessageBox.question(self, "Save file", "Save file \"{}\"?".format(
                os.path.basename(self.path) if self.path else "New file"),
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if choice == QMessageBox.No:
                self.savePosAndSize()
                event.accept()
            elif choice == QMessageBox.Yes:
                self.savePosAndSize()
                self.save_as()
                if self.path is not None:
                    print("er path è specificato!")
                    event.accept()
                else:
                    event.ignore()
            else:
                event.ignore()
        else:
            self.savePosAndSize()
            event.accept()

    def openA(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Open file",
            directory="",
            filter=self.filterTypes
        )
        if path:
            try:
                with open(path, "r") as f:
                    text = f.read()
                    f.close()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path
                self.textEdit.setText(text)
                self.update_title()
        self.Highlighter_py()
        self.Highlighter_java()
        print(path)

    def dialog_message(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def update_title(self):
        self.setWindowTitle("{0} - PyNote".format(os.path.basename(self.path) if self.path else "New file"))

    def toggle_wrap_text(self):
        self.textEdit.setLineWrapMode(not self.textEdit.lineWrapMode())


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        """
        quotationColor = "rgb(195,232,141)"
        classfunctionColor = "rgb(255,203,107)"
        keywordColor = "rgb(183,146,234)"
        functionColor = "rgb(137,215,217)"
        commentColor = "rgb(247,118,105)"
        """

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(227, 113, 0))
        keywordPatterns = ["\\bFalse\\b", "\\bNone\\b", "\\bTrue\\b", "\\band\\b", "\\bas\\b",
                           "\\bassert\\b", "\\bbreak\\b", "\\bcontinue\\b", "\\b__author__\\b", "\\b__version__\\b",
                           "\\bdel\\b", "\\belif\\b", "\\belse\\b", "\\bexcept\\b", "\\bfinally\\b",
                           "\\bfor\\b", "\\bfrom\\b", "\\bglobal\\b", "\\bif\\b", "\\bimport\\b", "\\bself\\b",
                           "\\bin\\b", "\\bis\\b", "\\blambda\\b", "\\bnonlocal\\b", "\\bnot\\b", "\\bsuper\\b",
                           "\\bor\\b", "\\bpass\\b", "\\braise\\b", "\\breturn\\b", "\\btry\\b", "\\b__init__\\b",
                           "\\bwhile\\b", "\\bwith\\b", "\\byield\\b", "\\bclass\s[A-Za-z_]+\\b"]
        self.highlightingRules = [(QRegExp(pattern), keywordFormat)
                                  for pattern in keywordPatterns]
        classRegExp = "\\bself\\b"
        classFormat = QTextCharFormat()
        classFormat.setForeground(QColor(178, 28, 179))
        self.highlightingRules.append((QRegExp(classRegExp), classFormat))

        printRegExp = "\\print\\b"
        printFormat = QTextCharFormat()
        printFormat.setForeground(QColor(178, 28, 179))
        self.highlightingRules.append((QRegExp(printRegExp), printFormat))

        defRegExp = "\\bdef\s[A-Za-z_]+\\b"
        defFormat = QTextCharFormat()
        defFormat.setForeground(QColor(0, 218, 220))
        self.highlightingRules.append((QRegExp(defRegExp), defFormat))

        singleLineCommentExp = "#[^\n]*"
        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setFontItalic(True)
        singleLineCommentFormat.setForeground(QColor(197, 19, 19))
        self.highlightingRules.append((QRegExp(singleLineCommentExp), singleLineCommentFormat))

        decorators = "@[^\n]*"
        decoratorsFor = QTextCharFormat()
        decoratorsFor.setFontItalic(True)
        decoratorsFor.setForeground(QColor(197, 19, 19))
        self.highlightingRules.append((QRegExp(decorators), decoratorsFor))

        quotationExp = "\".*\""
        quotation2Exp = "\".*\""

        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(QColor(105, 178, 0))
        self.highlightingRules.append((QRegExp(quotationExp), quotationFormat))
        self.highlightingRules.append((QRegExp(quotation2Exp), quotationFormat))

        functionExp = "\\[A-Za-z0-9_]+(?=\\()"
        functionFormat = QTextCharFormat()
        functionFormat.setForeground(QColor(39, 204, 208))
        self.highlightingRules.append((QRegExp(functionExp), functionFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)


class Highlighter2(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter2, self).__init__(parent)
        """
        quotationColor = "rgb(195,232,141)"
        classfunctionColor = "rgb(255,203,107)"
        keywordColor = "rgb(183,146,234)"
        functionColor = "rgb(137,215,217)"
        commentColor = "rgb(247,118,105)"
        """

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(227, 113, 0))
        keywordPatterns = ["\\bfalse\\b", "\\bnull\\b", "\\btrue\\b", "\\bfinal\\b", "\\bout\\b", "\\bimplements\\",
                           "\\bvoid\\b", "\\bbreak\\b", "\\bcontinue\\b", "\\bint\\b", "\\bstatic\\b", "\\bextends\\",
                           "\\bpublic\\b", "\\belse\\b", "\\bexcept\\b", "\\bdouble\\b", "\\binterface\\b",
                           "\\bfor\\b", "\\bfrom\\b", "\\bglobal\\b", "\\bif\\b", "\\bimport\\b", "\\bself\\b",
                           "\\bin\\b", "\\blambda\\b", "\\bfloat\\b", "\\bnot\\b", "\\bsuper\\b", "\\bbyte\\b",
                           "\\bString\\b", "\\bpass\\b", "\\breturn\\b", "\\btry\\b", "\\bin\\b", "\\bnew\\",
                           "\\bwhile\\b", "\\bwith\\b", "\\bclass\\b"]
        self.highlightingRules = [(QRegExp(pattern), keywordFormat)
                                  for pattern in keywordPatterns]
        classRegExp = "\\bthis\\b"
        classFormat = QTextCharFormat()
        classFormat.setForeground(QColor(178, 28, 179))
        self.highlightingRules.append((QRegExp(classRegExp), classFormat))

        printRegExp = "\\bprint\\b"
        printFormat = QTextCharFormat()
        printFormat.setForeground(QColor(178, 28, 179))
        self.highlightingRules.append((QRegExp(printRegExp), printFormat))

        printlnRegExp = "\\bprintln\\b"
        printlnFormat = QTextCharFormat()
        printlnFormat.setForeground(QColor(178, 28, 179))
        self.highlightingRules.append((QRegExp(printlnRegExp), printlnFormat))

        systemRegExp = "\\bSystem\\b"
        systemFormat = QTextCharFormat()
        systemFormat.setForeground(QColor(178, 28, 179))
        self.highlightingRules.append((QRegExp(systemRegExp), systemFormat))

        singleLineCommentExp = "//[^\n]*"
        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setFontItalic(True)
        singleLineCommentFormat.setForeground(QColor(197, 19, 19))
        self.highlightingRules.append((QRegExp(singleLineCommentExp), singleLineCommentFormat))

        decorators = "@[^\n]*"
        decoratorsFor = QTextCharFormat()
        decoratorsFor.setFontItalic(True)
        decoratorsFor.setForeground(QColor(197, 19, 19))
        self.highlightingRules.append((QRegExp(decorators), decoratorsFor))

        quotationExp = "\".*\""
        quotation2Exp = "\".*\""

        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(QColor(105, 178, 0))
        self.highlightingRules.append((QRegExp(quotationExp), quotationFormat))
        self.highlightingRules.append((QRegExp(quotation2Exp), quotationFormat))

        functionExp = "\\[A-Za-z0-9_]+(?=\\()"
        functionFormat = QTextCharFormat()
        functionFormat.setForeground(QColor(39, 204, 208))
        self.highlightingRules.append((QRegExp(functionExp), functionFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())

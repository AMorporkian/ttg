import sys
import re
import random
import requests

from PySide.QtCore import QTimer
from PySide.QtGui import QTableWidgetItem, QErrorMessage, QIntValidator
from PySide import QtCore, QtGui

def get_top_level_comments(thread_id):
    r = requests.get('http://reddit.com/comments/{}/.json?sort=old'.format(thread_id))
    #print(r.json())
    comments = [x['data']['body'] for x in r.json()[1]['data']['children']]
    return comments
    
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(650, 592)
        self.gridLayoutWidget = QtGui.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 9, 631, 571))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.plain_text = QtGui.QPlainTextEdit(self.gridLayoutWidget)
        self.plain_text.setObjectName("plain_text")
        self.gridLayout.addWidget(self.plain_text, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.markdown = QtGui.QPlainTextEdit(self.gridLayoutWidget)
        self.markdown.setObjectName("markdown")
        self.gridLayout.addWidget(self.markdown, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(
            QtGui.QApplication.translate("Dialog", "Teams", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(
            QtGui.QApplication.translate("Dialog", "Plain Text", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.label.setText(
            QtGui.QApplication.translate("Dialog", "Reddit Markdown", None,
                                         QtGui.QApplication.UnicodeUTF8))


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Tagpro Tournament Generator")
        MainWindow.resize(418, 384)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 0, 371, 91))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(
            QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.thread_id_edit = QtGui.QLineEdit(self.formLayoutWidget)
        self.thread_id_edit.setText("")
        self.thread_id_edit.setObjectName("thread_id")
        self.thread_id_edit.setMaxLength(6)
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
                                  self.thread_id_edit)
        self.label2 = QtGui.QLabel(self.formLayoutWidget)
        self.label2.setObjectName("label2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label2)
        self.max_teams_edit = QtGui.QLineEdit(self.formLayoutWidget)
        self.max_teams_edit.setText("")
        self.max_teams_edit.setObjectName("max_teams")
        self.max_teams_edit.setMaxLength(4)
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
                                  self.max_teams_edit)

        self.begin_button = QtGui.QCommandLinkButton(
            self.formLayoutWidget)
        self.begin_button.setObjectName("begin_button")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
                                  self.begin_button)
        self.table = QtGui.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(20, 100, 371, 195))
        self.table.setObjectName("textBrowser")
        self.generate_button = QtGui.QPushButton(self.centralwidget)
        self.generate_button.setGeometry(QtCore.QRect(240, 295, 151, 27))
        self.generate_button.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 418, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.timer = QTimer()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QtGui.QApplication.translate("MainWindow",
                                         "Tagpro Tournament Generator", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.label.setText(
            QtGui.QApplication.translate("MainWindow", "Thread ID", None,
                                         QtGui.QApplication.UnicodeUTF8))

        self.label2.setText(
            QtGui.QApplication.translate("MainWindow", "Max Teams (Optional)",
                                         None,
                                         QtGui.QApplication.UnicodeUTF8))

        self.begin_button.setText(
            QtGui.QApplication.translate("MainWindow", "Begin", None,
                                         QtGui.QApplication.UnicodeUTF8))

        self.generate_button.setText(
            QtGui.QApplication.translate("MainWindow", "Generate Teams", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(
            QtGui.QApplication.translate("MainWindow", "File", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(
            QtGui.QApplication.translate("MainWindow", "toolBar", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(
            QtGui.QApplication.translate("MainWindow", "Quit", None,
                                         QtGui.QApplication.UnicodeUTF8))

    def add_signals(self):
        self.begin_button.clicked.connect(self.begin)
        self.generate_button.clicked.connect(self.generate_teams)
        self.generate_button.setDisabled(True)
        self.begin_button.setDisabled(True)
        self.thread_id_edit.textChanged.connect(self.check_length)
        v = QIntValidator(0, 999)
        self.max_teams_edit.setValidator(v)

    def begin(self):
        thread_id = self.thread_id_edit.text()
        max_teams = self.max_teams_edit.text()
        if max_teams == "":
            max_teams = 65535
        else:
            max_teams = int(max_teams)

        try:
            self.thread_id_edit.setDisabled(True)
            self.begin_button.setDisabled(True)
            try:
                self.roles = self.extract(thread_id, max_teams)
            except TypeError:
                return
            except Exception as e:
                s = QErrorMessage(self.centralwidget)
                s.showMessage("Unknown error encountered.\n" + str(e))
                return

            self.table.clearContents()
            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels(["Name", "Position"])
            self.table.setRowCount(
                len(self.roles['o']) + len(self.roles['d']) + len(
                    self.roles['do']) + len(self.roles['od']))
            self.table.horizontalHeader().setStretchLastSection(True)
            s = 0
            for p in self.roles['o']:
                n = QTableWidgetItem(p)
                r = QTableWidgetItem('Offense')
                self.table.setItem(s, 0, n)
                self.table.setItem(s, 1, r)
                s += 1
            for p in self.roles['d']:
                n = QTableWidgetItem(p)
                r = QTableWidgetItem('Defense')
                self.table.setItem(s, 0, n)
                self.table.setItem(s, 1, r)
                s += 1
            for p in self.roles['od']:
                n = QTableWidgetItem(p)
                r = QTableWidgetItem('Offense/Defense')
                self.table.setItem(s, 0, n)
                self.table.setItem(s, 1, r)
                s += 1
            for p in self.roles['do']:
                n = QTableWidgetItem(p)
                r = QTableWidgetItem('Defense/Offense')
                self.table.setItem(s, 0, n)
                self.table.setItem(s, 1, r)
                s += 1
            if s >= 1:
                self.generate_button.setEnabled(True)
        finally:
            self.begin_button.setEnabled(True)
            self.thread_id_edit.setEnabled(True)

    def generate_teams(self):
        s = DialogWindow(self.centralwidget)
        teams, leftover = self._generate()
        s.ui.markdown.setPlainText(self._generate_markdown(teams, leftover))
        s.ui.plain_text.setPlainText(self._generate_plaintext(teams, leftover))
        s.show()

    def extract(self, thread_id, max=65535):
        pattern = re.compile('[\W_|\_|\-|\.]+')
        fix = re.compile(r'(D / O)')
        fix2 = re.compile(r'(O / D)')
        defense = set()
        offense = set()
        do = set()
        od = set()
        unknown = []
        self.statusbar.showMessage("Attempting to retrieve submission {}.".format(thread_id))
        comments = get_top_level_comments(thread_id)
        self.statusbar.showMessage(
            "Submission {} retrieved".format(thread_id))
        c = 0
        for i, comment in enumerate(comments):
            if (len(offense) + len(defense) + len(do) + len(od)) / 4 >= max:
                break
            self.statusbar.showMessage(
                "Processing comment {}/{}".format(i, len(comments)))
            if comment.lower().rstrip() == "[deleted]":
                continue
            else:
                try:
                    nc = comment.split(":")
                    name = nc[0]
                    position = nc[1].lstrip().rstrip()
                except IndexError:
                    continue

                if position.lower() not in ['d', 'o', 'd/o', 'o/d']:
                    continue
                if position.lower() == 'd':
                    defense.add(name)

                elif position.lower() == 'o':
                    offense.add(name)

                elif position.lower() == 'd/o':
                    do.add(name)

                elif position.lower() == 'o/d':
                    od.add(name)

        self.statusbar.showMessage("{} total players parsed.".format(
            len(offense) + len(defense) + len(do) + len(od)))
        return {"o": offense,
                "d": defense,
                "do": do,
                "od": od}

    def check_length(self):
        if len(self.thread_id_edit.text()) != 6:
            self.begin_button.setDisabled(True)
        else:
            self.begin_button.setEnabled(True)

    def _generate(self):
        d = list(self.roles['d'])
        o = list(self.roles['o'])
        do = list(self.roles['do'])
        od = list(self.roles['od'])

        random.shuffle(d)
        random.shuffle(o)
        random.shuffle(do)
        random.shuffle(od)

        leftover = []
        teams = []

        def get_defense():
            if len(d) > 0:
                return d.pop()
            elif len(do) > 0:
                return do.pop()
            elif len(od) > 0:
                return od.pop()
            else:
                p = o.pop()
                return p

        def get_offense():
            if len(o) > 0:
                return o.pop()
            elif len(od) > 0:
                return od.pop()
            elif len(do) > 0:
                return do.pop()
            else:
                p = d.pop()
                return p

        while True:
            total = len(d) + len(o) + len(do) + len(od)
            if 4 > total > 0:
                leftover = o + d + od + do
                break
            if total == 0:
                break
            team = []
            for _ in range(2):
                team.append(get_defense() + ", Defense")
            for _ in range(2):
                team.append(get_offense() + ", Offense")
            teams.append(team)
        return teams, leftover

    def _generate_markdown(self, teams, leftover):
        s = "##Teams\n----"
        for i, team in enumerate(teams):
            s += "\n\n#Team {}\n".format(i + 1)
            for p in team:
                s += "* {}\n".format(p)
        if len(leftover) > 0:
            s += "\nSubstitute Players\n\n"
            for r in leftover:
                s += "\n* {}".format(r)
        return s

    def _generate_plaintext(self, teams, leftover):
        s = "Teams"
        for i, team in enumerate(teams):
            s += "\n\nTeam {}\n".format(i + 1)
            for p in team:
                s += "* {}\n".format(p)
        if len(leftover) > 0:
            s += "\nSubstitute Players\n"
            for r in leftover:
                s += "\n* {}".format(r)
        return s


class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.add_signals()


class DialogWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        super(DialogWindow, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())

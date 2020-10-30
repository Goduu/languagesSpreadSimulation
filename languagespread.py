#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
import getopt

from LanguageBoard import LanguageBoard

DEFAULT_BOARD_SIZE = 50
DEFAULT_TOUR = 5
STATE = {
    "SUSCEPTIBLE": 0,
    "LEARNING": 1,
    "LEARNED": 2
}

STATE_NAME = [ ("Susceptible", "Susceptible"), ("En Aprendisage", "Learning"),
               ("Apris", "Learned")]

STATUS_PLAYING = 1
STATUS_STOPPED = 0

IMMUNITY_RATE_PARAM = 0
CLUSTER_NB_PARAM = 1
TRANSMISSION_RATE_PARAM = 2
MORTALITY_RATE_PARAM = 3
MORTALITY_DELAY_PARAM = 4
CONTAGION_DELAY_PARAM = 5
QUARANTINE_RATE_PARAM = 6
DIAGNOSIS_DELAY_PARAM = 7
HOSPITALIZED_RATE_PARAM = 8
HOSPITALIZED_DELAY_PARAM = 9
SOCIALDISTANCING_RATE_PARAM = 10
SOCIALDISTANCING_DELAY_PARAM = 11

CONF_ELEMENTS = {
    IMMUNITY_RATE_PARAM: (("Tx Immunité", "Immunity Rate"), "double"),
    CLUSTER_NB_PARAM: (("Nb cluster", "Cluster Nbr"), "int"),
    TRANSMISSION_RATE_PARAM: (("Tx contagion", "Contagion Rate"), "double"),
    MORTALITY_RATE_PARAM: (("Tx mortalité", "Death Rate"), "double"),
    MORTALITY_DELAY_PARAM: (("Délai mortalité", "Death Delay"), "int"),
    CONTAGION_DELAY_PARAM: (("Délai contagion", "Contagion Delay"), "int"),
    QUARANTINE_RATE_PARAM: (("Tx diag / mise quarantaine", "Diagnosis / Quarantine Rate"), "double"),
    HOSPITALIZED_RATE_PARAM: (("Tx hospitalisation", "Hospitalization Rate"), "int"),
    HOSPITALIZED_DELAY_PARAM: (("Délai hospitalisation", "Hospitalization Delay"), "int"),
    DIAGNOSIS_DELAY_PARAM: (("Délai diagnostic", "Diagnosis Delay"), "int"),
    SOCIALDISTANCING_RATE_PARAM: (("Taux post soc. dist", "Post soc. dist rate"), "double"),
    SOCIALDISTANCING_DELAY_PARAM: (("Délai pour soc. dist", "Soc. dist delay"), "int")
}

LANG_FR = 0
LANG_US = 1

RED_PLOT = 0
GREEN_PLOT = 1
BLUE_PLOT = 2
PLOT_NB = 3

class Pos(QWidget):
    expandable = pyqtSignal(int, int)
    clicked = pyqtSignal()
    ohno = pyqtSignal()

    # stores floating label list, as we might miss some leaveEvent, we need a way to hide them all
    activeLabelList = []

    def __init__(self, x, y, lang, *args, **kwargs):
        super(Pos, self).__init__(*args, **kwargs)

        self.setFixedSize(QSize(10, 10))

        self.x = x
        self.y = y
        self.lang = lang

        self.floatingLabel = QLabel()
        self.floatingLabel.setWindowFlags(Qt.FramelessWindowHint)
        self.floatingLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def redraw(self, state,r,g,b):
        self._state = state
        self._rgb = []
        self._rgb.append(r)
        self._rgb.append(g)
        self._rgb.append(b)
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        
        r = event.rect()
        if self._state == STATE["SUSCEPTIBLE"]:
            blueColor = QColor(210,210,255)
            outer, inner = blueColor, blueColor
        # elif self._state == STATE["LEARNED"]:
        #     outer, inner = Qt.darkRed, Qt.red
        elif self._state == STATE["LEARNING"] or self._state == STATE["LEARNED"]:
            # outer, inner = Qt.black, Qt.black
            # print(self._rgb[0],self._rgb[1],self._rgb[2])
            outer, inner = Qt.black, QColor(self._rgb[0],self._rgb[1],self._rgb[2])
            
      

        p.fillRect(r, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

    def click(self):
        pass
        return

        # self.clicked.emit()

    def mouseReleaseEvent(self, e):
        pass

    def enterEvent(self, event):
        if event.type() == QEvent.Enter and not self.floatingLabel.isVisible():
            self.cleanFloatingLabel()

            position = QCursor.pos()
            position += QPoint(0, -20)  # Move the floating label up to improve its visibility
            labelText = STATE_NAME[self._state][self.lang]
            self.floatingLabel.setText(labelText)
            self.floatingLabel.move(position)

            self.floatingLabel.setVisible(True)
            self.floatingLabel.update()

            Pos.activeLabelList.append(self.floatingLabel)

    def leaveEvent(self, event):
        if event.type() == QEvent.Leave:
            self.cleanFloatingLabel()

    def cleanFloatingLabel(self):
        for i, label in enumerate(Pos.activeLabelList):
            label.setVisible(False)
            label.update()

        Pos.activeLabelList = []


class MainWindow(QMainWindow):
    def __init__(self, newboard_size, round_nbr, dB, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("spread : disease spread simple model")

        self.qLocale = QLocale()
        if self.qLocale.name()[0:2] == "fr":
            self.lang = LANG_FR
        else:
            self.lang = LANG_US

        self.status = STATUS_STOPPED

        self.board_size = newboard_size
        self.diseaseBoard = dB
        self.total_round_nbr = round_nbr

        # w est le Widge QT affiché dans la fenêtre
        w = QWidget()

        # hb : la bande horizontale supérieure de la fenêtre
        hb = QHBoxLayout()
        hb.addStretch(1)

        self.nb_toursLabel = QLabel()
        self.nb_toursLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.nb_toursLabel.setText("%03d" % 0)

        self._timer = QTimer()
        self._timer.timeout.connect(self.updateTimer)
        self._timer.start(100)  # in ms

        self.goButton = QPushButton("GO")
        self.goButton.setFixedSize(QSize(72, 32))
        self.goButton.setFlat(False)
        self.goButton.pressed.connect(self.goButtonPressed)

        self.nextButton = QPushButton("NEXT")
        self.nextButton.setFixedSize(QSize(72, 32))
        self.nextButton.setFlat(False)
        self.nextButton.pressed.connect(self.nextButtonPressed)

        self.resetButton = QPushButton("RESET")
        self.resetButton.setFixedSize(QSize(82, 32))
        self.resetButton.setFlat(False)
        self.resetButton.pressed.connect(self.resetButtonPressed)

        hb.addWidget(self.nb_toursLabel)
        hb.addWidget(self.goButton)
        hb.addWidget(self.nextButton)
        hb.addWidget(self.resetButton)

        # vb permet de mettre en place 2 lignes
        # La première ligne contient le hb ci-dessous (le header)
        # La seconde ligne contient un vboxlayout pour la configuration et un gridLayout pour le board
        vb = QVBoxLayout()
        vb.addLayout(hb)
        vb.addStretch(1)

        # Construction de la partie principale de la fenêtre
        # A l'aide d'un Hbox (mainLayout), mise en place d'une barre à gauche pour la configuration (QGridLayout de
        # QLabel et de QLineEdit) puis à droite le board et enfin la zone de graphique

        #
        # Panneau de configuration à gauche
        #
        self.confgrid = self.setupConfGrid()

        #
        # Principal grid pour l'affichage du diseaseBoard
        #
        self.grid = QGridLayout()
        self.grid.setSpacing(1)

        # Nécessaire pour permettre à l'affichage du board de rester compact
        gridLayout = QVBoxLayout()
        gridLayout.addStretch(1)
        gridLayout.addLayout(self.grid)

        #
        # Zone pour afficher les graphiques
        #

        graphLayout = QHBoxLayout()
        graphWidget = pg.PlotWidget()
        graphWidget.setBackground(self.palette().color(QPalette.Window))
        graphWidget.setXRange(0, 3*self.total_round_nbr, padding=0)
        graphLayout.addWidget(graphWidget)

        self.plots = [None] * PLOT_NB
        self.plots[RED_PLOT] = graphWidget.plot([],[], pen=pg.mkPen(color = (255,0,0), width=3), name="Red")
        self.plots[GREEN_PLOT] = graphWidget.plot([],[], pen=pg.mkPen(color=(0,255,0), width=3), name="Green")
        self.plots[BLUE_PLOT] = graphWidget.plot([],[], pen=pg.mkPen(color=(0,0,255), width=3), name="Blue")
        graphWidget.addLegend()

        mainLayout = QHBoxLayout()
        mainLayout.addStretch(1)
        mainLayout.addLayout(self.confgrid)
        mainLayout.addLayout(gridLayout)
        mainLayout.addLayout(graphLayout)
        vb.addLayout(mainLayout)

        #
        # Footer configuration
        #

        footerLayout = QHBoxLayout()

        popLabel = QLabel("Pop = " + self.qLocale.toString(self.diseaseBoard.population))
        popLabel.setStyleSheet("color: grey")
        footerLayout.addWidget(popLabel)

        r0Label = QLabel("R0 = " + self.qLocale.toString(self.diseaseBoard.R0))
        r0Label.setStyleSheet("color: grey")
        self.r0Label = r0Label
        footerLayout.addWidget(r0Label)

        ratioLabel = QLabel("time")
        ratioLabel.setStyleSheet("color: grey")
        self.ratioLabel = ratioLabel
        footerLayout.addWidget(ratioLabel)

        vb.addLayout(footerLayout)

        w.setLayout(vb)
        self.setCentralWidget(w)
        state, lan_vec = dB.lastBoard()
        self.initMap(state, lan_vec)
        self.show()

    def setupConfGrid(self):

        confgrid = QGridLayout()
        confgrid.setSpacing(1)

        for param, data in CONF_ELEMENTS.items():
            lbl = QLabel(data[0][self.lang])

            qle = QLineEdit()

            # if param == IMMUNITY_RATE_PARAM:
            #     qle.setText(self.qLocale.toString(self.diseaseBoard.immunityRate, precision = 2))
            # if param == CLUSTER_NB_PARAM:
            #     qle.setText(self.qLocale.toString(self.diseaseBoard.clusterNbr))
            # elif param == TRANSMISSION_RATE_PARAM:
            #     qle.setText(self.qLocale.toString(self.diseaseBoard.contagionRate, precision = 2))
            #     qle.textChanged.connect(self.updateR0)
            
            if data[1] == "double":
                qle.setValidator(QDoubleValidator(0.0, 1.0, 2))
            elif data[1] == "int":
                qle.setValidator(QIntValidator(0, self.total_round_nbr))

            qle.setAlignment(Qt.AlignRight)
            qle.setFixedWidth(40)

            confgrid.addWidget(lbl, param, 0)
            confgrid.addWidget(qle, param, 1)

        return confgrid

    def initMap(self, state,lan_vec):
        # Add positions to the map

        for x in range(0, self.board_size):
            for y in range(0, self.board_size):
                w = Pos(x, y, self.lang)
                self.grid.addWidget(w, x, y)
                w.redraw(state[x, y],lan_vec[0][x,y],lan_vec[1][x,y],lan_vec[2][x,y])

    def updateMap(self, etat,lan_vec):
        # Add positions to the map
        for x in range(0, self.board_size):
            for y in range(0, self.board_size):
                w = self.grid.itemAtPosition(x, y).widget()
                w.redraw(etat[x, y],lan_vec[0][x,y],lan_vec[1][x,y],lan_vec[2][x,y])

        # self.infectedLabel.setText("#Sick = " + self.qLocale.toString(self.diseaseBoard.sickNbr) +
        #                            " (inc #Hospit. = " +
        #                            self.qLocale.toString(self.diseaseBoard.hospitalizedNbr) + ")")

        # if self.diseaseBoard.diagnosedNbr != 0:
        #     self.ratioLabel.setText("#infected / #detected = " + \
        #                             self.qLocale.toString(self.diseaseBoard.sickNbr / self.diseaseBoard.diagnosedNbr))
        # else:
        #     self.ratioLabel.setText("#infected / #detected = N/A")

        round_nbr = self.diseaseBoard.currentRound
        counter = self.diseaseBoard.counter_points
        self.plots[RED_PLOT].setData(range(0, len(counter[0])), counter[0])
        self.plots[GREEN_PLOT].setData(range(0, len(counter[0])),counter[1])
        self.plots[BLUE_PLOT].setData(range(0, len(counter[0]) ), counter[2])

    def goButtonPressed(self):
        if (self.diseaseBoard.currentRound == 0):
            # Reconfiguration de la simulation
            self.diseaseBoard.contagionRate = self.qLocale.toDouble(
                self.confgrid.itemAtPosition(TRANSMISSION_RATE_PARAM, 1).widget().text())[0]
            self.diseaseBoard.mortalityRate = self.qLocale.toDouble(
                self.confgrid.itemAtPosition(MORTALITY_RATE_PARAM, 1).widget().text())[0]
            self.diseaseBoard.contagionDelay = self.qLocale.toDouble(
                self.confgrid.itemAtPosition(CONTAGION_DELAY_PARAM, 1).widget().text())[0]
            self.diseaseBoard.hospitalizedRate = self.qLocale.toDouble(
                self.confgrid.itemAtPosition(HOSPITALIZED_RATE_PARAM, 1).widget().text())[0]
            self.diseaseBoard.hospitalizedDelay = self.qLocale.toDouble(
                self.confgrid.itemAtPosition(HOSPITALIZED_DELAY_PARAM, 1).widget().text())[0]
            self.diseaseBoard.mortalityDelay = self.qLocale.toDouble(
                self.confgrid.itemAtPosition(MORTALITY_DELAY_PARAM, 1).widget().text())[0]
            self.diseaseBoard.quarantineRate = self.qLocale.toDouble(
                self.confgrid.itemAtPosition(QUARANTINE_RATE_PARAM, 1).widget().text())[0]
            self.diseaseBoard.diagnosisDelay = self.qLocale.toDouble(
                self.confgrid.itemAtPosition(DIAGNOSIS_DELAY_PARAM, 1).widget().text())[0]
            self.diseaseBoard.socialDistancingDelay = self.qLocale.toInt(
                self.confgrid.itemAtPosition(SOCIALDISTANCING_DELAY_PARAM, 1).widget().text())[0]
            self.diseaseBoard.socialDistancingContagionRate = self.qLocale.toDouble(
                self.confgrid.itemAtPosition(SOCIALDISTANCING_RATE_PARAM, 1).widget().text())[0]

        if self.status == STATUS_STOPPED:
            self.status = STATUS_PLAYING
            self.goButton.setText("PAUSE")

            for i in range(self.confgrid.rowCount()):
                self.confgrid.itemAtPosition(i, 1).widget().setReadOnly(True)
                self.confgrid.itemAtPosition(i, 1).widget().setStyleSheet("color: grey; selection-color: grey")
                self.confgrid.itemAtPosition(i, 1).widget().repaint()

        else:
            self.status = STATUS_STOPPED
            self.goButton.setText("GO")
            for i in range(self.confgrid.rowCount()):
                self.confgrid.itemAtPosition(i,1).widget().setReadOnly(False)
                self.confgrid.itemAtPosition(i, 1).widget().setStyleSheet("color: black; selection-color: black")
                self.confgrid.itemAtPosition(i, 1).widget().repaint()

    def nextButtonPressed(self):
        if self.diseaseBoard.currentRound + 1 > self.total_round_nbr:
            self.status = STATUS_STOPPED
            return

        etat,lan_vec = self.diseaseBoard.nextRound()
        self.nb_toursLabel.setText("%03d" % self.diseaseBoard.currentRound)
        self.updateMap(etat,lan_vec)
        self.updateR0()
        self.grid.update()

    def resetButtonPressed(self):
        self.diseaseBoard.immunityRate = self.qLocale.toDouble(
            self.confgrid.itemAtPosition(IMMUNITY_RATE_PARAM, 1).widget().text())[0]

        self.diseaseBoard.clusterNbr = self.qLocale.toInt(
            self.confgrid.itemAtPosition(CLUSTER_NB_PARAM, 1).widget().text())[0]

        self.diseaseBoard.reset()
        self.nb_toursLabel.setText("%03d" % 0)
        state,lan_vec = self.diseaseBoard.lastBoard()
        self.updateMap(state,lan_vec)
        self.updateR0()

        self.goButton.setText("GO")
        self.status = STATUS_STOPPED

    def updateTimer(self):
        if self.status == STATUS_PLAYING:

            if self.diseaseBoard.currentRound + 1 > self.total_round_nbr :
                self.status = STATUS_STOPPED
                for i in range(self.confgrid.rowCount()):
                    self.confgrid.itemAtPosition(i,1).widget().setReadOnly(False)
                    self.confgrid.itemAtPosition(i, 1).widget().setStyleSheet("color: black; selection-color: black")
                    self.confgrid.itemAtPosition(i, 1).widget().repaint()

                return

            self.nb_toursLabel.setText("%03d" % self.diseaseBoard.currentRound)
            etat,lan_vec = self.diseaseBoard.nextRound()
            self.updateMap(etat,lan_vec)
            self.updateR0()

    def updateR0(self):
        self.r0Label.setText("R0 = {:.3} ".format(self.diseaseBoard.R0))

def usage():
    print(
"""Usage: spread [options] round_number board_size cluster_number
            round_number: number of rounds for the simulation
            board_size: size of the board
            cluster_number: number of initial board disease clusters""")


if __name__ == '__main__':

    tours = 150
    board_size = 40
    nb_clusters = 3

    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'h')
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    for o, c in optlist:
        if o == '-h':
            usage()
            sys.exit()

    if len(sys.argv) >= 2:
        try:
            tours = int(sys.argv[1])
        except:
            pass

    if len(sys.argv) >= 3:
        try:
            board_size = int(sys.argv[2])
        except:
            pass

    if len(sys.argv) >= 4:
        try:
            nb_clusters = int(sys.argv[3])
        except:
            pass

    db = LanguageBoard(board_size, tours, nb_clusters)
    db.immunityRate = 0.0
    # Entre 2 et 3 personnes contaminées par malade, si on considère qu'à chaque tour (a peu près un jour), on
    # a l'occasion de contaminer environ 15 personnes, et ce pendant la durée de la contamination, considérée comme
    # égale au délai de rétablissement

    app = QApplication([])
    window = MainWindow(board_size, tours, db)
    app.exec_()
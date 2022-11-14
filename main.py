import sys
import threading
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime
import os
import csv
import sys
import csv
import time
import pandas as pd
import numpy as np
import json
import pythoncom
import pymysql
import telegram


form_class = uic.loadUiType(f"main.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.setupUi(self)
        self.old_position = None
        self.keyword_dict = dict()

        wt = 800
        ht = 600
        self.resize(wt, ht)

        gr_list = ['config_gr', 'collect_gr']
        for gr in gr_list:
            cgr = self.findChild(QGroupBox, gr)
            w = cgr.width()
            h = cgr.height()
            cgr.move((wt - w) / 2, (ht - h) / 2)

        tb_list = ['keyword_table', 'keyword_table2']
        for tb_name in tb_list:
            tb = self.findChild(QTableWidget, tb_name)
            tb.setColumnWidth(0, tb.width() * 0.3)
            tb.setColumnWidth(1, tb.width() * 0.69)

        self.findChild(QPushButton, 'close_pg').clicked.connect(self.close_pg_clicked)
        self.findChild(QPushButton, 'hide_pg').clicked.connect(self.hide_pg_clicked)
        self.findChild(QPushButton, 'set_detail_close').clicked.connect(self.set_detail_close_clicked)
        self.findChild(QPushButton, 'set_detail_btn').clicked.connect(self.set_detail_btn_clicked)
        self.findChild(QPushButton, 'add_keyword').clicked.connect(self.add_keyword_clicked)

        self.findChild(QGroupBox, 'collect_gr').setVisible(False)

    def add_keyword_clicked(self):
        current_keyword = self.findChild(QLineEdit, 'keyword_edit').text()
        self.keyword_dict[current_keyword] = {
            'flag': False
        }
        self.update_keyword_table()
        self.findChild(QLabel, 'log').setText(f'{current_keyword} 추가 완료.')
        return

    def update_keyword_table(self):
        for tb_name in ['keyword_table', 'keyword_table2']:
            tb = self.findChild(QTableWidget, tb_name)

            keyword_list = list(self.keyword_dict.keys())
            tb.setRowCount(len(keyword_list))
            for idx in range(len(keyword_list)):
                tb.setItem(idx, 0, QTableWidgetItem(str(idx)))
                tb.setItem(idx, 1, QTableWidgetItem(str(keyword_list[idx])))
        return

    def set_detail_btn_clicked(self):
        return

    def set_detail_close_clicked(self):
        return

    def mousePressEvent(self, e):
        self.old_position = e.globalPos()

    def mouseMoveEvent(self, e):
        if self.old_position is None:
            return
        delta = QPoint(e.globalPos() - self.old_position)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_position = e.globalPos()

    def hide_pg_clicked(self):
        self.showMinimized()

    def close_pg_clicked(self):
        QCoreApplication.instance().quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
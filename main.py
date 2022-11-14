from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime
import sys


form_class = uic.loadUiType(f"main.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.setupUi(self)
        self.old_position = None
        self.keyword_dict = dict()
        self.news_list    = []
        self.log          = self.findChild(QLabel, 'log')
        self.log2         = self.findChild(QLabel, 'log2')

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

        tb = self.findChild(QTableWidget, 'news_table')
        tb.setColumnWidth(0, tb.width() * 0.25)
        tb.setColumnWidth(1, tb.width() * 0.74)

        # 버튼
        self.findChild(QPushButton, 'close_pg').clicked.connect(self.close_pg_clicked)
        self.findChild(QPushButton, 'hide_pg').clicked.connect(self.hide_pg_clicked)
        self.findChild(QPushButton, 'set_detail_close').clicked.connect(self.set_detail_close_clicked)
        self.findChild(QPushButton, 'set_detail_btn').clicked.connect(self.set_detail_btn_clicked)
        self.findChild(QPushButton, 'add_keyword').clicked.connect(self.add_keyword_clicked)
        self.findChild(QPushButton, 'set_date').clicked.connect(self.set_date_clicked)
        self.findChild(QPushButton, 'reset_date').clicked.connect(self.reset_date_clicked)
        self.findChild(QPushButton, 'config_btn').clicked.connect(self.config_btn_clicked)

        # 테이블
        self.findChild(QTableWidget, 'keyword_table').clicked.connect(self.keyword_table_clicked)
        self.findChild(QTableWidget, 'keyword_table2').clicked.connect(self.keyword_table2_clicked)

        # 그룹 박스
        self.findChild(QGroupBox, 'collect_gr').setVisible(False)

        # 날짜 세팅
        self.findChild(QLineEdit, 'start_date').setText(str(datetime.datetime.now() - datetime.timedelta(days=30)).split(' ')[0])
        self.findChild(QLineEdit, 'end_date').setText(str(datetime.datetime.now()).split(' ')[0])

        # 라디오 버튼
        self.findChild(QComboBox, 'filter').activated.connect(self.filter_activated)
        
        # 테스트 뉴스
        self.add_news_table({'title': '7공화국 개헌, 이번에는?', 'corp': '매일경제', 'color': 'red'})
        self.add_news_table({'title': '"尹대통령 개헌 적극적, 펠로시는 비비언 리 연상"[국회의장 단독인터뷰]', 'corp': '조선일보', 'color': 'red'})
        self.add_news_table({'title': '''통일교, 日의원에 개헌 등 '정책협정' 요구 의혹…기시다 "확인하겠다"''', 'corp': '한겨레', 'color': 'skyblue'})

    def filter_activated(self):
        print(self.findChild(QComboBox, 'filter').currentText())

    def add_news_table(self, news):
        self.news_list.append(news)

        tb = self.findChild(QTableWidget, 'news_table')

        idx = tb.rowCount()
        tb.insertRow(idx)

        i = QTableWidgetItem(str(news['corp']))
        i.setFlags(Qt.ItemIsEnabled)
        i.setBackground(QColor(news['color']))
        tb.setItem(idx, 0, i)

        i = QTableWidgetItem(str(news['title']))
        i.setFlags(Qt.ItemIsEnabled)
        tb.setItem(idx, 1, i)

    def config_btn_clicked(self):
        self.findChild(QGroupBox, 'config_gr').setVisible(True)
        self.findChild(QGroupBox, 'collect_gr').setVisible(False)
        return

    def reset_date_clicked(self):
        self.findChild(QLineEdit, 'start_date').setEnabled(True)
        self.findChild(QLineEdit, 'end_date').setEnabled(True)

        self.findChild(QPushButton, 'set_date').setVisible(True)
        self.findChild(QPushButton, 'reset_date').setVisible(False)

    def set_date_clicked(self):
        start_date = self.findChild(QLineEdit, 'start_date').text()
        end_date   = self.findChild(QLineEdit, 'end_date').text()

        try:
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
        except:
            self.log2.setText('시작 날짜 형식은 %Y-%m-%d 여야 합니다.')
            return
        try:
            datetime.datetime.strptime(end_date, '%Y-%m-%d')
        except:
            self.log2.setText('끝 형식은 %Y-%m-%d 여야 합니다.')
            return

        self.findChild(QPushButton, 'set_date').setVisible(False)
        self.findChild(QPushButton, 'reset_date').setVisible(True)
        self.findChild(QLineEdit, 'start_date').setEnabled(False)
        self.findChild(QLineEdit, 'end_date').setEnabled(False)
        self.log2.setText('날짜 설정 완료. 수집이 시작 됩니다.')
        return

    def keyword_table2_clicked(self):
        index = self.findChild(QTableWidget, 'keyword_table2').currentIndex()
        return

    def keyword_table_clicked(self):
        tb      = self.findChild(QTableWidget, 'keyword_table')
        index   = tb.currentRow()
        keyword = tb.item(index, 1).text()
        self.findChild(QLabel, 'curr_keyword').setText(str(keyword))
        return

    def add_keyword_clicked(self):
        current_keyword = self.findChild(QLineEdit, 'keyword_edit').text()
        self.keyword_dict[current_keyword] = {
            'flag': False
        }
        self.update_keyword_table()
        self.log.setText(f'[{current_keyword}] 추가 완료.')
        return

    def update_keyword_table(self):
        # for tb_name in ['keyword_table', 'keyword_table2']:
        tb = self.findChild(QTableWidget, 'keyword_table')

        keyword_list = list(self.keyword_dict.keys())
        tb.setRowCount(len(keyword_list))
        for idx in range(len(keyword_list)):
            index_item = QTableWidgetItem(str(idx))
            index_item.setFlags(Qt.ItemIsEnabled)
            tb.setItem(idx, 0, index_item)

            keyword_item = QTableWidgetItem(str(keyword_list[idx]))
            keyword_item.setFlags(Qt.ItemIsEnabled)
            tb.setItem(idx, 1, keyword_item)

        tb = self.findChild(QTableWidget, 'keyword_table2')

        keyword_list = list(self.keyword_dict.keys())
        tb.setRowCount(len(keyword_list))
        for idx in range(len(keyword_list)):
            current_keyword = str(keyword_list[idx])
            flag            = self.keyword_dict[current_keyword]['flag']
            if flag:
                index_item = QTableWidgetItem(str(idx))
                index_item.setFlags(Qt.ItemIsEnabled)
                tb.setItem(idx, 0, index_item)

                keyword_item = QTableWidgetItem(current_keyword)
                keyword_item.setFlags(Qt.ItemIsEnabled)
                tb.setItem(idx, 1, keyword_item)
            else:
                tb.setRowCount(tb.rowCount() - 1)
        return

    def set_detail_btn_clicked(self):
        current_keyword = self.findChild(QLineEdit, 'keyword_edit').text()
        self.log.setText(f'[{current_keyword}] 설정 완료.')
        self.keyword_dict[current_keyword]['flag'] = True
        self.update_keyword_table()
        return

    def set_detail_close_clicked(self):
        self.findChild(QGroupBox, 'config_gr').setVisible(False)
        self.findChild(QGroupBox, 'collect_gr').setVisible(True)
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
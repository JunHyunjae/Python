import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtGui import *
from PyQt5 import uic

form_class = uic.loadUiType("main.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("PyStock")

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        self.kiwoom.OnEventConnect.connect(self.event_connect)
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)

        self.login_lineEdit.setEnabled(False)
        self.account_textEdit.setEnabled(False)
        self.output_textEdit.setEnabled(False)

        self.code_lineEdit.setText("039490")

        self.login_btn.clicked.connect(self.login_btn_clicked)
        self.account_btn.clicked.connect(self.account_btn_clicked)
        self.code_btn.clicked.connect(self.code_btn_clicked)
        self.search_btn.clicked.connect(self.search_btn_clicked)

    def login_btn_clicked(self):
        self.kiwoom.dynamicCall("CommConnect()")

    def event_connect(self, nErrCode):
        if nErrCode == 0:
            self.login_lineEdit.setText("로그인 성공")
        else:
            self.login_lineEdit.setText("로그인 실패")

    def account_btn_clicked(self):
        self.account_textEdit.clear()
        account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
        username = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["USER_NAME"])
        self.account_textEdit.append("사용자명 : " + username.strip())
        self.account_textEdit.append("계좌정보 : " +account_num.rstrip(";"))

    def code_btn_clicked(self):
        self.code_listWidget.clear()
        kospi_code_list = self.kiwoom.dynamicCall("GetCodeListByMarket(QSTRING)", ["0"]).split(';')
        print(kospi_code_list)
        kospi_code_name_list = []

        for code in kospi_code_list:
            name = self.kiwoom.dynamicCall("GetMasterCodeName(QSTRING)", [code])
            if name:
                kospi_code_name_list.append(code + " : " + name)

        self.code_listWidget.addItems(kospi_code_name_list)

    def search_btn_clicked(self):
        code = self.code_lineEdit.text()
        self.output_textEdit.append("종목코드: " + code)

        # SetInputValue
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)

        # CommRqData
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101")


    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if rqname == "opt10001_req":
            # name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname,
                                          # 0, "종목명")
            name = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "종목명")
            current_price = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "현재가")
            high = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "상한가")
            volume = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname,
                                             0, "거래량")  # CommGetData는 없어질 함수이므로 GetCommData를 사용해야 함.

            self.output_textEdit.append("종목명: " + name.strip())
            self.output_textEdit.append("거래량: " + volume.strip())
            self.output_textEdit.append("현재가: " + current_price.strip())
            self.output_textEdit.append("상한가: " + high.strip())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()


''' 
    self.statusBar().showMessage("Not connected")   # 하단의 status bar에 text를 출력하는 방법
    
    self.label.setText("Connected")  # label 내용 입력
              
    self.textedit.setText("입력 text")    # textEdit 내용 입력 
    txt = self.textedit.toPlainText()   # 내용글 얻어오기

    self.code_line_edit.setText("039490")   # lineEdit 내용 입력
    code = self.code_line_edit.text()   # 내용글 얻어오기            
'''
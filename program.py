import sys, os

from PyQt5 import QtWidgets, QtCore, uic, QtGui, QtSql, QtPrintSupport

import shutil
import main_windows, Priv
import sql, text
import time, datetime


class Thread(QtCore.QThread):
    sig = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        while True:
            time.sleep(10)
            self.sig.emit()

#
class RegistForm(QtWidgets.QWidget):
    def __init__(self, sql, parent=None):
        super(RegistForm, self).__init__()
        uic.loadUi("ui_Regist.ui", self)
        self.sql = sql
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.Enter.clicked.connect(self.EnterReg)
        self.Cancel.clicked.connect(self.close)

    def EnterReg(self):
        if (
                                    self.login.text() and self.password.text() and self.f.text() and self.i.text() and self.o.text() and self.phone.text()) != '':
            self.sql.Insert('users', self.login.text(), self.password.text(), self.f.text(), self.i.text(),
                            self.o.text(), self.phone.text(), 'Не активен')
            self.close()
        else:
            self.ErrorL.setText('Все поля должны быть заполнены.')

#
class MyWindow(QtWidgets.QMainWindow, main_windows.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.sql = sql.SqlCom()
        # переменные для работы кнопок
        self.photos = self.sql.SelectOne('photo', 'route')
        self.idNews = 1
        self.idMax = self.sql.SelectMaxID('news_admin')
        self.news = self.sql.SelectOne('news_admin', 'news', 'ID', self.idNews)
        self.News.setText(self.news[0])
        self.Photo.setPixmap(QtGui.QPixmap(self.photos[0]))
        self.counP = 0
        self.posP = -1
        for i in self.photos:
            self.posP += 1
        # вывод таблицы комментариев
        self.TableCommentUp()
        # Кнопки
        self.Comment.clicked.connect(self.CommentF)
        self.com = CommentForm(self.sql, MyWindow)
        self.Register.clicked.connect(self.RegistF)
        self.reg = RegistForm(self.sql)
        self.us = PrivilegForm(self.sql, user)
        self.About.clicked.connect(self.AboutB)
        self.Cabinet.clicked.connect(self.CabinetB)
        self.Rent.clicked.connect(self.RentB)
        self.Services.clicked.connect(self.ServicesB)
        self.Contacts.clicked.connect(self.ContactsB)
        self.Manual.clicked.connect(self.ManualB)
        self.Text.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.News.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.AboutB()

    def ManualB(self):
        self.Text.setHtml(text.e)

    def ContactsB(self):
        self.Text.setHtml(text.d)

    def ServicesB(self):
        self.Text.setHtml(text.c)

    def RentB(self):
        self.Text.clear()
        self.Text.insertPlainText('У нас есть следующее оборудование для аренды - \n\n')
        for i in self.sql.SelectOne('rent','nameIns'):
            self.Text.insertPlainText(i+' - '+str(self.sql.SelectOne('rent','price','nameIns',"'"+i+"'")[0])+'\n')
        self.Text.insertPlainText('\n Оборудование арендуется на все время репетиции, не зависимо от колличества часов.')


    def CabinetB(self):
        self.Text.setHtml(text.b)

    def AboutB(self):
        self.Text.setHtml(text.a)

    def TableCommentUp(self):
        self.sgm = QtSql.QSqlQueryModel(parent=self.tableC)
        self.sgm.setQuery("select * from comments order by ID desc")
        self.sgm.setHeaderData(1, QtCore.Qt.Horizontal, 'Логин')
        self.sgm.setHeaderData(2, QtCore.Qt.Horizontal, 'Комментарий')
        self.tableC.setModel(self.sgm)
        self.tableC.hideColumn(0)
        self.tableC.resizeRowsToContents()
        self.tableC.setColumnWidth(2, 166)

    def RegistF(self):
        self.reg.show()
        self.reg.login.clear()
        self.reg.password.clear()
        self.reg.phone.clear()
        self.reg.f.clear()
        self.reg.i.clear()
        self.reg.o.clear()

    def CommentF(self):
        self.com.show()
        self.com.textEdit.clear()

    def EnterUs(self):
        log = self.Login.text()
        pas = self.Password.text()
        self.query = QtSql.QSqlQuery()
        self.query.exec(
            "select login,status from users where login=" + "'" + log + "'" + " and password=" + "'" + pas + "'")
        if self.query.isActive():
            self.query.first()
            if self.query.isValid():
                user.append(self.query.value('login'))
                user.append(self.query.value('status'))
                self.query.finish()
                self.Password.clear()
                if user[1]!='Не активен':
                    self.us.show()
                    self.us.start()
                else:
                    user.clear()
                    self.Login.setText('Не Активирован')
            else:
                self.Login.setText('error')

    def PhotoB(self):
        self.counP -= 1
        if self.counP < 0:
            self.counP = self.posP
        self.Photo.setPixmap(QtGui.QPixmap(self.photos[self.counP]))

    def PhotoN(self):
        self.counP += 1
        if self.counP > self.posP:
            self.counP = 0
        self.Photo.setPixmap(QtGui.QPixmap(self.photos[self.counP]))

    def NewsB(self):
        self.idNews -= 1
        if self.idNews < 1:
            self.idNews = self.idMax
            self.News.setText(self.sql.SelectOne('news_admin', 'news', 'ID', self.idNews)[0])
        else:
            self.News.setText(self.sql.SelectOne('news_admin', 'news', 'ID', self.idNews)[0])

    def NewsN(self):
        self.idNews += 1
        if not self.sql.SelectOne('news_admin', 'news', 'ID', self.idNews):
            self.idNews = 1
            self.News.setText(self.sql.SelectOne('news_admin', 'news', 'ID', self.idNews)[0])
        else:
            self.News.setText(self.sql.SelectOne('news_admin', 'news', 'ID', self.idNews)[0])

#
class RecordBand(QtWidgets.QWidget):
    def __init__(self, sql, parent=None):
        super(RecordBand, self).__init__()
        self.sql = sql
        uic.loadUi("ui_record.ui", self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.Cancel.clicked.connect(self.close)
        self.Record.clicked.connect(self.addRecord)
        self.Date.dateChanged.connect(self.selectTable)

    def selectTable(self):
        self.sgm = QtSql.QSqlQueryModel(parent=self.Table)
        self.sgm.setQuery("select time,timeEnd from sing_up where date='" + self.Date.text() + "'")
        self.sgm.setHeaderData(0, QtCore.Qt.Horizontal, 'Начало')
        self.sgm.setHeaderData(1, QtCore.Qt.Horizontal, 'Конец')
        self.Table.setModel(self.sgm)
        self.Table.resizeRowsToContents()
        self.Table.setColumnWidth(2, 166)

    def addRecord(self):
        band = self.sql.SelectOne('bands', 'ID', 'nameB', "'" + self.Band.currentText() + "'")[0]
        self.sql.Insert('sing_up', band, self.Date.text(), self.Time.text(), self.TimeEnd.text(), self.Data.text())
        self.close()

    def addBand(self):
        self.Band.clear()
        self.Band.addItems(self.sql.SelectOne('bands', 'nameB'))
        datePc = datetime.datetime.now()
        self.Date.setDate(datePc.date())
        self.selectTable()

#
class PayForm(QtWidgets.QWidget):
    def __init__(self, sql, parent=None):
        super(PayForm, self).__init__()
        uic.loadUi("ui_Pay.ui", self)
        self.sql = sql
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.IntPay = 0
        self.IntZ = 0
        self.Cancel.clicked.connect(self.close)
        self.Band.activated.connect(self.TimeTimeEnd)
        self.Pay.setDecMode()
        self.addRent.clicked.connect(self.addR)
        self.addHour.clicked.connect(self.addH)
        self.PayBand.editingFinished.connect(self.ReturnSum)
        self.PayB.clicked.connect(self.addPay)
        self.Instruction.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.RentT.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

    def addPay(self):
        self.sql.Insert('pay', self.sql.SelectOne('bands', 'ID', 'nameB', "'" + self.Band.currentText() + "'")[0],
                        datetime.datetime.now().strftime("%d.%m.%Y"), self.Time.text(), self.TimeEnd.text(),
                        self.RentT.toPlainText(), self.Pay.intValue())
        txt = QtGui.QTextDocument()
        txt.setPlainText(
            '-' * 100 + "\n Репетиционная студия '9/10'" + "\n Спасибо что провели у нас репетицию " + self.Band.currentText() + "\n" + '-' * 100 +
            '\n' + str(datetime.datetime.now()) +
            '\n К оплате - \n Продолжительность репетиции - ' + self.Hour.text() + ' час/часов \n' + '(Стоимость часа - 200 руб)\n' +
            'Арендованно оборудование: \n' + self.RentT.toPlainText() + '\n' + '-' * 100 +
            '\n Итог - ' + str(self.Pay.intValue()) + '\n Внесено -' + self.PayBand.text() + '\n Сдача - ' + str(
                self.Return.intValue()) +
            '\n Спасибо ' + self.Band.currentText() + ', приходите еще. \n' + '-' * 100)
        pri = QtPrintSupport.QPrinter()
        dia = QtPrintSupport.QPrintDialog(pri)
        dia.exec()
        txt.print_(pri)
        self.sql.Delete('sing_up', self.sql.SelectOne('bands', 'ID', 'nameB', "'" + self.Band.currentText() + "'")[0],
                        datetime.datetime.now().strftime("%d.%m.%Y"))
        self.close()

    def ReturnSum(self):
        self.Return.display(int(self.PayBand.text()) - self.Pay.intValue())

    def addH(self):
        self.Pay.display(self.Pay.intValue()+int(self.Hour.text()) * 200)
        self.addHour.setEnabled(False)

    def addR(self):
        self.RentT.insertPlainText(self.Rent.currentText() + ', ')
        self.Pay.display(self.Pay.intValue()+self.sql.SelectOne('rent', 'price', 'nameIns', "'" + self.Rent.currentText() + "'")[0])
        self.Rent.removeItem(self.Rent.currentIndex())
        if self.Rent.count() == 0:
            self.addRent.setEnabled(False)

    def TimeTimeEnd(self):
        self.Time.setText(self.sql.SelectOne('sing_up', 'time', 'id_nameB', self.sql.SelectOne('bands', 'ID', 'nameB',
                                                                                               "'" + self.Band.currentText() + "'")[
            0])[0])
        self.TimeEnd.setText(self.sql.SelectOne('sing_up', 'timeEnd', 'id_nameB',
                                                self.sql.SelectOne('bands', 'ID', 'nameB',
                                                                   "'" + self.Band.currentText() + "'")[0])[0])

    def Start(self):
        self.addHour.setEnabled(True)
        self.addRent.setEnabled(True)
        self.Pay.display(0)
        self.Return.display(0)
        self.Band.clear()
        self.Rent.clear()
        for i in self.sql.SelectOne('sing_up', 'id_nameB', 'date',
                                    "'" + datetime.datetime.now().strftime("%d.%m.%Y") + "'"):
            self.Band.addItems(self.sql.SelectOne('bands', 'nameB', 'ID', i))
        self.Rent.addItems(self.sql.SelectOne('rent', 'nameIns'))
        self.Time.clear()
        self.TimeEnd.clear()
        self.RentT.clear()
        self.PayBand.clear()
        self.Hour.setValue(0)

#
class ReportYear(QtWidgets.QWidget):
    def __init__(self, sql, parent=None):
        super(ReportYear, self).__init__()
        uic.loadUi("ui_report.ui", self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.sql = sql
        self.report = QtGui.QTextDocument()
        self.YearEdit.editingFinished.connect(self.start)
        self.Close.clicked.connect(self.close)
        self.Print.clicked.connect(self.PrintR)
        self.Text.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

    def PrintR(self):
        pri = QtPrintSupport.QPrinter()
        dia = QtPrintSupport.QPrintDialog(pri)
        dia.exec()
        self.report.print_(pri)

    def start(self):
        self.Text.clear()
        self.report.clear()
        self.Text.insertPlainText('-' * 100 + '\n Годовой отчет \n \n \n')
        pr = 0
        for i in range(13):
            if i != 0:
                sum = 0
                if i < 10:
                    self.sql.query.exec("select * from pay where date like '__.0" + str(i) + "." + str(self.YearEdit.text()) + "'")
                else:
                    self.sql.query.exec(
                        "select * from pay where date like '__." + str(i) + "." + str(self.YearEdit.text()) + "'")
                lst1 = []
                if self.sql.query.isActive():
                    self.sql.query.first()
                    while self.sql.query.isValid():
                        lst1.append(self.sql.query.value('price'))
                        self.sql.query.next()
                for f in lst1:
                    sum += f
                pr += sum
                self.Text.insertPlainText(str(i) + ' Месяц - ' + str(sum) + ' руб. \n')
        self.Text.insertPlainText('-' * 100 + '\n Годовая прибыль -> ' + str(pr) + '\n' + '-' * 100)
        self.report.setPlainText(self.Text.toPlainText())


#
class ReportMount(QtWidgets.QWidget):
    def __init__(self, sql, parent=None):
        super(ReportMount, self).__init__()
        uic.loadUi("ui_reportM.ui", self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.sql = sql
        self.report = QtGui.QTextDocument()
        self.Mount.editingFinished.connect(self.start)
        self.Year.editingFinished.connect(self.start)
        self.Close.clicked.connect(self.close)
        self.Print.clicked.connect(self.PrintR)
        self.Text.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

    def PrintR(self):
        pri = QtPrintSupport.QPrinter()
        dia = QtPrintSupport.QPrintDialog(pri)
        dia.exec()
        self.report.print_(pri)

    def start(self):
        self.Text.clear()
        self.report.clear()
        self.Text.insertPlainText('-' * 100 + '\n Отчет за месяц \n \n \n' + 'Группа | Дата   | Сумма \n')
        pr = 0
        lst = []
        if int(self.Mount.text()) < 10:
            self.sql.query.exec(
                "select * from pay where date like '__.0" + str(self.Mount.text()) + "." + str(self.Year.text()) + "'")
        else:
            self.sql.query.exec(
                "select * from pay where date like '__." + str(self.Mount.text()) + "." + str(self.Year.text()) + "'")
        if self.sql.query.isActive():
            self.sql.query.first()
            while self.sql.query.isValid():
                lst.append(self.sql.query.value('id_nameB'))
                lst.append(self.sql.query.value('date'))
                lst.append(self.sql.query.value('price'))
                self.sql.query.next()
        con = 0
        for i in lst:
            if con == 0:
                self.Text.insertPlainText(self.sql.SelectOne('bands', 'nameB', 'ID', "'" + str(i) + "'")[0] + '  ')
                con += 1
            elif con == 1:
                self.Text.insertPlainText(str(i) + '  ')
                con += 1
            elif con == 2:
                pr += i
                self.Text.insertPlainText(str(i) + '\n')
                con = 0
        self.Text.insertPlainText('-' * 100 + '\n Прибыль -> ' + str(pr) + '\n' + '-' * 100)
        self.report.setPlainText(self.Text.toPlainText())

#
class PrivilegForm(QtWidgets.QWidget, Priv.Ui_FormPriv):
    def __init__(self, sql, parent=None):
        super(PrivilegForm, self).__init__()
        self.sql = sql
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.Comment.clicked.connect(self.UsComment)
        self.com = ''
        self.Exit.clicked.connect(self.close)
        self.NewsAdminB.clicked.connect(self.newsAdminText)
        self.newsAd = NewsAdminForm(self.sql, PrivilegForm)
        self.Box.activated.connect(self.tableUp)
        self.addB.clicked.connect(self.addBut)
        self.deleteB.clicked.connect(self.delBut)
        self.newPhoto.clicked.connect(self.newPh)
        self.time()
        self.RecordB.clicked.connect(self.addRec)
        self.record = RecordBand(self.sql)
        self.pay = PayForm(self.sql)
        self.PayB.clicked.connect(self.addPay)
        self.DayB.clicked.connect(self.FilterDay)
        self.EnterRecB.clicked.connect(self.EntRec)
        self.EnterPayB.clicked.connect(self.EntPay)
        self.EnterRec.clicked.connect(self.EntRecD)
        self.EnterPay.clicked.connect(self.EntPayD)
        self.reportY = ReportYear(self.sql)
        self.yearB.clicked.connect(self.year)
        self.reportM = ReportMount(self.sql)
        self.mountB.clicked.connect(self.mount)
        self.DayT.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

    def mount(self):
        self.reportM.show()
        self.reportM.start()

    def year(self):
        self.reportY.show()
        self.reportY.start()

    def EntPayD(self):
        self.Table.setModel(self.sql.STMR('pay', 'date', self.PayDate.text()))
        self.Table.setItemDelegateForColumn(1, QtSql.QSqlRelationalDelegate(self.Table))
        self.Table.hideColumn(0)
        self.Table.resizeRowsToContents()
        self.Table.setColumnWidth(2, 166)
        self.Table.setSortingEnabled(True)

    def EntRecD(self):
        self.Table.setModel(self.sql.STMR('sing_up', 'date', self.RecDate.text()))
        self.Table.setItemDelegateForColumn(1, QtSql.QSqlRelationalDelegate(self.Table))
        self.Table.hideColumn(0)
        self.Table.resizeRowsToContents()
        self.Table.setColumnWidth(2, 166)
        self.Table.setSortingEnabled(True)

    def EntPay(self):
        self.Table.setModel(self.sql.STMR('pay', 'id_nameB', str(
            self.sql.SelectOne('bands', 'ID', 'nameB', "'" + self.BandBox.currentText() + "'")[0])))
        self.Table.setItemDelegateForColumn(1, QtSql.QSqlRelationalDelegate(self.Table))
        self.Table.hideColumn(0)
        self.Table.resizeRowsToContents()
        self.Table.setColumnWidth(2, 166)
        self.Table.setSortingEnabled(True)

    def EntRec(self):
        self.Table.setModel(self.sql.STMR('sing_up', 'id_nameB', str(
            self.sql.SelectOne('bands', 'ID', 'nameB', "'" + self.BandBox.currentText() + "'")[0])))
        self.Table.setItemDelegateForColumn(1, QtSql.QSqlRelationalDelegate(self.Table))
        self.Table.hideColumn(0)
        self.Table.resizeRowsToContents()
        self.Table.setColumnWidth(2, 166)
        self.Table.setSortingEnabled(True)

    def FilterDay(self):
        self.Table.setModel(self.sql.STMR('sing_up', 'date', datetime.datetime.now().strftime("%d.%m.%Y")))
        self.Table.setItemDelegateForColumn(1, QtSql.QSqlRelationalDelegate(self.Table))
        self.Table.hideColumn(0)
        self.Table.resizeRowsToContents()
        self.Table.setColumnWidth(2, 166)
        self.Table.setSortingEnabled(True)

    def addPay(self):
        self.pay.show()
        self.pay.Start()

    def addRec(self):
        self.record.show()
        self.record.addBand()

    def time(self):
        dtime = datetime.datetime.now()
        self.DateL.setText(str(dtime.day) + '/' + str(dtime.month) + '/' + str(dtime.year))
        self.TimeL.setText(str(dtime.hour) + ':' + str(dtime.minute))

    def newPh(self):
        file = QtWidgets.QFileDialog.getOpenFileName(caption='Добавить Фото')
        if file[0] != '':
            shutil.copy(file[0], "photo")
            self.sql.Insert('photo', os.path.basename(file[0]))
            os.path.basename(file[0])

    def delBut(self):
        self.sql.stmR.removeRow(self.Table.currentIndex().row())
        self.sql.stmR.select()
        self.sql.stm.removeRow(self.Table.currentIndex().row())
        self.sql.stm.select()

    def addBut(self):
        self.sql.stm.insertRow(self.sql.stm.rowCount())
        self.sql.stmR.insertRow(self.sql.stmR.rowCount())

    def tableUp(self):
        if self.Box.currentText() == 'Группы':
            self.Table.setModel(self.sql.STM('bands'))
            self.Table.hideColumn(0)
            self.Table.resizeRowsToContents()
            self.Table.setColumnWidth(2, 166)
            self.Table.setSortingEnabled(True)
        if self.Box.currentText() == 'Пользователи':
            self.Table.setModel(self.sql.STM('users'))
            self.Table.hideColumn(0)
            self.Table.resizeRowsToContents()
            self.Table.setColumnWidth(2, 166)
            self.Table.setSortingEnabled(True)
        if self.Box.currentText() == 'Коментарии':
            self.Table.setModel(self.sql.STM('comments'))
            self.Table.hideColumn(0)
            self.Table.resizeRowsToContents()
            self.Table.setColumnWidth(2, 166)
            self.Table.setSortingEnabled(True)
        if self.Box.currentText() == 'Аренда':
            self.Table.setModel(self.sql.STM('rent'))
            self.Table.hideColumn(0)
            self.Table.resizeRowsToContents()
            self.Table.setColumnWidth(2, 166)
            self.Table.setSortingEnabled(True)
        if self.Box.currentText() == 'Новости':
            self.Table.setModel(self.sql.STM('news_admin'))
            self.Table.hideColumn(0)
            self.Table.resizeRowsToContents()
            self.Table.setColumnWidth(2, 166)
            self.Table.setSortingEnabled(True)
        if self.Box.currentText() == 'Фотографии':
            self.Table.setModel(self.sql.STM('photo'))
            self.Table.hideColumn(0)
            self.Table.resizeRowsToContents()
            self.Table.setColumnWidth(2, 166)
            self.Table.setSortingEnabled(True)
        if self.Box.currentText() == 'Записи':
            self.Table.setModel(self.sql.STMR('sing_up'))
            self.Table.setItemDelegateForColumn(1, QtSql.QSqlRelationalDelegate(self.Table))
            self.Table.hideColumn(0)
            self.Table.resizeRowsToContents()
            self.Table.setColumnWidth(2, 166)
            self.Table.setSortingEnabled(True)
        if self.Box.currentText() == 'Приемка':
            self.Table.setModel(self.sql.STMR('pay'))
            self.Table.setItemDelegateForColumn(1, QtSql.QSqlRelationalDelegate(self.Table))
            self.Table.hideColumn(0)
            self.Table.resizeRowsToContents()
            self.Table.setColumnWidth(2, 166)
            self.Table.setSortingEnabled(True)

    def closeEvent(self, QCloseEvent):
        self.close()
        global user
        user = []

    def UsComment(self):
        window.CommentF()

    def start(self):
        self.Login.setText(user[0])
        self.Status.setText(user[1])
        self.Box.clear()
        self.BandBox.clear()
        self.Table.setModel(None)
        if user[1] == 'Администратор':
            self.Box.addItem("Пользователи")
            self.Box.addItem("Фотографии")
            self.Box.addItem("Новости")
            self.Box.addItem("Аренда")
        self.Box.addItem("Приемка")
        self.Box.addItem("Записи")
        self.Box.addItem("Группы")
        self.Box.addItem("Коментарии")
        self.DayT.clear()
        self.DayT.insertPlainText(datetime.datetime.now().strftime("%d.%m.%Y") + '  Сегоднишние репетиции: \n')
        for i in self.sql.SelectOne('sing_up', 'id_nameB', 'date',
                                    "'" + datetime.datetime.now().strftime("%d.%m.%Y") + "'"):
            self.DayT.insertPlainText(self.sql.SelectOne('bands', 'nameB', 'ID', i)[0] + '\n')
        self.BandBox.addItems(self.sql.SelectOne('bands', 'nameB'))

    def newsAdminText(self):
        self.newsAd.show()

#
class NewsAdminForm(QtWidgets.QWidget):
    def __init__(self, sql, parent=None):
        super(QtWidgets.QWidget, self).__init__()
        self.sql = sql
        uic.loadUi("ui_NewsAdmin.ui", self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.CancelB.clicked.connect(self.close)
        self.EnterB.clicked.connect(self.enterNews)

    def enterNews(self):
        self.sql.Insert('news_admin', self.NewsT.toPlainText())
        self.close()

#
class CommentForm(QtWidgets.QWidget):
    def __init__(self, sql, parent=None):
        super(CommentForm, self).__init__()
        uic.loadUi("ui_Comment.ui", self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.CommentEnter.clicked.connect(self.ComEn)
        self.CommentExit.clicked.connect(self.close)
        self.sql = sql

    def ComEn(self):
        if len(user) == 0:
            self.sql.Insert('comments', 'Гость', self.textEdit.toPlainText())
            window.TableCommentUp()
            self.close()
        else:
            self.sql.Insert('comments', user[0], self.textEdit.toPlainText())
            window.TableCommentUp()
            self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    user = []
    window = MyWindow(user)
    window.showFullScreen()
    th = Thread()
    th.start()
    th.sig.connect(window.NewsN)
    th.sig.connect(window.PhotoN)
    th.sig.connect(window.us.time)
    sys.exit(app.exec_())

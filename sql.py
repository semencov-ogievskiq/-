from PyQt5 import QtWidgets, QtSql
import sys

class SqlCom():
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.con.setDatabaseName('rehearsal_base')
        self.con.open()
        self.query = QtSql.QSqlQuery()
        if 'news_admin' not in self.con.tables():
            self.query.exec("create table news_admin(ID integer not null primary key autoincrement, news text) ")
            self.query.prepare("insert into news_admin values(null,?)")
            self.query.addBindValue('Проба, ураааааа сработало!!!!')
            self.query.exec_()
        if 'photo' not in self.con.tables():
            self.query.exec("create table photo(ID integer not null primary key autoincrement, route text)")
            self.query.prepare("insert into photo values(null,?)")
            self.query.addBindValue('photo/1.jpg')
            self.query.exec_()
            self.query.prepare("insert into photo values(null,?)")
            self.query.addBindValue('photo/2.jpg')
            self.query.exec_()
        if 'comments' not in self.con.tables():
            self.query.exec("create table comments(ID integer not null primary key autoincrement, login text, comment text)")
            self.query.prepare("insert into comments values(null,?,?)")
            self.query.addBindValue('admin')
            self.query.addBindValue('работает, вроде')
            self.query.exec_()
            self.query.prepare("insert into comments values(null,?,?)")
            self.query.addBindValue('Гость')
            self.query.addBindValue('Чет пока тут пуста....')
            self.query.exec_()
        if 'users' not in self.con.tables():
            self.query.exec("create table users(ID integer not null primary key autoincrement, login text, password text,f text,i text,o text, phone integer, status text)")
            self.query.prepare("insert into users values(null,?,?,?,?,?,?,?)")
            self.query.addBindValue('admin')
            self.query.addBindValue('7291')
            self.query.addBindValue('Семенцов')
            self.query.addBindValue('Алексей')
            self.query.addBindValue('Михайлович')
            self.query.addBindValue('8998888888')
            self.query.addBindValue('Администратор')
            self.query.exec_()
        if 'bands' not in self.con.tables():
            self.query.exec("create table bands(ID integer not null primary key autoincrement, nameB text, data text)")
            self.query.prepare("insert into bands values(null,?,?)")
            self.query.addBindValue('Slipknot')
            self.query.addBindValue('Кори Тейлор - 89995674354')
            self.query.exec_()
        if 'rent' not in self.con.tables():
            self.query.exec("create table rent(ID integer not null primary key autoincrement, nameIns text, price integer)")
            self.query.prepare("insert into rent values(null,?,?)")
            self.query.addBindValue('Ibanez GIO')
            self.query.addBindValue('100')
            self.query.exec_()
        if 'sing_up' not in self.con.tables():
            self.query.exec("create table sing_up(ID integer not null primary key autoincrement, id_nameB INTEGER REFERENCES bands (ID) ON DELETE CASCADE ON UPDATE CASCADE, date integer , time text, timeEnd text, data text)")
            self.query.prepare("insert into sing_up values(null,?,?,?,?,?)")
            self.query.addBindValue('1')
            self.query.addBindValue('05.06.2017')
            self.query.addBindValue('12.00')
            self.query.addBindValue('11.00')
            self.query.addBindValue('Мик Томсон 89993216548')
            self.query.exec_()
        if 'pay' not in self.con.tables():
            self.query.exec("create table pay(ID integer not null primary key autoincrement, id_nameB INTEGER REFERENCES bands (ID) ON DELETE CASCADE ON UPDATE CASCADE, date text, time text,timeEnd text,nameIns text ,price integer)")
            self.query.prepare("insert into pay values(null,?,?,?,?,?,?)")
            self.query.addBindValue('1')
            self.query.addBindValue('05.06.2017')
            self.query.addBindValue('12.00')
            self.query.addBindValue('13.00')
            self.query.addBindValue('Ibanez GIO')
            self.query.addBindValue('1500')
            self.query.exec_()
        self.stm = QtSql.QSqlTableModel()
        self.stmR = QtSql.QSqlRelationalTableModel()
    def STMR(self,table,filt='',us=''):
        self.stmR.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.stmR.setTable(table)
        if filt !='':
            print("'"+filt+"'"+'='+"'"+us+"'")
            self.stmR.setFilter(filt+'='+"'"+us+"'")
        self.stmR.setRelation(1, QtSql.QSqlRelation('bands','ID','nameB'))
        self.stmR.select()
        return self.stmR

    def STM(self,table):
        self.stm.setTable(table)
        self.stm.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.stm.select()
        return self.stm

    def Delete(self,tabl,name, date):
        self.query.exec("delete from " + tabl+' where id_nameB='+"'"+str(name)+"'"+' and date='+"'"+date+"'")

    def Insert(self,tabl,data1,data2='',data3='',data4='',data5='',data6='',data7=''):
        if data2 != '':
            if data3 != '':
                if data4 != '':
                    if data5 !='':
                        if data6 !='':
                            if data7 != '':
                                self.query.prepare("insert into " + tabl + " values(null,?,?,?,?,?,?,?)")
                                self.query.addBindValue(data1)
                                self.query.addBindValue(data2)
                                self.query.addBindValue(data3)
                                self.query.addBindValue(data4)
                                self.query.addBindValue(data5)
                                self.query.addBindValue(data6)
                                self.query.addBindValue(data7)
                                self.query.exec_()
                                self.query.finish()
                            else:
                                self.query.prepare("insert into " + tabl + " values(null,?,?,?,?,?,?)")
                                self.query.addBindValue(data1)
                                self.query.addBindValue(data2)
                                self.query.addBindValue(data3)
                                self.query.addBindValue(data4)
                                self.query.addBindValue(data5)
                                self.query.addBindValue(data6)
                                self.query.exec_()
                                self.query.finish()
                        else:
                            self.query.prepare("insert into " + tabl + " values(null,?,?,?,?,?)")
                            self.query.addBindValue(data1)
                            self.query.addBindValue(data2)
                            self.query.addBindValue(data3)
                            self.query.addBindValue(data4)
                            self.query.addBindValue(data5)
                            self.query.exec_()
                            self.query.finish()
                    else:
                        self.query.prepare("insert into " + tabl + " values(null,?,?,?,?)")
                        self.query.addBindValue(data1)
                        self.query.addBindValue(data2)
                        self.query.addBindValue(data3)
                        self.query.addBindValue(data4)
                        self.query.exec_()
                        self.query.finish()
                else:
                    self.query.prepare("insert into " + tabl + " values(null,?,?,?)")
                    self.query.addBindValue(data1)
                    self.query.addBindValue(data2)
                    self.query.addBindValue(data3)
                    self.query.exec_()
                    self.query.finish()
            else:
                self.query.prepare("insert into " + tabl + " values(null,?,?)")
                self.query.addBindValue(data1)
                self.query.addBindValue(data2)
                self.query.exec_()
                self.query.finish()
        else:
            self.query.prepare("insert into " + tabl + " values(null,?)")
            self.query.addBindValue(data1)
            self.query.exec_()
            self.query.finish()

    def SelectMaxID(self,table):
        self.query.exec("select count(1) from " + table)
        lst = 0
        if self.query.isActive():
            self.query.first()
            lst=self.query.value('count(1)')
            self.query.next()
        return lst
    def SelectOne(self, table, column,columnS='',line=''):
        if columnS == '':
            self.query.exec("select * from "+table)
            lst=[]
            if self.query.isActive():
                self.query.first()
                while self.query.isValid():
                    lst.append(self.query.value(column))
                    self.query.next()
            return lst
        else:
            line=str(line)
            self.query.exec("select * from " + table+' where '+columnS+'='+line)
            lst = []
            if self.query.isActive():
                self.query.first()
                while self.query.isValid():
                    lst.append(self.query.value(column))
                    self.query.next()
            return lst






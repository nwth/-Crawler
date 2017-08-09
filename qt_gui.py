# coding=utf-8
'''
Created on 2016年5月24日
 @author: moverzp
 description: 使用pyqt4编写GUI界面
'''
import sys, os
from PyQt5.QtGui import *
from PyQt5  import *
import mongoDB, recommend
import operator
from PyQt5 import QtDialog
from PyQt5 import QtWidgets
from time import sleep

# reload(sys)
# sys.setdefaultencoding('utf-8')


#QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class MyGui(QDialog):
    
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self)
        self.mongodb = mongoDB.MongoDB() #数据库操作器
        self.recommend = recommend.Recommend() #推荐器
        self.spiderGui = SpiderGui()
        #函数
        self._init_gui()
        self._init_signal_slot()
        self._display_bookshelf()
        self._recommend_good_books()
        
        #变量
        #self.recommendUrls， 保存推荐书籍的url
        #self.searchDoc, 搜索栏cursor
        #self.bookshelfDoc, 书架栏cursor
        #self.bookshelfDoc2, 推荐栏cursor
          
    def _init_gui(self):
        self.setWindowTitle("GoodBooks")
        #搜索栏布局
        self.searchLabel = QtLabel(u'书名')
        self.searchEdit = QLineEdit()
        self.searchButton = QPushButton(u'搜索')
        self.searchTable = QTableWidget(0, 2)
        self.searchTable.setEditTriggers(QAbstractItemView.NoEditTriggers) #禁止编辑
        self.searchTable.setHorizontalHeaderLabels([u'书名', u'评分'])
        self.searchTable.setSelectionBehavior(QAbstractItemView.SelectRows)  #整行选中的方式
        self.searchTable.setColumnWidth(0, 220)
        self.searchTable.setColumnWidth(1, 30)
        self.spiderButton = QPushButton(u'爬虫窗口')
        
        searchLayout = QGridLayout()
        searchLayout.addWidget(self.searchLabel, 0, 0)
        searchLayout.addWidget(self.searchEdit, 0, 1)
        searchLayout.addWidget(self.searchButton, 0, 2)
        searchLayout.addWidget(self.searchTable, 1, 0, 1, 3)
        searchLayout.addWidget(self.spiderButton, 2, 0)
        
        #书籍栏布局
        self.bookNameLabel = QLabel(u'书名：')
        self.bookNameEdit = QLineEdit()
        #bookNameLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.scoreLabel = QtLabel(u'评分：')
        self.scoreEdit = QLineEdit()
        self.authorLabel = QLabel(u'作者：')
        self.authorEdit = QLineEdit()
        self.timeLabel = QLabel(u'出版时间：')
        self.timeEdit = QLineEdit()
        self.publisherLabel = QLabel(u'出版社：')
        self.publisherEdit = QLineEdit()
        self.urlLabel = QLabel(u'url')
        self.urlEdit = QLineEdit()
        self.introLabel = QLabel(u'简介：')
        self.introTextEdit = QTextEdit()
        self.hotReviewLabel = QLabel(u'评论：')
        self.hotReviewTextEdit = QTextEdit()
        self.joinBookShelf = QPushButton(u'加入书架')
        self.deleteFromBookShelf = QPushButton(u'从书架删除')
        
        bookLayout = QGridLayout()
        bookLayout.addWidget(self.bookNameLabel, 0, 0)
        bookLayout.addWidget(self.bookNameEdit, 0, 1)
        bookLayout.addWidget(self.scoreLabel, 1, 0)
        bookLayout.addWidget(self.scoreEdit, 1, 1)
        bookLayout.addWidget(self.authorLabel, 2, 0)
        bookLayout.addWidget(self.authorEdit, 2, 1)
        bookLayout.addWidget(self.timeLabel, 3, 0)
        bookLayout.addWidget(self.timeEdit, 3, 1)
        bookLayout.addWidget(self.publisherLabel, 4, 0)
        bookLayout.addWidget(self.publisherEdit, 4, 1)
        bookLayout.addWidget(self.urlLabel, 5, 0)
        bookLayout.addWidget(self.urlEdit, 5, 1)
        bookLayout.addWidget(self.introLabel, 6, 0, Qt.AlignTop)
        bookLayout.addWidget(self.introTextEdit, 6, 1)
        bookLayout.addWidget(self.joinBookShelf, 7, 1)
        bookLayout.addWidget(self.deleteFromBookShelf, 7, 2)
        bookLayout.addWidget(self.hotReviewLabel, 0, 2, Qt.AlignTop)
        bookLayout.addWidget(self.hotReviewTextEdit, 1, 2, 6, 1)
        
        #书架栏布局
        self.bookShelfLabel = QLabel(u'我的书架：')
        self.bookShelfTable = QTableWidget(0, 1)
        self.bookShelfTable.setEditTriggers(QAbstractItemView.NoEditTriggers) #禁止编辑
        self.bookShelfTable.setHorizontalHeaderLabels([u'书名'])
        self.bookShelfTable.setColumnWidth(0, 180) 
        
        bookShelfLayout = QVBoxLayout()
        bookShelfLayout.addWidget(self.bookShelfLabel)
        bookShelfLayout.addWidget(self.bookShelfTable)
 
        #推荐栏布局
        self.recommendTable = QTableWidget(2, 0)
        self.recommendTable.setVerticalHeaderLabels([u'书名', u'评分'])
        self.recommendTable.setEditTriggers(QAbstractItemView.NoEditTriggers) #禁止编辑
        self.recommendTable.setSelectionBehavior(QAbstractItemView.SelectColumns) #整列选中的方式
        self.recommendTable.resizeRowsToContents()
        
        recommendLayout = QGridLayout()
        recommendLayout.addWidget(self.recommendTable, 0, 0)
        
        #主布局
        mainLayout = QGridLayout(self)
        mainLayout.setSpacing(10)
        mainLayout.addLayout(searchLayout, 0, 0)
        mainLayout.addLayout(bookLayout, 0, 1, 1, 2)
        mainLayout.addLayout(bookShelfLayout, 0, 3)
        mainLayout.addLayout(recommendLayout, 1, 0, 1, 4)
        mainLayout.setRowStretch(0, 5)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(0, 4)
        #mainLayout.setColumnStretch(1, 2)
        mainLayout.setColumnStretch(3, 3)

        mainLayout.setSizeConstraint(QLayout.SetFixedSize) #固定对话框
        self.setWindowFlags(Qt.Window)
        
    def _init_signal_slot(self):
        self.connect(self.searchButton, SIGNAL('clicked()'), self.slot_search_keyword)
        self.connect(self.searchTable, SIGNAL('itemClicked (QTableWidgetItem *)'), self.slot_click_search_table)
        self.connect(self.spiderButton, SIGNAL('clicked()'), self.spiderGui.show)
        
        self.connect(self.joinBookShelf, SIGNAL('clicked()'), self.slot_join_bookshelf)
        self.connect(self.deleteFromBookShelf, SIGNAL('clicked()'), self.slot_delete_from_bookshelf)
        
        self.connect(self.bookShelfTable, SIGNAL('itemClicked (QTableWidgetItem *)'), self.slot_click_bookshelf_table)
        
        self.connect(self.recommendTable, SIGNAL('itemClicked (QTableWidgetItem *)'), self.slot_click_recommend_table)
        
    def _display_bookshelf(self):
        doc = self.mongodb.get_user_docs()
        self.bookshelfDoc = doc.clone()
        self.bookshelfDoc2 = doc.clone()
        #显示书架上的书
        self.bookShelfTable.clearContents()
        self.bookShelfTable.setRowCount(0)
        row = 0
        for i in doc:
            self.bookShelfTable.insertRow(row)
            self.bookShelfTable.setItem(row, 0, QTableWidgetItem( i['bookName'] ))
            row += 1
   
    def _display_recommend_books(self):
        self.recommendTable.clearContents()
        self.recommendTable.setColumnCount(0)
        column = 0
        for url in self.recommendUrls:
            book = self.mongodb.search_book_by_url(url)
            if book is None:
                continue
            self.recommendTable.insertColumn(column)
            self.recommendTable.setColumnWidth(column, 107)
            self.recommendTable.setItem(0, column, QTableWidgetItem( book['bookName'] ))
            self.recommendTable.setItem(1, column, QTableWidgetItem( book['score'] ))
            column += 1
    def _display_book_information(self, book):
        self.bookNameEdit.setText(book['bookName'].strip())
        self.scoreEdit.setText(book['score'].strip())
        self.authorEdit.setText(book['author'].strip())
        self.publisherEdit.setText(book['publisher'].strip())
        self.timeEdit.setText(book['time'].strip())
        self.urlEdit.setText(book['url'].strip())
        self.introTextEdit.setText(book['intro'])
        self.hotReviewTextEdit.setHtml(book['hotReview'])
            
    #槽函数    
    def slot_search_keyword(self):
        keyword = self.searchEdit.text()
        if keyword is None:
            return
        doc = self.mongodb.search_book(keyword)
        self.searchDoc = doc.clone() #保留光标
        #显示查询结果
        self.searchTable.clearContents()
        self.searchTable.setRowCount(0)
        row = 0
        for i in doc:
            self.searchTable.insertRow(row)
            self.searchTable.setItem(row, 0, QTableWidgetItem( i['bookName'] ))
            self.searchTable.setItem(row, 1, QTableWidgetItem( i['score'] ))
            row += 1
            
    def slot_click_search_table(self):
        curRow = self.searchTable.currentRow()
        book = self.searchDoc[curRow]
        self._display_book_information(book)
        
    def slot_click_bookshelf_table(self):
        curRow = self.bookShelfTable.currentRow()
        url = self.bookshelfDoc[curRow]['url']
        book = self.mongodb.search_book_by_url(url)
        self._display_book_information(book)
    
    def slot_click_recommend_table(self):
        curCol = self.recommendTable.currentColumn()
        url = self.recommendUrls[curCol]
        book = self.mongodb.search_book_by_url(url)
        self._display_book_information(book)
        
        
    def slot_join_bookshelf(self):
        book = {}
        book['bookName'] = str(self.bookNameEdit.text())
        book['url'] = str(self.urlEdit.text())
        self.mongodb.add_data_to_user(book)
        self._display_bookshelf()
        self._recommend_good_books()
        
    def slot_delete_from_bookshelf(self):
        url = str(self.urlEdit.text())
        self.mongodb.remove_data_from_user(url)
        self._display_bookshelf()
        self._recommend_good_books()
    
    
    
    
       
##############################################################################################
    def _recommend_good_books(self):
        #获取书架上所有书籍的url，并统计其频数
        urls = [] #保存推荐书籍url的频数
        for i in self.bookshelfDoc2:
            urls.append(i['url'])
        self.recommendUrls = self.recommend.itemCF(urls)
        #展示推荐书籍
        self._display_recommend_books()
 
import spider_main
class SpiderGui(QDialog):
    def __init__(self, parent = None):
        QWidget.__init__(self)
        self._init_gui()
        self._init_slot()
        self.spider = spider_main.SpiderMain()
    
    def _init_gui(self):
        self.setWindowTitle("Spider")

        self.urlLabel = QLabel(u'初始url：')
        self.urlEdit = QLineEdit()
        self.urlEdit.setText('https://book.douban.com/subject/1477390/')
        self.saveCookie1Button = QPushButton(u'保存cookie1')
        self.saveCookie2Button = QPushButton(u'保存cookie2')
        self.outputButton = QPushButton(u'导出xls文件')
        self.spideButton = QPushButton(u'开始爬取')
        
        icon = QPixmap('res/spiderIcon.jpg')
        iconLabel = QLabel()
        iconLabel.setPixmap(icon)
        
        layout = QGridLayout(self)
        layout.addWidget(self.urlLabel, 0, 0)
        layout.addWidget(self.urlEdit, 0, 1, 1, 3)
        layout.addWidget(iconLabel, 1, 0, 2, 1)
        layout.addWidget(self.saveCookie1Button, 1, 1)
        layout.addWidget(self.saveCookie2Button, 1, 2)
        layout.addWidget(self.outputButton, 1, 3)
        layout.addWidget(self.spideButton, 2, 1, 1, 3)
        
    def _init_slot(self):
        self.connect(self.saveCookie1Button, SIGNAL('clicked()'), self._saveCookie1)
        self.connect(self.saveCookie2Button, SIGNAL('clicked()'), self._saveCookie2)
        self.connect(self.spideButton, SIGNAL('clicked()'), self._spide)
        self.connect(self.outputButton, SIGNAL('clicked()'), self._output_xls)
    
    def _saveCookie1(self):
        self.spider.downloader.save_cookie("cookie1.txt", rootUrl) #未登录运行
    def _saveCookie2(self):
        self.spider.downloader.save_cookie("cookie2.txt", rootUrl) #登录运行
    def _output_xls(self):
        self.spider.mongodb.output_xls() #以xls格式输出爬取结果
        QMessageBox.information(self, u"通知", u"导出xls文件完成！")
    def _spide(self):
        cookie1Exist = os.path.exists('cookie1.txt')
        cookie2Exist = os.path.exists('cookie2.txt')
        if not cookie1Exist:
            QMessageBox.information(self,u"警告", u"cookie1.txt不存在，请先保存。")
            return
        if not cookie2Exist:
            QMessageBox.information(self,u"警告", u"cookie2.txt不存在，请先保存。")
            return
        url = str(self.urlEdit.text())
        self.spider.craw(url, 7.9)
        print 'All down!'
    
app=QApplication(sys.argv)
splash = QSplashScreen(QPixmap('res/startImage.jpg')) #启动图片
splash.show()
gui = MyGui()
#设置窗口图标
icon = QIcon()
icon.addPixmap(QPixmap('res/bookIcon.jpg'), QIcon.Normal, QIcon.Off)
gui.setWindowIcon(icon)
#显示主窗口
gui.show()
splash.finish(gui) #关闭启动图片

app.exec_()  
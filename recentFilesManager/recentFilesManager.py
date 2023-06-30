from PyQt5.QtWidgets import *
from krita import *

class rfmDocker(DockWidget):

    THUMBNAIL_HEIGHT=50
    RF_INDEX=0
    RF_PATH=1
    RF_NAME=2

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recent Files Manager")
        #everything is contained inside a scrollarea, to account for the possible
        #large number of recent files
        self.scroll=QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.setWidget(self.scroll)
        #the widget that will contain the update button and the list of
        #recent files
        self.mainWidget=QWidget(self.scroll)
        self.mainWidget.setLayout(QVBoxLayout())
        self.mainWidget.layout().setSpacing(0)
        self.scroll.setWidget(self.mainWidget)
        #a button that will update the list of recent files
        self.updateBtn=QPushButton()
        self.updateBtn.setText("Update List")
        self.updateBtn.clicked.connect(self.updateList)
        self.mainWidget.layout().addWidget(self.updateBtn)
        #a widget that contains all entries of the recent files list
        self.listHolder=QWidget(self.mainWidget)
        self.listHolder.setLayout(QVBoxLayout())
        self.listHolder.layout().setContentsMargins(0,10,0,0)
        self.mainWidget.layout().addWidget(self.listHolder)
        #lists of buttons for each recent file
        #this is used to be able to reference each button afterward
        self.removeBtnList=[]
        self.moveUpBtnList=[]
        self.moveDownBtnList=[]
        self.fileEntriesList=[]
        self.recentFiles=self.getRecentFiles()
        #populate the list
        self.createList()

    def canvasChanged(self, canvas):
        pass

    def openDocument(self,filename):
        d=Krita.instance().openDocument(filename)
        Krita.instance().activeWindow().addView(d)

    #returns a list of recent files as tuples (I,F,N), where:
    #I is the index number of the file, as given in the config file kritarc
    #F is the path of the file, as given by its FileX entry in the config file
    #N is the name of the file, as given by its NameX entry in the config file
    def getRecentFiles(self):
        returnRecentFiles=[]
        for index in range(len(Krita.instance().recentDocuments())):
            if Krita.instance().recentDocuments()[index].strip()=="":
                continue
            returnRecentFiles.append((index,Krita.instance().readSetting("RecentFiles",f"File{index}",""),Krita.instance().readSetting("RecentFiles",f"Name{index}","")))
        return returnRecentFiles

    def updateList(self):
        self.updateBtn.setText("Updating...")
        self.updateBtn.setEnabled(False)
        #clear widget list
        for entryIndex in range(self.listHolder.layout().count()):
            self.listHolder.layout().itemAt(0).widget().setParent(None)
        self.recentFiles=self.getRecentFiles()
        self.createList()
        self.updateBtn.setEnabled(True)
        self.updateBtn.setText("Update List")

    def clickWidget(self, event, filename):
        self.openDocument(filename)

    def createList(self):
        self.removeBtnList=[]
        self.moveUpBtnList=[]
        self.moveDownBtnList=[]
        self.fileEntriesList=[]
        self.fileLabels=[]
        rfCount=0
        #for each recent file, show "up" and "down" move buttons, thumbnail, name, and a "remove" button
        for rf in self.recentFiles:
            #each recent file is displayed in a new widget
            fileWidget=QWidget(self.listHolder)
            fileWidget.setLayout(QHBoxLayout())
            fileWidget.layout().setContentsMargins(0,0,0,0)
            fileWidget.layout().setSpacing(0)
            self.fileEntriesList.append(fileWidget)
            self.listHolder.layout().addWidget(fileWidget)
            #the move buttons are within a holder
            moveButtonHolder=QWidget(fileWidget)
            moveButtonHolder.setLayout(QVBoxLayout())
            moveButtonHolder.setFixedWidth(20)
            moveButtonHolder.layout().setSpacing(0)
            moveButtonHolder.layout().setContentsMargins(0,0,0,0)
            fileWidget.layout().addWidget(moveButtonHolder)
            #first element is the moveUp button
            self.moveUpBtnList.append(QToolButton(fileWidget))
            self.moveUpBtnList[rfCount].setContentsMargins(0,0,0,0)
            self.moveUpBtnList[rfCount].setIcon(Krita.instance().icon("arrow-up"))
            self.moveUpBtnList[rfCount].setToolTip("Move up")
            self.moveUpBtnList[rfCount].setStyleSheet("border:none")
            self.moveUpBtnList[rfCount].clicked.connect(lambda check,index=rfCount:self.moveUpRecentFile(check,index))
            moveButtonHolder.layout().addWidget(self.moveUpBtnList[rfCount])
            #the first file (rfCount==0) shouldn't have it, so it is hidden
            if rfCount==0:
                self.moveUpBtnList[rfCount].hide()
            #second element is the moveDown button
            self.moveDownBtnList.append(QToolButton(fileWidget))
            self.moveDownBtnList[rfCount].setContentsMargins(0,0,0,0)
            self.moveDownBtnList[rfCount].setIcon(Krita.instance().icon("arrow-down"))
            self.moveDownBtnList[rfCount].setToolTip("Move down")
            self.moveDownBtnList[rfCount].setStyleSheet("border:none")
            self.moveDownBtnList[rfCount].clicked.connect(lambda check,index=rfCount:self.moveDownRecentFile(check,index))
            moveButtonHolder.layout().addWidget(self.moveDownBtnList[rfCount])
            #the last file (rf[RF_INDEX]==len(self.recentFiles)) shouldn't  have it, so it is hidden
            if rfCount==len(self.recentFiles)-1:
                self.moveDownBtnList[rfCount].hide()
            #third element in the widget is the thumbnail
            #an "imgHolder" is used to scale the image without messing the layout
            imgHolder=QWidget()
            imgHolder.setLayout(QHBoxLayout())
            imgHolder.layout().setSpacing(0)
            imgHolder.layout().setContentsMargins(0,0,0,0)
            imgHolder.layout().setAlignment(Qt.AlignHCenter)
            imgHolder.setFixedSize(rfmDocker.THUMBNAIL_HEIGHT,rfmDocker.THUMBNAIL_HEIGHT)
            imgHolder.setStyleSheet("padding-left:4px")
            img = QPixmap(rf[rfmDocker.RF_PATH]).scaledToHeight(rfmDocker.THUMBNAIL_HEIGHT,Qt.SmoothTransformation)
            imgWidget=QLabel()
            imgWidget.setPixmap(img)
            imgHolder.layout().addWidget(imgWidget)
            fileWidget.layout().addWidget(imgHolder)
            imgWidget.show()
            #fourth element is the recent-file's name
            self.fileLabels.append(QLabel(fileWidget))
            self.fileLabels[rfCount].setText(rf[rfmDocker.RF_NAME])
            self.fileLabels[rfCount].setStyleSheet("padding-left:4px")
            fileWidget.layout().addWidget(self.fileLabels[rfCount])
            #fifth element is the remove button
            self.removeBtnList.append(QToolButton(fileWidget))
            self.removeBtnList[rfCount].setIcon(Krita.instance().icon("deletelayer"))
            self.removeBtnList[rfCount].setToolTip("Remove from Recent Files list")
            self.removeBtnList[rfCount].clicked.connect(lambda check,index=rfCount:self.removeRecentFile(check,index))
            fileWidget.layout().addWidget(self.removeBtnList[rfCount])
            self.fileEntriesList[rfCount].mouseReleaseEvent=lambda event, filename=rf[rfmDocker.RF_PATH]: self.openDocument(filename)
            rfCount+=1
        self.mainWidget.layout().addStretch()

    def moveUpRecentFile(self,check,index):
        #index can't be 0, and must stay within range of the recentFiles list size
        if index<1 or index>len(self.recentFiles):
            return
        #rearrange elements in the layout (remove it, then insert it before its previous element)
        self.listHolder.layout().removeWidget(self.fileEntriesList[index])
        self.listHolder.layout().insertWidget(index-1,self.fileEntriesList[index])
        #rewire remove button for new previous element
        self.removeBtnList[index].clicked.disconnect()
        self.removeBtnList[index].clicked.connect(lambda check,newIndex=index-1:self.removeRecentFile(check,newIndex))
        #rewire remove button for new next element
        self.removeBtnList[index-1].clicked.disconnect()
        self.removeBtnList[index-1].clicked.connect(lambda check,newIndex=index:self.removeRecentFile(check,newIndex))
        #rewire moveUp button for new previous element
        self.moveUpBtnList[index].clicked.disconnect()
        self.moveUpBtnList[index].clicked.connect(lambda check,newIndex=index-1:self.moveUpRecentFile(check,newIndex))
        #rewire moveUp button for new next element
        self.moveUpBtnList[index-1].clicked.disconnect()
        self.moveUpBtnList[index-1].clicked.connect(lambda check,newIndex=index:self.moveUpRecentFile(check,newIndex))
        #rewire moveUp button for new previous element
        self.moveDownBtnList[index].clicked.disconnect()
        self.moveDownBtnList[index].clicked.connect(lambda check,newIndex=index-1:self.moveDownRecentFile(check,newIndex))
        #rewire moveUp button for new next element
        self.moveDownBtnList[index-1].clicked.disconnect()
        self.moveDownBtnList[index-1].clicked.connect(lambda check,newIndex=index:self.moveDownRecentFile(check,newIndex))
        #if element was second (moved into first)
        if index==1:
            #hide its moveUp button and show moveUp button of new second element
            self.moveUpBtnList[index].hide()
            self.moveUpBtnList[index-1].show()
        #if element was last (moved into second-to-last)
        if index==len(self.recentFiles)-1:
            #show its moveDown button, and hide the moveDown button of the new last element
            self.moveDownBtnList[index].show()
            self.moveDownBtnList[index-1].hide()
        #swap elements in the config file
        movedFile=self.recentFiles[index][rfmDocker.RF_PATH]
        movedName=self.recentFiles[index][rfmDocker.RF_NAME]
        Krita.instance().writeSetting("RecentFiles",f"File{index+1}",self.recentFiles[index-1][rfmDocker.RF_PATH])
        Krita.instance().writeSetting("RecentFiles",f"Name{index+1}",self.recentFiles[index-1][rfmDocker.RF_NAME])
        Krita.instance().writeSetting("RecentFiles",f"File{index}",movedFile)
        Krita.instance().writeSetting("RecentFiles",f"Name{index}",movedName)
        #rearrange buttons and values in the respective lists
        self.removeBtnList.insert(index-1,self.removeBtnList.pop(index))
        self.moveDownBtnList.insert(index-1,self.moveDownBtnList.pop(index))
        self.moveUpBtnList.insert(index-1,self.moveUpBtnList.pop(index))
        self.fileEntriesList.insert(index-1,self.fileEntriesList.pop(index))
        self.fileLabels.insert(index-1,self.fileLabels.pop(index))
        self.recentFiles.insert(index-1,self.recentFiles.pop(index))

    def moveDownRecentFile(self,check,index):
        #index can't be 0, and must stay within range of the recentFiles list size
        if index<0 or index>len(self.recentFiles)-1:
            return
        #rearrange elements in the layout
        self.listHolder.layout().removeWidget(self.fileEntriesList[index])
        self.listHolder.layout().insertWidget(index+1,self.fileEntriesList[index])
        #rewire remove button for new previous element
        self.removeBtnList[index].clicked.disconnect()
        self.removeBtnList[index].clicked.connect(lambda check,newIndex=index+1:self.removeRecentFile(check,newIndex))
        #rewire remove button for new next element
        self.removeBtnList[index+1].clicked.disconnect()
        self.removeBtnList[index+1].clicked.connect(lambda check,newIndex=index:self.removeRecentFile(check,newIndex))
        #rewire moveUp button for new previous element
        self.moveUpBtnList[index].clicked.disconnect()
        self.moveUpBtnList[index].clicked.connect(lambda check,newIndex=index+1:self.moveUpRecentFile(check,newIndex))
        #rewire moveUp button for new next element
        self.moveUpBtnList[index+1].clicked.disconnect()
        self.moveUpBtnList[index+1].clicked.connect(lambda check,newIndex=index:self.moveUpRecentFile(check,newIndex))
        #rewire moveUp button for new previous element
        self.moveDownBtnList[index].clicked.disconnect()
        self.moveDownBtnList[index].clicked.connect(lambda check,newIndex=index+1:self.moveDownRecentFile(check,newIndex))
        #rewire moveUp button for new next element
        self.moveDownBtnList[index+1].clicked.disconnect()
        self.moveDownBtnList[index+1].clicked.connect(lambda check,newIndex=index:self.moveDownRecentFile(check,newIndex))
        #if element was moved into first
        if index==0:
            #hide its moveUp button and show moveUp button of new second element
            self.moveUpBtnList[index].show()
            self.moveUpBtnList[index+1].hide()
        #if element was moved into second-to-last
        if index==len(self.recentFiles)-2:
            #show its moveDown button, and hide the moveDown button of the new last element
            self.moveDownBtnList[index].hide()
            self.moveDownBtnList[index+1].show()
        #swap elements in the config file
        movedFile=self.recentFiles[index][rfmDocker.RF_PATH]
        movedName=self.recentFiles[index][rfmDocker.RF_NAME]
        Krita.instance().writeSetting("RecentFiles",f"File{index+1}",self.recentFiles[index+1][rfmDocker.RF_PATH])
        Krita.instance().writeSetting("RecentFiles",f"Name{index+1}",self.recentFiles[index+1][rfmDocker.RF_NAME])
        Krita.instance().writeSetting("RecentFiles",f"File{index+2}",movedFile)
        Krita.instance().writeSetting("RecentFiles",f"Name{index+2}",movedName)
        #rearrange buttons and values in the respective lists
        self.removeBtnList.insert(index+1,self.removeBtnList.pop(index))
        self.moveDownBtnList.insert(index+1,self.moveDownBtnList.pop(index))
        self.moveUpBtnList.insert(index+1,self.moveUpBtnList.pop(index))
        self.fileEntriesList.insert(index+1,self.fileEntriesList.pop(index))
        self.recentFiles.insert(index+1,self.recentFiles.pop(index))
        self.fileLabels.insert(index+1,self.fileLabels.pop(index))

    def removeRecentFile(self,check,rfIndex):
        numFiles=len(self.recentFiles)
        for i in range(rfIndex+1, numFiles):
            self.moveUpRecentFile(check,i)
        self.recentFiles.pop(numFiles-1)
        self.removeBtnList.pop(numFiles-1)
        self.moveUpBtnList.pop(numFiles-1)
        self.moveDownBtnList.pop(numFiles-1)
        self.fileEntriesList.pop(numFiles-1)
        self.listHolder.layout().itemAt(numFiles-1).widget().deleteLater()
        self.moveDownBtnList[-1].hide()
        Krita.instance().writeSetting("RecentFiles",f"File{numFiles}","")
        Krita.instance().writeSetting("RecentFiles",f"Name{numFiles}","")

    """
    #removes the file from the display list and from the RecentFiles configuration group
    def removeRecentFile(self,check,rfIndex):
        #remove the corresponding buttons and widgets (remove buttons from their lists)
        self.recentFiles.pop(rfIndex)
        self.removeBtnList.pop(rfIndex)
        self.moveUpBtnList.pop(rfIndex)
        self.moveDownBtnList.pop(rfIndex)
        self.fileEntriesList.pop(rfIndex)
        self.listHolder.layout().itemAt(rfIndex).widget().deleteLater()
        #replace the element with its next one, then repeat for each subsequent one
        #(disconnect its buttons, then connect them with the element that comes next (index+1))
        for i in range(rfIndex,len(self.recentFiles)):
            self.removeBtnList[i].clicked.disconnect()
            self.removeBtnList[i].clicked.connect(lambda check,index=i:self.removeRecentFile(check,index))
            self.moveUpBtnList[i].clicked.disconnect()
            self.moveUpBtnList[i].clicked.connect(lambda check,index=i:self.moveUpRecentFile(check,index))
            self.moveDownBtnList[i].clicked.disconnect()
            self.moveDownBtnList[i].clicked.connect(lambda check,index=i:self.moveDownRecentFile(check,index))
            Krita.instance().writeSetting("RecentFiles",f"File{i+1}",self.recentFiles[i][rfmDocker.RF_PATH])
            Krita.instance().writeSetting("RecentFiles",f"Name{i+1}",self.recentFiles[i][rfmDocker.RF_NAME])
        #remove from the config file (the last element has been duplicated. removing the copy)
        Krita.instance().writeSetting("RecentFiles",f"File{len(self.recentFiles)}","")
        Krita.instance().writeSetting("RecentFiles",f"Name{len(self.recentFiles)}","")
        if len(self.moveUpBtnList)>0 and self.moveUpBtnList[0]!=None:
            #first element removed; remove the new first element's moveUp button
            self.moveUpBtnList[0].setParent(None)
            self.moveUpBtnList[0]=None
        if len(self.moveDownBtnList)>0 and self.moveDownBtnList[-1]!=None:
            #last element removed; remove the new last element's moveDown button
            self.moveDownBtnList[-1].setParent(None)
            self.moveDownBtnList[-1]=None
        #TODO
    """

    def writeFile(index, filename):
        Krita.instance().writeSetting("RecentFiles",f"File{index+1}",filename)
        
    def writeName(index, name):
        Krita.instance().writeSetting("RecentFiles",f"Name{index+1}",name)

Krita.instance().addDockWidgetFactory(DockWidgetFactory("recentFilesManager",DockWidgetFactoryBase.DockRight, rfmDocker))
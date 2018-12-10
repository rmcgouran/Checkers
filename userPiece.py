class UserPiece():
    idVal = 0
    row = 0
    column = 0
    colour = ""
    king = False
    neNeighbour = []
    nwNeighbour = []
    seNeighhbor = []
    swNeighbour = []
    
    def __init__(self, row_, column_, colour_, king_, idVal_):
        self.row = row_
        self.column = column_
        self.king = king_
        self.colour = colour_
        self.idVal = idVal_
        self.assignNeighbours()
        
    def getRow(self):
        return self.row
    
    def getColumn(self):
        return self.column
    
    def getColour(self):
        return self.colour
    
    def isKing(self):
        return self.king
    
    def getIDVal(self):
        return self.idVal
    
    def setToKing(self):
        self.king = True
    
    def getNEneighbour(self):
        return self.neNeighbour
    
    def getNWneighbour(self):
        return self.nwNeighbour
    
    def getSEneighbour(self):
        return self.seNeighhbor
    
    def getSWneighbour(self):
        return self.swNeighbour
        
    #Description: assign the piece's neighbours tiles. If a neighbour tile does not exist, either its row or column will equal 100 
    def assignNeighbours(self):
        #Declare default values for function variables
        northRow = 100
        southRow = 100
        eastCol = 100
        westCol = 100
        
        #Check if the neighbouring row or column exists
        #If it does exists, save it to a variable
        if (self.row - 1) >= 0:
            northRow = self.row - 1
        if (self.row + 1) <= 7:
            southRow =  self.row + 1
        if (self.column - 1) >= 0:
            westCol = self.column - 1
        if (self.column + 1) <= 7:
            eastCol = self.column + 1
        
        #Assign all neighbours with variable values
        self.neNeighbour = (northRow, eastCol)
        self.nwNeighbour = (northRow, westCol)
        self.seNeighhbor = (southRow, eastCol)
        self.swNeighbour = (southRow, westCol)
    
    #Description: updates piece's location. reassigns neighbours, sets self to king if piece became a king
    def updateLocation(self, row_, column_):
        self.row = row_
        self.column = column_
        self.assignNeighbours()
        if row_ == 0 and self.colour == "red":
            if not self.isKing():
                self.setToKing()
        if row_ == 7 and self.colour == "grey":
            if not self.isKing():
                self.setToKing()
    
    def printLocation(self):
        print "Location: (%s, %s)" % (self.column, self.row)
    
    def printInfo(self):
        print "Location: (%s, %s)" % (self.column, self.row),
        print ("King: %s" % self.king)

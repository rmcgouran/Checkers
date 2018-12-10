import Tkinter
from Tkinter import *
from userPiece import UserPiece

class GameBoard(Canvas):
    gb = Tkinter.Tk()
    greyPieces = []
    redPieces = []
    board = []
    highlightedTiles = []
    currentlySelectedPieceObject = UserPiece(0, 0, "grey", False, 0)
    currentlySelectedPieceID = 0
    tileWidth = 31
    tileHeight = 31
    rows = 8
    columns = 8
    GREY_CHECKER = 1
    RED_CHECKER = 2
    tileBorder = .75
    pieceBorder = 4
    currentPlayer = "red"
    mustDoubleJump = False
    redCount = 12
    greyCount = 12
    redScoreBoard = Label(gb, text="Red: %i" % redCount)
    greyScoreBoard = Label(gb, text="Grey: %i" % greyCount)

    #Description: Start a new game. Reset all pieces to starting position
    def startNewGame(self):
        #Delete all pieces
        for i in self.greyPieces:
            self.delete(i[0])
        for i in self.redPieces:
            self.delete(i[0])

        #Delete all arrays storing pieces. (not the board array. That stores game tiles)
        for i in range(0, len(self.greyPieces)):
            self.greyPieces.pop()

        for i in range(0, len(self.redPieces)):
            self.redPieces.pop()

        for i in range(0, len(self.highlightedTiles)):
            self.highlightedTiles.pop()


        #Reset all variables (not reseting board)
        self.greyPieces = []
        self.redPieces = []
        self.highlightedTiles = []
        self.currentlySelectedPieceObject = UserPiece(0, 0, "grey", False, 0)
        self.currentlySelectedPieceID = 0
        self.currentPlayer = "red"
        self.mustDoubleJump = False
        self.redCount = 12
        self.greyCount = 12
        self.redScoreBoard.config(text="Red: %i" % self.redCount)
        self.greyScoreBoard.config(text="Grey: %i" % self.greyCount)

        #Make new pieces
        self.createPieces()


    #Description: Initializes main window, canvas, tiles, and pieces
    #Creates main window, canvas, tiles, and pieces
    def __init__(self):
        self.gb.minsize(500, 700)
        Canvas.__init__(self, self.gb, bg="grey", height=250, width=250)
        newGameButton = Button(self.gb, text="New Game", command=self.startNewGame)
        self.redScoreBoard.pack()
        self.greyScoreBoard.pack()
        self.pack()
        newGameButton.pack()
        self.createTiles()
        self.createPieces()
        self.gb.mainloop()


    #Description: Function creates red and black tiles for the game board
    def createTiles(self):
        width = self.tileWidth
        height = self.tileHeight
        for i in range(0, self.columns):
            x1 = (i * width) + self.tileBorder
            x2 = ((i + 1) * width) - self.tileBorder
            for j in range(0, self.rows):
                y1 = (j * height) + self.tileBorder
                y2 = ((j + 1) * height) - self.tileBorder
                idVal = 0
                if ((i + j) % 2 == 0):
                    idVal = self.create_rectangle(x1, y1, x2, y2, fill="red")
                else:
                    idVal = self.create_rectangle(x1, y1, x2, y2, fill="black")
                if idVal != 0:
                    self.board.append((idVal, j, i, x1, x2, y1, y2))

    #Description: Function places all pieces on the game board at their starting positions
    def createPieces(self):
        pieceWidth = self.tileWidth
        pieceHeight = self.tileWidth
        #Iterate over each row. Row indicates y position
        for i in range(0, self.rows):
            #No pieces are placed on the 3rd or 4th row, so continue to the next row in loop if i == 3 or 4
            if i == 3 or i == 4:
                continue
            #Calculate y1 and y2 of the oval that forms the piece
            y1 = (i * pieceWidth) + self.pieceBorder
            y2 = ((i + 1) * pieceWidth) - self.pieceBorder
            #Grey pieces are placed on rows 0-2
            if i < 3:
                pieceColour = "grey"
            #Red pieces are placed on rows 5-7
            elif i > 4:
                pieceColour = "red"
            #Iterate over each column in the row. Column indicates x position
            for j in range(0, self.columns):
                #If the sum of the row(i) and column(j) is odd, a piece should go in this cell
                if ((i + j) % 2 == 1):
                    #Calculate x1 and x2 of the oval that forms the piece
                    x1 = (j * pieceHeight) + self.pieceBorder
                    x2 = ((j + 1) * pieceHeight) - self.pieceBorder
                    #Draw the piece on the board, giving it a colour tag and an id tag
                    idTag = self.create_oval(x1, y1, x2, y2, fill=pieceColour)
                    self.tag_bind(idTag, "<ButtonPress-1>", self.processPieceClick)
                    #Create a piece object to keep track of this newly created piece
                    newPiece = UserPiece(i, j, pieceColour, False, idTag)
                    #Append the id and piece object to their proper arrays
                    if pieceColour == "grey":
                        self.greyPieces.append((idTag, newPiece))
                    elif pieceColour == "red":
                        self.redPieces.append((idTag, newPiece))

    #Description: Process the user clicking a piece
    def processPieceClick(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        idValue = self.find_closest(x, y)[0]
        selectedPiece = self.getPieceObject(idValue)
        #If selectedPiece == 0, the idValue passed to getPieceObject does not match any known idValues
        if selectedPiece == 0:
            return
        #Only process click if currentPlayer == selectedPiece's colour
        if (self.currentPlayer == selectedPiece.getColour()) and (self.mustDoubleJump == False):
            #Assign the currentlySelectedPieceObject and currentlySelectedPieceID
            self.currentlySelectedPieceObject = selectedPiece
            self.currentlySelectedPieceID = idValue
            #Reset all highlighted tiles
            self.resetHighlightedTiles()
            #Show all available moves for the selected piece
            self.showAllAvailableRegularMoves(selectedPiece)
            #Show all available jump moves for the selected piece
            self.showAllAvailableJumpMoves(selectedPiece)


    #Description: process the user selecting a highlighted tile
    def processHighlightedTileClicked(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        idValue = self.find_closest(x, y)[0]
        #Find the new row and column to move the currently selected piece to
        newRow = 100
        newCol = 100
        jumpedPieceID = 0
        for i in self.board:
            if i[0] == idValue:
                newRow = i[1]
                newCol = i[2]
                jumpedPieceID = self.getJumpedPieceID(newRow, newCol)
                break
        #If newRow == 100, invalid tile was selected
        if newRow == 100:
            return

        #Move the currently selected piece to the tile with the selected idVal
        self.moveCurrentlySelectedPiece(newRow, newCol)
        #Reset all highlighted tiles
        self.resetHighlightedTiles()
        #If the selected piece made a jump, remove the jumped piece, show the current piece more jump moves
        if jumpedPieceID != 0:
            self.removePiece(jumpedPieceID)
            self.showAllAvailableJumpMoves(self.currentlySelectedPieceObject)
            #If there are jumps left for the player, set the mustDoubleJump flag to true
            if len(self.highlightedTiles) > 0:
                self.mustDoubleJump = True
            #Else if there are no jumps left for the player, set the mustDoubleJump flag to false and switch players
            else:
                self.switchCurrentPlayer()
                self.mustDoubleJump = False
        #If the selected piece was just a normal move, switch players
        else:
            self.switchCurrentPlayer()

    #Description: Switch the current player to the next player
    def switchCurrentPlayer(self):
        if self.currentPlayer == "red":
            self.currentPlayer = "grey"
        elif self.currentPlayer == "grey":
            self.currentPlayer = "red"

    #Description: Remove piece from the board and its respective piece array
    def removePiece(self, pieceID):
        if pieceID != 0:
            self.delete(pieceID)
            for i in self.redPieces:
                if i[0] == pieceID:
                    self.redPieces.remove(i)
                    self.redCount = self.redCount - 1
                    self.redScoreBoard.config(text="Red: %i" % self.redCount)
                    break
            for i in self.greyPieces:
                if i[0] == pieceID:
                    self.greyPieces.remove(i)
                    self.greyCount = self.greyCount - 1
                    self.greyScoreBoard.config(text="Grey: %i" % self.greyCount)
                    break
            self.checkForWin()

    #Description: Check if red or grey has won. If so, congratulate them
    def checkForWin(self):
        if self.redCount <= 0:
            greyWinnerLabel = Label(self.gb, text="Grey Wins!")
            greyWinnerLabel.pack()
            self.stopTheGame()
        elif self.greyCount <= 0:
            redWinnerLabel = Label(self.gb, text="Red Wins!")
            redWinnerLabel.pack()
            self.stopTheGame()

    #Description: Stops the game by unbinding all events
    def stopTheGame(self):
        for i in self.redPieces:
            pieceIDVal = i[0]
            if pieceIDVal != 0:
                self.tag_unbind(pieceIDVal, "<ButtonPress-1>")
        for i in self.greyPieces:
            pieceIDVal = i[0]
            if pieceIDVal != 0:
                self.tag_unbind(pieceIDVal, "<ButtonPress-1>")
        self.resetHighlightedTiles()


    #Description: given row and column, get jumped piece id
    def getJumpedPieceID(self, row_, col_):
        for i in self.highlightedTiles:
            if row_ == i[0] and col_ == i[1]:
                return i[2]
        return 0

    #Description: move the currently selected piece to (newRow_, newCol_)
    def moveCurrentlySelectedPiece(self, newRow_, newCol_):
        y1 = (newRow_ * self.tileWidth) + self.pieceBorder
        y2 = ((newRow_ + 1) * self.tileWidth) - self.pieceBorder
        x1 = (newCol_ * self.tileWidth) + self.pieceBorder
        x2 = ((newCol_ + 1) * self.tileWidth) - self.pieceBorder
        #Move piece to new location
        self.coords(self.currentlySelectedPieceID, (x1, y1, x2, y2))
        #Update currentlySelectedPiece's location
        self.currentlySelectedPieceObject.updateLocation(newRow_, newCol_)
        if self.currentlySelectedPieceObject.isKing():
            self.itemconfig(self.currentlySelectedPieceID, outline="cyan")


    #Description: reset all highlighted tiles to black borders instead of yellow
    #                unbind all events the highlighted tiles had
    def resetHighlightedTiles(self):
        #Reset all currently highlighted cells
        for i in self.highlightedTiles:
            tileIDVal = self.getTileID(i[0], i[1])
            if tileIDVal != 0:
                self.itemconfig(tileIDVal, outline="black")
                self.tag_unbind(tileIDVal, "<ButtonPress-1>")

        #Remove all current values from highlightedTiles
        for i in range(0, len(self.highlightedTiles)):
            self.highlightedTiles.pop()


    #Description: show available moves for a selected piece
    def showAllAvailableRegularMoves(self, _selectedPiece):
        selectedPiece = _selectedPiece
        selectedPieceIsKing = selectedPiece.isKing()
        selectedPieceColour = selectedPiece.getColour()
        openSpaces = []

        if selectedPieceIsKing:
            #Check north west neighbour
            rowValue = selectedPiece.getNWneighbour()[0]
            colValue = selectedPiece.getNWneighbour()[1]
            if (not self.isTileOccupied(rowValue, colValue)[0]):
                openSpaces.append(selectedPiece.getNWneighbour())

            #Check north east neighbour
            rowValue = selectedPiece.getNEneighbour()[0]
            colValue = selectedPiece.getNEneighbour()[1]
            if (not self.isTileOccupied(rowValue, colValue)[0]):
                openSpaces.append(selectedPiece.getNEneighbour())

            #Check south west neighbour
            rowValue = selectedPiece.getSWneighbour()[0]
            colValue = selectedPiece.getSWneighbour()[1]
            if (not self.isTileOccupied(rowValue, colValue)[0]):
                openSpaces.append(selectedPiece.getSWneighbour())

            #Check south east neighbour
            rowValue = selectedPiece.getSEneighbour()[0]
            colValue = selectedPiece.getSEneighbour()[1]
            if (not self.isTileOccupied(rowValue, colValue)[0]):
                openSpaces.append(selectedPiece.getSEneighbour())
        #Else if piece is normal and red, only check north west and north east
        elif selectedPieceColour == "red":
            #Check north west neighbour
            rowValue = selectedPiece.getNWneighbour()[0]
            colValue = selectedPiece.getNWneighbour()[1]
            if (not self.isTileOccupied(rowValue, colValue)[0]):
                openSpaces.append(selectedPiece.getNWneighbour())

            #Check north east neighbour
            rowValue = selectedPiece.getNEneighbour()[0]
            colValue = selectedPiece.getNEneighbour()[1]
            if (not self.isTileOccupied(rowValue, colValue)[0]):
                openSpaces.append(selectedPiece.getNEneighbour())
        #Else if piece is normal and grey, only check south west and south east
        elif selectedPieceColour == "grey":
            #Check south west neighbour
            rowValue = selectedPiece.getSWneighbour()[0]
            colValue = selectedPiece.getSWneighbour()[1]
            if (not self.isTileOccupied(rowValue, colValue)[0]):
                openSpaces.append(selectedPiece.getSWneighbour())

            #Check south east neighbour
            rowValue = selectedPiece.getSEneighbour()[0]
            colValue = selectedPiece.getSEneighbour()[1]
            if (not self.isTileOccupied(rowValue, colValue)[0]):
                openSpaces.append(selectedPiece.getSEneighbour())

        #Highlight all open spaces
        for i in range(0, len(openSpaces)):
            highlightRow = openSpaces[i][0]
            highlightCol = openSpaces[i][1]
            if highlightRow == 100 or highlightCol == 100:
                continue
            tileIDVal = self.getTileID(highlightRow, highlightCol)
            if tileIDVal != 0:
                self.itemconfig(tileIDVal, outline="yellow")
                self.tag_bind(tileIDVal, "<ButtonPress-1>", self.processHighlightedTileClicked)
                self.highlightedTiles.append((highlightRow, highlightCol, 0))
            else:
                print "Invalid tile"

    #Description: Show all available jump moves a selected piece can make
    def showAllAvailableJumpMoves(self, selectedPiece_):
        selectedPiece = selectedPiece_
        selectedPieceIsKing = selectedPiece.isKing()
        selectedPieceColour = selectedPiece.getColour()

        if selectedPieceIsKing:
            #Check north west neighbour
            rowValue = selectedPiece.getNWneighbour()[0]
            colValue = selectedPiece.getNWneighbour()[1]
            isTileOccupiedReturnArray = self.isTileOccupied(rowValue, colValue)
            isTileOccupied = isTileOccupiedReturnArray[0]
            tileColour = isTileOccupiedReturnArray[1]
            jumpPieceID = isTileOccupiedReturnArray[2]
            if isTileOccupied:
                if selectedPieceColour != tileColour:
                    jumpRow = selectedPiece.getNWneighbour()[0]
                    jumpCol = selectedPiece.getNWneighbour()[1]
                    self.checkForJump(jumpRow - 1, jumpCol - 1, jumpPieceID)

            #Check north east neighbour
            rowValue = selectedPiece.getNEneighbour()[0]
            colValue = selectedPiece.getNEneighbour()[1]
            isTileOccupiedReturnArray = self.isTileOccupied(rowValue, colValue)
            isTileOccupied = isTileOccupiedReturnArray[0]
            tileColour = isTileOccupiedReturnArray[1]
            jumpPieceID = isTileOccupiedReturnArray[2]
            if isTileOccupied:
                if selectedPieceColour != tileColour:
                    jumpRow = selectedPiece.getNEneighbour()[0]
                    jumpCol = selectedPiece.getNEneighbour()[1]
                    self.checkForJump(jumpRow - 1, jumpCol + 1, jumpPieceID)

            #Check south west neighbour
            rowValue = selectedPiece.getSWneighbour()[0]
            colValue = selectedPiece.getSWneighbour()[1]
            isTileOccupiedReturnArray = self.isTileOccupied(rowValue, colValue)
            isTileOccupied = isTileOccupiedReturnArray[0]
            tileColour = isTileOccupiedReturnArray[1]
            jumpPieceID = isTileOccupiedReturnArray[2]
            if isTileOccupied:
                if selectedPieceColour != tileColour:
                    jumpRow = selectedPiece.getSWneighbour()[0]
                    jumpCol = selectedPiece.getSWneighbour()[1]
                    self.checkForJump(jumpRow + 1, jumpCol - 1, jumpPieceID)

            #Check south east neighbour
            rowValue = selectedPiece.getSEneighbour()[0]
            colValue = selectedPiece.getSEneighbour()[1]
            isTileOccupiedReturnArray = self.isTileOccupied(rowValue, colValue)
            isTileOccupied = isTileOccupiedReturnArray[0]
            tileColour = isTileOccupiedReturnArray[1]
            jumpPieceID = isTileOccupiedReturnArray[2]
            if isTileOccupied:
                if selectedPieceColour != tileColour:
                    jumpRow = selectedPiece.getSEneighbour()[0]
                    jumpCol = selectedPiece.getSEneighbour()[1]
                    self.checkForJump(jumpRow + 1, jumpCol + 1, jumpPieceID)

        #Else if piece is a normal, red piece, check the north west and north east neighbours
        elif selectedPieceColour == "red":
            #Check north west neighbour
            rowValue = selectedPiece.getNWneighbour()[0]
            colValue = selectedPiece.getNWneighbour()[1]
            isTileOccupiedReturnArray = self.isTileOccupied(rowValue, colValue)
            isTileOccupied = isTileOccupiedReturnArray[0]
            tileColour = isTileOccupiedReturnArray[1]
            jumpPieceID = isTileOccupiedReturnArray[2]
            if isTileOccupied:
                if selectedPieceColour != tileColour:
                    jumpRow = selectedPiece.getNWneighbour()[0]
                    jumpCol = selectedPiece.getNWneighbour()[1]
                    self.checkForJump(jumpRow - 1, jumpCol - 1, jumpPieceID)

            #Check north east neighbour
            rowValue = selectedPiece.getNEneighbour()[0]
            colValue = selectedPiece.getNEneighbour()[1]
            isTileOccupiedReturnArray = self.isTileOccupied(rowValue, colValue)
            isTileOccupied = isTileOccupiedReturnArray[0]
            tileColour = isTileOccupiedReturnArray[1]
            jumpPieceID = isTileOccupiedReturnArray[2]
            if isTileOccupied:
                if selectedPieceColour != tileColour:
                    jumpRow = selectedPiece.getNEneighbour()[0]
                    jumpCol = selectedPiece.getNEneighbour()[1]
                    self.checkForJump(jumpRow - 1, jumpCol + 1, jumpPieceID)

        elif selectedPieceColour == "grey":
            #Check south west neighbour
            rowValue = selectedPiece.getSWneighbour()[0]
            colValue = selectedPiece.getSWneighbour()[1]
            isTileOccupiedReturnArray = self.isTileOccupied(rowValue, colValue)
            isTileOccupied = isTileOccupiedReturnArray[0]
            tileColour = isTileOccupiedReturnArray[1]
            jumpPieceID = isTileOccupiedReturnArray[2]
            if isTileOccupied:
                if selectedPieceColour != tileColour:
                    jumpRow = selectedPiece.getSWneighbour()[0]
                    jumpCol = selectedPiece.getSWneighbour()[1]
                    self.checkForJump(jumpRow + 1, jumpCol - 1, jumpPieceID)

            #Check south east neighbour
            rowValue = selectedPiece.getSEneighbour()[0]
            colValue = selectedPiece.getSEneighbour()[1]
            isTileOccupiedReturnArray = self.isTileOccupied(rowValue, colValue)
            isTileOccupied = isTileOccupiedReturnArray[0]
            tileColour = isTileOccupiedReturnArray[1]
            jumpPieceID = isTileOccupiedReturnArray[2]
            if isTileOccupied:
                if selectedPieceColour != tileColour:
                    jumpRow = selectedPiece.getSEneighbour()[0]
                    jumpCol = selectedPiece.getSEneighbour()[1]
                    self.checkForJump(jumpRow + 1, jumpCol + 1, jumpPieceID)

    #Description: Highlight square if jump tile is not occupied
    def checkForJump(self, row_, col_, jumpedPieceID_):
        #If row_ and col_ are not on the board, return
        if not self.isValidPosition(row_, col_):
            return 0
        #If tile is not occupied, highlight it
        if not self.isTileOccupied(row_, col_)[0]:
            tileIDVal = self.getTileID(row_, col_)
            if tileIDVal != 0:
                self.itemconfig(tileIDVal, outline="yellow")
                self.tag_bind(tileIDVal, "<ButtonPress-1>", self.processHighlightedTileClicked)
                self.highlightedTiles.append((row_, col_, jumpedPieceID_))


    #Description: Checks if tile described by the rowVal and colVal is occupied
    #                If occupied, returns (True, <colourOfPieceOccupyingTheTile> , <idOfPieceOccupyingTheTile>)
    #                If not occupied, returns (False, "NA", 0)
    def isTileOccupied(self, rowVal, colVal):
        row = rowVal
        col = colVal

        if (not self.isValidPosition(row, col)):
            return (False, "NA", 0)

        #Check if any grey pieces are in the tile
        for i in range(0, len(self.greyPieces)):
            currentPiece = self.greyPieces[i][1]
            if (row == currentPiece.getRow()) and (col == currentPiece.getColumn()):
                return (True, "grey", self.greyPieces[i][0])

        #Check if any red pieces are in the tile
        for i in range(0, len(self.redPieces)):
            currentPiece = self.redPieces[i][1]
            if (row == currentPiece.getRow()) and (col == currentPiece.getColumn()):
                return (True, "red", self.redPieces[i][0])

        #No pieces found in the tile, return (False, "NA", 0)
        return (False, "NA", 0)


    #Description: returns the piece object representing the passed id value
    def getPieceObject(self, idValue):
        #Check greyPieces for id
        for i in range(0, len(self.greyPieces)):
            if self.greyPieces[i][0] == idValue:
                return self.greyPieces[i][1]

        #Check redPieces for id
        for i in range(0, len(self.redPieces)):
            if self.redPieces[i][0] == idValue:
                return self.redPieces[i][1]

        #If no piece found, return 0
        return 0

    #Description: Return the tileID of the tile found at (row_, col_)
    def getTileID(self, row_, col_):
        row = row_
        col = col_
        for i in range(0, len(self.board)):
            if row == self.board[i][1] and col == self.board[i][2]:
                return self.board[i][0]
        return 0

    #Description: Return true if the position is valid
    def isValidPosition(self, row_, col_):
        return self.isValidRow(row_) and self.isValidColumn(col_)

    #Description: Return true if the row is valid
    def isValidRow(self, row_):
        if (row_ >= 0 and row_ <= 7):
            return True
        else:
            return False

    #Description: Return true if the col is valid
    def isValidColumn(self, col_):
        if (col_ >= 0 and col_ <= 7):
            return True
        else:
            return False

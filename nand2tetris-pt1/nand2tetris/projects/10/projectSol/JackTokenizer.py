import re
class JackTokenizer():
    """
    
    """
    def __init__(self,inputFile):
        self.writeToFile = ''
        self.fileLines = self.readFile(inputFile)
        
        self.removeNextLine = False
        self.symbols = [
            '{' , '}' , '(' ,')' , '[' , ']' , '.' ,',' ,';' , '+' ,'-' ,'*' ,'/' ,'&' ,'|' ,'<' ,'>' ,'=' ,'~']
        self.keywords = [
            'class' ,'constructor' ,'function' ,'method' ,'field' ,'static' ,'var' ,'int' ,'char' ,'boolean' ,'void' ,'true' ,'false' ,'null' ,'this' ,'let' , 'do' ,'if' ,'else' ,'while' ,'return']
        
        self.tokenList = [] 
        self.currentToken = -1 
        # Fill in the tokenList 
        self.tokenz()
        self.nToken = len(self.tokenList)
        self.outputXML()

        # self.ListReadable(self.tokenList)

        # print(self.tokenList)
        # print(self.tokenList[30])
        # print(self.tokenList[33])



    def ListReadable(self,fileList):
        [print(line) for line in fileList]

    def readFile(self,fileName):
        # Check if its right extention
        pattern = re.compile(r'.*[.]jack')
        match = re.match(pattern,fileName)
        if match:
            self.writeToFile = fileName.partition('.')[0]
            with open(fileName, 'r') as reader:
                lines = reader.readlines()
                return lines
        else:
            raise "File Extenstion not supported"

        
    def filterLine(self,line): # remove white spaces and stand-alone line comments
        lineList = line.split()
        return ((lineList == []) or (lineList[0] == '//'))

    def clean(self,line): 
        triple = line.partition('//') # Remove in-line comments
        token  = triple[0].rstrip('\n') # Remove '\n' chars
        token  = token.strip()  # Remove leading and trailing whitespaces
        return token
    
    def blockComment(self,line):
        isBlockComment  =   (line.partition('/*')[1] == '/*') 
        isBlockEnded    =   (line.partition('*/')[1] == '*/') 
        if (isBlockComment and isBlockEnded) : # /** ..  */
            self.removeNextLine = False
        elif ( isBlockComment and (not isBlockEnded) ):  # /** ..
            self.removeNextLine = True
        elif (isBlockEnded): # .. */
            self.removeNextLine = False
        return isBlockComment or self.removeNextLine or isBlockEnded
            
         
    def filter(self,fileList):
        filterList = [ self.clean(line) for line in fileList if not (self.blockComment(line) or  self.filterLine(line)) ]    
        return filterList
    
    def splitOnSymbols(self,line):
        tokens = re.split(r'([^a-zA-Z0-9"?:])',line) # split on every thing except digits and chars
        tokens = [token for token in tokens if not ((token == ' ') or (token == ''))]   # remove empty strings
        return tokens
     
    def fixStringConst(self):
        startIndex = 0
        endIndex = 0
        openQuote = True
        mergeIndecies = []
        startStringPattern = re.compile(r'^\".*')
        endStringPattern = re.compile(r'.*\"$')
        for i,token in enumerate(self.tokenList) :
            # print(f'token:{token}')
            starMatch = re.match(startStringPattern,token)
            # starMatch = list(token)[0] == '"'
            endMatch = re.match(endStringPattern,token)
            # endMatch =  list(token)[-1] == '"'
            if starMatch and  openQuote:
                startIndex = i 
                openQuote = False
                print(startIndex)
            elif endMatch:
                endIndex = i 
                openQuote = True
                mergeIndecies.insert(0,(startIndex,endIndex))
        print(mergeIndecies)
        for i in range(len(mergeIndecies)):
            start = mergeIndecies[i][0]
            end = mergeIndecies[i][1]
            self.tokenList[start:end+1] = [' '.join(self.tokenList[start:end+1])]

    def tokenz(self):
            filteredFileLines = self.filter(self.fileLines)  # list of lines without comments and whitespaces
            splitedLines = [self.splitOnSymbols(filteredLine) for filteredLine in filteredFileLines]
            tokensList = [token for splitedLine in splitedLines for token in splitedLine]
            # tokensList = splitedLines
            self.tokenList = tokensList
            self.fixStringConst()

    def hasMoreTokens(self):
        
        if self.currentToken < (self.nToken - 1) :
            return True
        else:
            return False

    def advance(self):
        if self.hasMoreTokens():
            
            self.currentToken = self.currentToken + 1 
        else :
            raise "Can't be called -- No more Tokens left!"
        

    def tokenType(self):
        current = self.tokenList[self.currentToken]
        if current in self.keywords:
            return 'KEYWORD'
        
        elif current in self.symbols:
            return 'SYMBOL'
        elif list(current)[0] == '"':
            return 'STRING_CONST'
        else:
            try:
                int(current)
                return 'INT_CONST'
            except:
                return 'IDENTIFIER'

    def keyWord(self):
        if self.tokenType() == 'KEYWORD':
            return self.tokenList[self.currentToken]

    def symbol(self):

        if self.tokenType() == 'SYMBOL':
            symbol = self.tokenList[self.currentToken]
            if symbol == '<':return '&lt;'
            elif symbol == '>':return '&gt;'
            elif symbol == '&':return '&amp;'
            elif symbol == '"':return '&quot;'
            else: return symbol
            

    def identifier(self):
        if self.tokenType() == 'IDENTIFIER':
            return self.tokenList[self.currentToken]

    def intVal(self):
        if self.tokenType() == 'INT_CONST':
            return int(self.tokenList[self.currentToken])

    def stringVal(self):
        if self.tokenType() == 'STRING_CONST':
            return self.tokenList[self.currentToken].split('"')[1]

    def handleTokenTags(self):
        tokenType = self.tokenType()
        if tokenType == 'KEYWORD':
            return f'<keyword> {self.keyWord()} </keyword>'
        elif tokenType == 'SYMBOL':
            return f'<symbol> {self.symbol()} </symbol>'
        elif tokenType == 'STRING_CONST':
            return f'<stringConstant> {self.stringVal()} </stringConstant>'
        elif tokenType == 'INT_CONST':
            return f'<integerConstant> {self.intVal()} </integerConstant>'
        elif tokenType == 'IDENTIFIER':
            return f'<identifier> {self.identifier()} </identifier>'



    def outputXML(self):
        with open( self.writeToFile + 'TMine.xml' , 'w') as writer:
            
            writer.write('<tokens>' + '\n')
            while self.hasMoreTokens():
                self.advance()
                writer.write(self.handleTokenTags() + '\n')
            writer.write('</tokens>' + '\n')



        


tokenizer = JackTokenizer('Main.jack')
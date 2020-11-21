from JackTokenizer import JackTokenizer
from VMWriter import VMWriter
from SymbolTable import SymbolTable
class CompilationEngine():
    

    def __init__(self,fileName,writeToFile):
        self.tokenizer = JackTokenizer(fileName)
        self.writer = open( writeToFile, 'w')
        self.vm = VMWriter(self.writer)
        self.symbolTable = SymbolTable()
        self.space = '  '
        self.className = ''
        self.compileClass()

        self.writer.close()

    def compileClass(self):
        # 'class'
        classToken = self.tokenizer.getToken()
        if classToken.lower() == 'class':
            
            # '{className}'
            self.className = self.tokenizer.getToken()
            
            # class openBrace '{'
            self.tokenizer.getToken()
            
            self.compileClassVarDec()
            
            # class closeBrace '}'
            self.tokenizer.getTokenNoAdvance()

    def compileClassVarDec(self):
        # might be varDecToken or subroutineDec 
        # 'static|field'     
        varDecToken = self.tokenizer.getToken() 
        varDecToken = varDecToken.lower()
        if (varDecToken == 'static') or   (varDecToken == 'field'):
            
            # 'type'
            varType = self.tokenizer.getToken() 
                
            moreVars = True
            while moreVars:
                varName = self.tokenizer.getToken() 
                # ADD the var to the class Symbol Table
                self.symbolTable.define(varName,varType,varDecToken)
                nextToken = self.tokenizer.getToken()
                if nextToken != ',':
                    moreVars = False
                # semiColon  or comma 
            
            # look ahead to the First token in the new line
            nextToken = self.tokenizer.getNextTokenNoAdvance()
            nextToken = nextToken.lower()
            if (nextToken == 'static') or   (nextToken == 'field'):
                self.compileClassVarDec()
            
            #advace 
            self.tokenizer.getToken()
            self.compileSubroutine()        
                              
        else :
            self.compileSubroutine()

        # print(token)

    def compileSubroutine(self):
        currentToken = self.tokenizer.getTokenNoAdvance()
        if currentToken.lower() in ['constructor','function','method']:
            # 'constructor' | 'function' | 'method'
            routine = currentToken
            # ( 'void' | type )
            returnType = self.tokenizer.getToken()

            # 'subroutineName' 
            subroutineName = self.tokenizer.getToken()
            
            # parameterList open-brace '('            
            openBrace = self.tokenizer.getToken()
            
            # clear subroutine symbol-table
            self.symbolTable.startSubroutine()
            
            self.compileParameterList()

            # closeBrace ')' has been Read
            
            # subroutinebody OpenBrace '{'            
            bodyOpenBrace = self.tokenizer.getToken()

            self.compileVarDec()
            
            self.writer.write(self.space * 2 + '</subroutineBody>' + '\n')
            

            self.writer.write(self.space + '</subroutineDec>' + '\n')
            # bodyCloseBrace = self.tokenizer.getToken()
            # self.writer.write(self.space * 3 + self.tokenizer.handleTokenTags() + '\n' )
            currentToken = self.tokenizer.getToken()
            # print(f'currentToken :: {currentToken}')
            if currentToken in ['constructor','function','method']:
                self.compileSubroutine()
            


        else:
            pass


    def compileVarDec(self):

        varDec = self.tokenizer.getToken()
        if varDec.lower() == 'var':
            
            varType = self.tokenizer.getToken()
            moreVars = True
            while moreVars:
                varName = self.tokenizer.getToken()
                # fill in the subroutine symbol-table with vars
                self.symbolTable.define(varName,varType,'var')

                nextToken = self.tokenizer.getToken()
                if nextToken != ',':
                    moreVars = False
    
            # semiColon ';' has been read 
            

            MoreVarDecs = self.tokenizer.getNextTokenNoAdvance()
            ###print(f'nextToken :: {MoreVarDecs}')
            if MoreVarDecs.lower() == 'var':
                self.compileVarDec()

            # statements
            sToken = self.tokenizer.getToken()
            ###print(f'sToken :: {sToken}')
            
            #first token of statements is the current token
            self.compileStatements()
            # '}' subroutine body 


        else:
    
            # statements
            #first token of statements is the current token
            self.compileStatements()

            # '}' subroutine body 
            

        

    def compileParameterList(self):
        parType = self.tokenizer.getNextTokenNoAdvance()
        if parType != ')':

            morePars = True
            while morePars:

                parType = self.tokenizer.getToken()
                parName = self.tokenizer.getToken()
                # fill in the subroutine symbol-table with function arguments
                self.symbolTable.define(parName,parType,'arg')

                nextToken = self.tokenizer.getToken()
                if nextToken != ',':
                    morePars = False
        # curren token now at close brace 
        else:
            # curren token now at close brace 
            self.tokenizer.getToken()

            
    def compileStatements(self):
    
        currentToken = self.tokenizer.getTokenNoAdvance()
        currentToken = currentToken.lower()
        if currentToken in ['let','if','while','do','return']:
            self.redirectStatement(currentToken)
        
    def redirectStatement(self,token):
        if token == 'let':
            self.compileLet()
        elif token == 'if':
            self.compileIf()
        elif token == 'while':
            self.compileWhile()
        elif token == 'do':
            self.compileDo()
        elif token == 'return':
            self.compileReturn()



    def compileLet(self):
        # 'Let' token is current token

        # VarName
        self.tokenizer.getToken()

        # [expresion] ?
        nextToken = self.tokenizer.getToken()
        if nextToken != '=':
            # '['
            
            self.compileExpression()
            # ']'
            # self.tokenizer.getToken()
            
            self.tokenizer.getToken()         
        
        # '='
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
        self.compileExpression()
        # ';'
        # self.tokenizer.getToken()
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
        self.writer.write(self.space * 4 + '</letStatement>' + '\n')
        
        # compile following statements
        self.tokenizer.getToken()
        self.compileStatements()

    def compileDo(self):
        self.writer.write(self.space * 4 + '<doStatement>' + '\n')
        # Do
        # self.tokenizer.getTokenNoAdvance()
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
        # subroutine call 
        self.tokenizer.getToken()
        self.subroutineCall()

        # ';'
        self.tokenizer.getToken()    
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
        self.writer.write(self.space * 4 + '</doStatement>' + '\n')

        # compile following statements
        self.tokenizer.getToken()
        self.compileStatements()

    def compileIf(self):
        self.writer.write(self.space * 4 + '<ifStatement>' + '\n')
        # if
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
        # '('
        self.tokenizer.getToken()    
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')

        # expression
        self.compileExpression()
        # ')'
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
        # '{'
        self.tokenizer.getToken()    
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
        # statements
        self.writer.write(self.space * 5 + '<statements>' + '\n')

        self.tokenizer.getToken()
        self.compileStatements()
        self.writer.write(self.space * 5 + '</statements>' + '\n')

        # '}'
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
        # 'else'?
        nextToken = self.tokenizer.getToken() 
        # print(f'in ELSE {nextToken}' )
        if nextToken == 'else':
            # 'else'
            self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
            # '{'
            self.tokenizer.getToken()
            self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
            # statements
            self.writer.write(self.space * 5 + '<statements>' + '\n')

            self.tokenizer.getToken()
            self.compileStatements()
            self.writer.write(self.space * 5 + '</statements>' + '\n')
            
            # '}'
            self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
            self.writer.write(self.space * 4 + '</ifStatement>' + '\n')
            
            # compile following statements
            self.tokenizer.getToken()
            self.compileStatements()

        else:
            self.writer.write(self.space * 4 + '<ifStatement>' + '\n')

            # compile following statements
            self.compileStatements()


    def compileReturn(self):
        self.writer.write(self.space * 4 + '<returnStatement>' + '\n')
        # 'return'
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
        nextToken = self.tokenizer.getNextTokenNoAdvance()
        if nextToken != ';':
            self.compileExpression()
            # ';'
            self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
        else :
            # ';'
            self.tokenizer.getToken()
            self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
            
        self.writer.write(self.space * 4 + '</returnStatement>' + '\n')

        # compile following statements
        self.tokenizer.getToken()
        self.compileStatements()
        

    def compileWhile(self):
        self.writer.write(self.space * 4 + '<whileStatement>' + '\n')
       
        # "while"
        # self.tokenizer.getTokenNoAdvance()
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
        # '('
        self.tokenizer.getToken()
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
        
        # expression
        self.compileExpression()

        # ')'
        # self.tokenizer.getToken()
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
        
        # '{'
        self.tokenizer.getToken()
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
        
        self.writer.write(self.space * 5 + '<statements>' + '\n')
        # compile following statements
        self.tokenizer.getToken()
        self.compileStatements()
        self.writer.write(self.space * 5 + '</statements>' + '\n')
        
        # '}'
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')

        self.writer.write(self.space * 4 + '</whileStatement>' + '\n')
        # compile following statements
        self.tokenizer.getToken()
        self.compileStatements()
     

    def subroutineCall(self):
        # subroutineName or (className | varName)

        # self.tokenizer.getToken()    
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
        nextToken = self.tokenizer.getToken()
        if nextToken == '.': 
            # (className | varName)
            # '.'
            self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
            # subroutineName
            self.tokenizer.getToken()    
            self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')

            self.tokenizer.getToken()    
        
        # '('
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
        # expressionList
        self.writer.write(self.space * 5 + '<expressionList>' + '\n')

        nextToken = self.tokenizer.getNextTokenNoAdvance()
        if nextToken != ')':
            self.CompileExpressionList()
        self.writer.write(self.space * 5 + '</expressionList>' + '\n')

        # ')'
        self.tokenizer.getToken()    
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')

    
            #subroutineName

  
    def compileExpression(self): # ends with next token as current

        # term
        self.CompileTerm() 
        # (op term)*
        moreTerms = True
        nextToken = self.tokenizer.getToken()
        while moreTerms:
            if nextToken in ['+' ,'-' ,'*' ,'/' ,'&' ,'|' ,'<' ,'>' , '=']:
                self.writer.write(self.space * 6 + self.tokenizer.handleTokenTags() + '\n')
                self.CompileTerm()
                nextToken = self.tokenizer.getToken()
            else:
                moreTerms = False
                

        self.writer.write(self.space * 5 + '</expression>' + '\n')

    def CompileTerm(self):
        
        token = self.tokenizer.getToken()

        nextToken = self.tokenizer.getNextTokenNoAdvance()
        print(f'token ::: {token}')
        print(f'nextToken ::: {nextToken}')
        
        tokenType = self.tokenizer.tokenType()
        
        if tokenType == 'INT_CONST':
            self.vm.writePush('constant',token)      
        
        elif tokenType == 'STRING_CONST':
            
        # elif token in ['true' , 'false' , 'null' , 'this']:
        #     self.writer.write(self.space * 7 + self.tokenizer.handleTokenTags() + '\n')

        elif token == '(':
            # self.tokenizer.getToken()

            # expression
            self.compileExpression()
            # ')'
        elif nextToken == '[':
            # array indexing
            # varName
            # self.tokenizer.getToken()
            # '['
            self.tokenizer.getToken()
            # expression
            self.compileExpression()
            # ']'
        elif (nextToken == '(') or (nextToken == '.'):
            # subroutine call
            self.subroutineCall()
        
        elif token in ['-','~']:
            # self.writer.write(self.space * 7 + self.tokenizer.handleTokenTags() + '\n')
            self.CompileTerm()
            if token == '-':
                
            else:
                pass
            
        else:
            # self.tokenizer.getToken()
            self.writer.write(self.space * 7 + self.tokenizer.handleTokenTags() + '\n')



        # self.writer.write(self.space * 7 + self.tokenizer.handleTokenTags() + '\n')
        
        self.writer.write(self.space * 6 + '</term>' + '\n')

    def CompileExpressionList(self):
        # self.writer.write(self.space * 5 + '<expressionList>' + '\n')
        
        # expression
        self.compileExpression()
        moreExp = True
        while moreExp:
            nextToken = self.tokenizer.getTokenNoAdvance()
            if nextToken == ',':
                # ','
                self.writer.write(self.space * 6 + self.tokenizer.handleTokenTags() + '\n')
                self.compileExpression()
            else: 
                moreExp = False

        
        # self.writer.write(self.space * 5 + '<expressionList>' + '\n')

        
engine = CompilationEngine("Main.jack","Main.xml")


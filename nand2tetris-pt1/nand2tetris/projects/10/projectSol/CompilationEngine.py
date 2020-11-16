from JackTokenizer import JackTokenizer
class CompilationEngine():
    """
    docstring
    """
    def __init__(self,fileName,writeToFile):
        self.tokenizer = JackTokenizer(fileName)
        self.writer = open( writeToFile, 'w')
        self.space = '  '
        self.compileClass()

        self.writer.close()

    def compileClass(self):
        classToken = self.tokenizer.getToken()
        if classToken.lower() == 'class':
            self.writer.write('<class>' + '\n')
            self.writer.write(self.space + self.tokenizer.handleTokenTags() + '\n' )

            className = self.tokenizer.getToken()
            self.writer.write(self.space + self.tokenizer.handleTokenTags() + '\n' )

            openBrace = self.tokenizer.getToken()
            (self.writer.write(self.space + self.tokenizer.handleTokenTags() + '\n' ) ) if (openBrace == '{') else print("Missing {")
            self.compileClassVarDec()
            
            closebrace = self.tokenizer.getTokenNoAdvance()
            self.writer.write(self.space + self.tokenizer.handleTokenTags() + '\n' )
            
            #close class tag 
            self.writer.write('</class>' + '\n')


            

    def compileClassVarDec(self):
        # might be varDecToken or subroutineDec 
        varDecToken = self.tokenizer.getToken() 
        varDecToken = varDecToken.lower()
        if (varDecToken == 'static') or   (varDecToken == 'field'):
            self.writer.write(self.space + '<classVarDec>' + '\n')
            self.writer.write(self.space * 2 + self.tokenizer.handleTokenTags() + '\n')
            varType = self.tokenizer.getToken() 
            self.writer.write(self.space * 2 + self.tokenizer.handleTokenTags() + '\n')
                
            moreVars = True
            while moreVars:
                varName = self.tokenizer.getToken() 
                self.writer.write(self.space * 2 + self.tokenizer.handleTokenTags() + '\n')
                nextToken = self.tokenizer.getToken()
                if nextToken != ',':
                    moreVars = False
                # semiColon  or comma 
                self.writer.write(self.space * 2 + self.tokenizer.handleTokenTags() + '\n')
            
            #close classVarDec tag 
            self.writer.write(self.space + '</classVarDec>' + '\n')

            nextToken = self.tokenizer.getNextTokenNoAdvance()
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
                
            self.writer.write(self.space + '<subroutineDec>' + '\n')
            self.writer.write(self.space * 2 + self.tokenizer.handleTokenTags() + '\n')

            returnType = self.tokenizer.getToken()
            self.writer.write(self.space * 2 + self.tokenizer.handleTokenTags() + '\n' )
            subroutineName = self.tokenizer.getToken()
            self.writer.write(self.space * 2 + self.tokenizer.handleTokenTags() + '\n' )
            openBrace = self.tokenizer.getToken()
            self.writer.write(self.space * 2 + self.tokenizer.handleTokenTags() + '\n' )
            
            self.compileParameterList()
            # closeBrace
            self.writer.write(self.space * 2 + self.tokenizer.handleTokenTags() + '\n' )
            
            self.writer.write(self.space * 2 + '<subroutineBody>' + '\n')
            
            bodyOpenBrace = self.tokenizer.getToken()
            self.writer.write(self.space * 3 + self.tokenizer.handleTokenTags() + '\n' )
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
        # self.writer.write(self.space * 3 + '<varDec>' + '\n')

        varDec = self.tokenizer.getToken()
        if varDec.lower() == 'var':
            self.writer.write(self.space * 3 + '<varDec>' + '\n')
            
            self.writer.write(self.space * 4 + self.tokenizer.handleTokenTags() + '\n' )
            varType = self.tokenizer.getToken()
            self.writer.write(self.space * 4 + self.tokenizer.handleTokenTags() + '\n' )
            moreVars = True
            while moreVars:
                varName = self.tokenizer.getToken()
                self.writer.write(self.space * 4 + self.tokenizer.handleTokenTags() + '\n' )
                nextToken = self.tokenizer.getToken()
                if nextToken != ',':
                    moreVars = False
                    # comma
                self.writer.write(self.space * 4 + self.tokenizer.handleTokenTags() + '\n' )
    
            self.writer.write(self.space * 3 + '</varDec>' + '\n')
            

            MoreVarDecs = self.tokenizer.getNextTokenNoAdvance()
            ###print(f'nextToken :: {MoreVarDecs}')
            if MoreVarDecs.lower() == 'var':
                self.compileVarDec()

            self.writer.write(self.space * 3 + '<statements>' + '\n')
            # statements
            sToken = self.tokenizer.getToken()
            ###print(f'sToken :: {sToken}')
            self.compileStatements()
            self.writer.write(self.space * 3 + '</statements>' + '\n')
            # '}' subroutine body 
            self.writer.write(self.space * 3 + self.tokenizer.handleTokenTags() + '\n')


        else:
            self.writer.write(self.space * 3 + '</varDec>' + '\n')
    
            self.writer.write(self.space * 3 + '<statements>' + '\n')
            # statements
            self.compileStatements()
            self.writer.write(self.space * 3 + '</statements>' + '\n')
            # '}' subroutine body 
            self.writer.write(self.space * 3 + self.tokenizer.handleTokenTags() + '\n')
            

        

    def compileParameterList(self):
        parType = self.tokenizer.getToken()
        self.writer.write(self.space * 2 + "<parameterList>" + '\n' )

        if parType != ')':
            self.writer.write(self.space * 3 + self.tokenizer.handleTokenTags() + '\n' )
            morePars = True
            while morePars:
                parName = self.tokenizer.getToken()
                self.writer.write(self.space * 3 + self.tokenizer.handleTokenTags() + '\n' )
                nextToken = self.tokenizer.getToken()
                if nextToken != ',':
                    morePars = False



        self.writer.write(self.space * 2 + "</parameterList>" + '\n' )


            
    def compileStatements(self):
        # self.writer.write(self.space * 3 + '<statements>' + '\n')
    
        currentToken = self.tokenizer.getTokenNoAdvance()
        currentToken = currentToken.lower()
        if currentToken in ['let','if','while','do','return']:
            self.redirectStatement(currentToken)
        
        # self.writer.write(self.space * 3 + '</statements>' + '\n')


    def compileLet(self):
        self.writer.write(self.space * 4 + '<letStatement>' + '\n')
        # Let
        # self.tokenizer.getTokenNoAdvance()
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
        # VarName
        self.tokenizer.getToken()
        self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
        # [expresion] ?
        nextToken = self.tokenizer.getToken()
        if nextToken != '=':
            # '['
            self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
            
            self.compileExpression()
            # ']'
            # self.tokenizer.getToken()
            self.writer.write(self.space * 5 + self.tokenizer.handleTokenTags() + '\n')
            
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

    def compileExpression(self): # ends with next token as current
        self.writer.write(self.space * 5 + '<expression>' + '\n')
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
        self.writer.write(self.space * 6 + '<term>' + '\n')
        
        token = self.tokenizer.getToken()
        nextToken = self.tokenizer.getNextTokenNoAdvance()
        print(f'token ::: {token}')
        print(f'nextToken ::: {nextToken}')
        # tokenType = self.tokenizer.tokenType():
        
        # if tokenType == 'INT_CONST':
        #     self.writer.write(self.space * 7 + self.tokenizer.handleTokenTags() + '\n')
            
        # elif tokenType == 'STRING_CONST':
        #     self.writer.write(self.space * 7 + self.tokenizer.handleTokenTags() + '\n')

        # elif token in ['true' , 'false' , 'null' , 'this']:
        #     self.writer.write(self.space * 7 + self.tokenizer.handleTokenTags() + '\n')

        if token == '(':
            # self.tokenizer.getToken()
            self.writer.write(self.space * 7 + self.tokenizer.handleTokenTags() + '\n')
            # expression
            self.compileExpression()
            # ')'
            self.writer.write(self.space * 7 + self.tokenizer.handleTokenTags() + '\n')
        elif nextToken == '[':
            # array indexing
            # varName
            # self.tokenizer.getToken()
            self.writer.write(self.space * 7 + self.tokenizer.handleTokenTags() + '\n')
            # '['
            self.tokenizer.getToken()
            self.writer.write(self.space * 7 + self.tokenizer.handleTokenTags() + '\n')
            # expression
            self.compileExpression()
            # ']'
            self.writer.write(self.space * 7 + self.tokenizer.handleTokenTags() + '\n')
        elif (nextToken == '(') or (nextToken == '.'):
            # subroutine call
            self.subroutineCall()
        
        elif token in ['-','~']:
            self.writer.write(self.space * 7 + self.tokenizer.handleTokenTags() + '\n')
            
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


class SymbolTable():
    def __init__(self):
        self.classTable = []
        self.subroutineTable = []
        self.staticIdx = -1
        self.fieldIdx = -1
        self.argIdx = -1
        self.varIdx = -1

        # self.prettyPrint()


    def startSubroutine(self):
        self.subroutineTable = []
        self.argIdx = -1
        self.varIdx = -1
    
    def define(self,name,type,kind):
        """
        define(name,type,kind)
        
        """
            #  Add to classTable
            kind = kind.upper()
            if kind == 'STATIC':
                self.staticIdx += 1
                self.classTable.append({'name':name,'type':type,'kind':kind,'id':self.staticIdx})
            elif kind == 'FIELD':
                self.fieldIdx += 1
                self.classTable.append({'name':name,'type':type,'kind':kind,'id':self.fieldIdx})

            #  Add to subroutineTable
            elif kind == 'ARG':
                self.argIdx += 1
                self.subroutineTable.append({'name':name,'type':type,'kind':kind,'id':self.argIdx})
            elif kind == 'VAR':
                self.varIdx += 1
                self.subroutineTable.append({'name':name,'type':type,'kind':kind,'id':self.varIdx})
            self.prettyPrint()


    def varCount(self,kind):
            if kind == 'STATIC':
                return self.staticIdx + 1
            elif kind == 'FIELD':
                return self.fieldIdx + 1        
            elif kind == 'ARG':
                return self.argIdx + 1
            elif kind == 'VAR':
                return self.varIdx + 1


    def search(self,attr,value,returnedAttr):
        # search in class SymbolTable     
        classTableResult = list(filter(lambda row: row[f'{attr}'] == value,self.classTable))
        if classTableResult == []:
            # search in subroutine SymbolTable     
            subroutineTableResult = list(filter(lambda row: row[f'{attr}'] == value,self.subroutineTable))
            return None if subroutineTableResult == [] else subroutineTableResult[0][f'{returnedAttr}']
            
        else: 
            return classTableResult[0][f'{returnedAttr}']


    def kindOf(self,name):
        print(f"kind of {name} : {self.search('name',name,'kind')}" )
        return self.search('name',name,'kind')

    def typeOf(self,name):
        print(f"type of {name} : {self.search('name',name,'type')}")
        return self.search('name',name,'type')

    
    def indexOf(self,name):
        print(f"index of {name} : {self.search('name',name,'id')}")
        return self.search('name',name,'id')

    def prettyPrint(self):
            print("-------- CLASS TABLE --------")
            [print(row) for row in self.classTable]
            # print(self.classTable) 
            print("-------- End CLASS TABLE --------")
            print('')
            print("-------- subroutine TABLE --------")
            [print(row) for row in self.subroutineTable]
            # print(self.subroutineTable) 

            print("-------- End subroutine TABLE --------")
            print('')


# file = SymbolTable()

# file.define('x1','int','var')
# file.define('x2','int','var')
# file.define('y1','int','arg')
# file.define('y2','int','arg')
# file.define('account','string','static')
# file.define('accountID','int','static')
# file.define('isTrue1','boolean','field')
# file.define('isTrue2','boolean','field')
# file.startSubroutine()
# file.prettyPrint()
# file.define('x1','int','var')

# file.indexOf('isTrue1')
# file.typeOf('isTrue1')
# file.kindOf('isTrue1')
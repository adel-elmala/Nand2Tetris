import re

class Tokenizer():
    
    def __init__(self,fileName):
        self.fileName = fileName

        
    
    def readFile(self):
        # Check if its right extention
        pattern = re.compile(r'\w*[.]asm')

        match = re.match(pattern,self.fileName)

        if match:
            with open(self.fileName, 'r') as reader:
                lines = reader.readlines()
                
                # print(lines)
                return lines
        else:
            raise "File Extenstion not supported"
   


    def filterLine(self,line):
        lineList = line.split()
        # print(lineList)
        return ((lineList == []) or (lineList[0] == '//'))

    def tokens(self,line):
        triple = line.partition('//') # Remove in-line comments
        token  = triple[0].rstrip('\n') # Remove '\n' chars
        token  = token.strip()  # Remove leading and trailing whitespaces
        # print(triple)
        return token

    def filter(self,list):
        filterList = [ self.tokens(line) for line in list if not(self.filterLine(line)) ]    

        # print(filterList)
        
        return filterList

    def tokenizer(self):
        file = self.readFile()
        return self.filter(file)    



# token = Tokenizer("Max.asm")
# token.tokenizer()

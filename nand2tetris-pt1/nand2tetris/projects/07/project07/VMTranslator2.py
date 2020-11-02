from parser import Tokenizer
from codeWriter import CodeWriter
import re
import os
import glob
import sys

class VMtranslator():
    """
        Translate VM command to Hack-assembly commands 

    """
    def __init__(self,path):
        self.path = path
        self.fileName = ''
        self.folderName = ''
        self.writeToFile = ''
        self.writeToFolder = ''
        self.fileNoExt = ''
        # self.parser = Tokenizer()

        # self.VMtranslator()
        self.identifyPath()

    def identifyPath(self):
        # path = self.path.split('/')
        path = re.split(r'[ / ]',self.path)
        last = path[-1]
        
        
        # print(self.writeToFolder)
        pattern = re.compile(r'.*[.]vm$')
        match = re.match(pattern,last)
        if match: # vm File

            
            print("in file")
            print("----------")
            print(match)
            print("----------")
            
            self.fileNoExt = last.partition('.')[0]
            self.writeToFile = self.fileNoExt + '.asm'

            # self.writeToFolder = '/'.join(path[:-1])
            self.fileName = last
            print("----------")
            print(self.fileName)
            print("----------")
            self.translateFile(self.path)
        else : # Folder
            print("in folder")
            self.writeToFolder = self.path
            self.writeToFile =  self.writeToFolder + self.fileName.partition('.')[0] + ".asm"
            self.folderName = last
            # print(self.writeToFolder)
            self.translateFolder(self.writeToFolder)

    
    
    def translateFile(self,fileName):
        print("----------")
        print(fileName)
        print("----------")

        parser = Tokenizer(fileName)
        commands = parser.tokenizer()   # List of vm commands
        # print(commands)
        coder = CodeWriter()
        
        print(f'write to: {self.writeToFile}')
        with open( self.writeToFile, 'w') as writer:
            # print(file)
            for i,cmd in enumerate(commands) :
                # print(i,cmd)
                translated = coder.writeCode(cmd,i,self.fileNoExt) 
                # print(translated)
                translated = [f"//{cmd}"] + translated
                #  translated
                [writer.write(tcmd + '\n') for tcmd in translated]

    def translateFolder(self,folder):
        # for filename in os.listdir(f'{folder}'):
        # path = '/some/path/to/file'
        print(f'in translate Folder')
        for filename in glob.glob(os.path.join(folder, '*.vm')):
            print("+++++")
            print(filename)
            self.fileName = filename.partition('/')[-1]
            self.writeToFile =  self.fileName.partition('.')[0] + ".asm"

            print( f'filename= {self.fileName}')

            self.translateFile(self.fileName)



# if name == "__main"    

# translate = VMtranslator("BasicTest.vm")
# translate = VMtranslator("tet")
# translate.identifyPath()
# translate.translateFolder("BasicTest.vm")

def main():
    path = sys.argv[-1]    
    VMtranslator(path)
    
if __name__ == '__main__':
    main()
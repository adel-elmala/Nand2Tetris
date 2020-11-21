class VMWriter():
    def __init__(self,writer):
        self.writer = writer


    def writePush(self,segment,index):
        self.writer.write(f'push {segment} {index}\n')

    def writePop(self,segment,index):
        self.writer.write(f'pop {segment} {index}\n')

    def writeArithmetic(self,command):
        self.writer.write(f'{command}\n')
  
    def writeLabel(self,label):
        self.writer.write(f'label {label}\n')

    def writeGoto(self,label):
        self.writer.write(f'if-goto {label}\n')

    def writeIf(self,label):
        self.writer.write(f'goto {label}\n')
    
    def writeCall(self,name,nArgs):
        self.writer.write(f'call {name} {nArgs}\n')


    def writeFunction(self,name,nLocals):
        self.writer.write(f'function {name} {nLocals}\n')
        

    def writeReturn(self):
        self.writer.write(f'return \n')
        
    def close(self):
        pass

    
# file = open('Main.vm','w')
# write = VMWriter(file)
# write.writeArithmetic('Add')
# write.writePush('Local',10)
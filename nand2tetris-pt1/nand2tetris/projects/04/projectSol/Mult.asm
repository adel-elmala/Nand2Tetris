// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.


// i = R1
// sum = 0
// (LOOP)
//      While (i != 0):
//      sum = sum + R0
//      i--
// END

// Initialize counter i = R1
    @R1 
    D=M 

    @i 
    M=D     // i = R1 
    
    @R2
    M=0    // sum = 0

// Load R0 into D
    @R0
    D=M     // D = R0

// IF (i == 0) (END)
(LOOP)
    @i
    D=M     // D = i

    @END
    D;JEQ   // if D = 0 jump to (END)
// Load R0 into D
    @R0
    D=M     // D = R0

    @R2
    M=M+D   // sum = sum + R0

    @i 
    M=M-1   // i = i - 1
    @LOOP
    0;JMP
// ELSE Goto (LOOP) 



(END)
    @END
    0;JMP
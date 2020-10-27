// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// (KEYLOOP)
    //  if kbd == 0
    // then Fill = 0
    // else Fill = -1 
    // Jump to (FILLSCREEN)
// (FILLSCREEN)
    // Fill all screen memry with FILL value using a loop 
    //  Jump to (KEYLOOP)


(KEYLOOP)
    @KBD 
    D=M    // D = Key pressed 
    
    @fill 
    M=0   // fill = 0
    
    @THEN   // if D=0 then fill = 0 else fill = -1
    D;JEQ   // D = 0

    @fill 
    M=-1     // fill = -1

(THEN)
   
    @FILLSCREEN 
    0;JMP   // JUMP to fill the screen 

(FILLSCREEN)
    @8192
    D=A
    @counter
    M=D     // counter = 8192

    
    @SCREEN 
    D=A     // D = SCREEN base addr.

    @i 
    M=D   // M = screen base addr + current register addr  
    
(LOOP)
   

    @counter 
    D=M   

    @END    // if counter == 0  ie. Filles the screen
    D;JEQ
    
    @fill     
    D=M     // D = -1 OR 0  
    
    @i 
    A=M     // A = Addr of target Register in screen map
    M=D     // fill target regsiter 
    @i 
    M=M+1   // i++
    @counter
    M=M-1   // counter--

    @LOOP
    0;JMP

(END)
    @KEYLOOP
    0;JMP   // JUMP to listen to KEYBOARD AGAIN
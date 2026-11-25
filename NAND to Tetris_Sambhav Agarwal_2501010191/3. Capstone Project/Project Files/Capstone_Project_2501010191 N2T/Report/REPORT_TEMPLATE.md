# Capstone Project: Make the Computer Draw a Box

**Name:** [Sambhav Agarwal]  
**Roll Number:** 2501010191  
**Course:** Nand to Tetris – I (ETCCNT301)  
**K:** 91

## 1. Aim
Build the Hack computer, write a two-pass Python assembler, and create a keyboard-controlled black rectangle.

## 2. Personalized box dimensions
- Starting row: 91
- Height: 20 rows
- Width: 16 × ((91 mod 4) + 1) = 64 pixels
- Width: 4 Hack screen words
- Starting address: SCREEN + 32 × 91 = 19296

## 3. Part A – Computer construction
Explain the CPU, Memory and Computer chips. Insert genuine screenshots from CPU.tst, Memory.tst, ComputerAdd.tst, ComputerMax.tst and ComputerRect.tst. Mention any built-in chips used.

## 4. Part B – Python assembler
The first pass records labels and their ROM addresses. The second pass translates A- and C-instructions into 16-bit binary code. Variables begin at RAM address 16. Since 91 mod 3 = 1, the extra feature is clear invalid-instruction messages with source line numbers.

## 5. Part C – Box program
The program checks KBD. When a key is pressed, it writes -1 into four consecutive screen words for 20 rows. When no key is pressed, it writes 0 to the same area. Each screen row is 32 words, and the box begins at address 19296. Insert your CPU Emulator screenshot.

## 6. Conclusion
[Summarize the tests you actually ran and their results.]

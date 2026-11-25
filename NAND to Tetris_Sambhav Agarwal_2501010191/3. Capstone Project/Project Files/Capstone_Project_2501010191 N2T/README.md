# Nand to Tetris Capstone – Roll No. 2501010191

K = 91 (last two digits of roll number).

## Personalized rectangle
- Starting row: 91
- Height: 20 rows
- Width: 16 × ((91 mod 4) + 1) = 64 pixels = 4 Hack screen words
- Starting address: SCREEN + 32 × 91 = 19296

## Personalized assembler feature
91 mod 3 = 1: invalid instructions produce a clear error with their source line number.

## Run
From this directory in PowerShell:
```powershell
python Part_B\assembler.py Part_C\Box.asm --k 91
```
Then load `Part_C/Box.hack` in the Nand2Tetris CPU Emulator.

## Testing and submission
Run the official Hardware Simulator tests listed in your assignment: CPU.tst, Memory.tst, ComputerAdd.tst, ComputerMax.tst and ComputerRect.tst. The test scripts and all prerequisite course chips are not supplied in the assignment PDF, so add them from your course/Nand2Tetris installation. Capture genuine screenshots yourself; do not claim tests passed until run.

Fill in your name and the actual mistake fixed in `Report/REPORT_TEMPLATE.md`.

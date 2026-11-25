#!/usr/bin/env python3
"""Two-pass Hack assembler; K=91 feature: line-numbered invalid-instruction errors."""
import argparse, re, sys
from pathlib import Path

DEST = {"":"000","M":"001","D":"010","MD":"011","A":"100","AM":"101","AD":"110","AMD":"111"}
JUMP = {"":"000","JGT":"001","JEQ":"010","JGE":"011","JLT":"100","JNE":"101","JLE":"110","JMP":"111"}
COMP = {
"0":"0101010","1":"0111111","-1":"0111010","D":"0001100","A":"0110000","M":"1110000",
"!D":"0001101","!A":"0110001","!M":"1110001","-D":"0001111","-A":"0110011","-M":"1110011",
"D+1":"0011111","A+1":"0110111","M+1":"1110111","D-1":"0001110","A-1":"0110010","M-1":"1110010",
"D+A":"0000010","D+M":"1000010","D-A":"0010011","D-M":"1010011","A-D":"0000111","M-D":"1000111",
"D&A":"0000000","D&M":"1000000","D|A":"0010101","D|M":"1010101"}
SYMBOL = re.compile(r"^[A-Za-z_.$:][\w.$:]*$")
PREDEFINED = {"SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4,"SCREEN":16384,"KBD":24576}
PREDEFINED.update({f"R{i}":i for i in range(16)})

def error(line, message, k):
    # 91 % 3 == 1: report a clear source line number.
    raise ValueError(f"Line {line}: {message}")

def assemble(path, k):
    source = []
    for n, raw in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        line = re.sub(r"\s+", "", raw.split("//", 1)[0])
        if line:
            source.append((n, line))
    symbols, rom = dict(PREDEFINED), 0

    # Pass 1: resolve labels to ROM addresses.
    for n, line in source:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            if not SYMBOL.match(label):
                error(n, "invalid label", k)
            if label in symbols:
                error(n, f"duplicate or reserved label '{label}'", k)
            symbols[label] = rom
        elif "(" in line or ")" in line:
            error(n, "malformed label declaration", k)
        else:
            rom += 1

    # Pass 2: encode instructions and allocate variables from RAM address 16.
    result, next_var = [], 16
    for n, line in source:
        if line.startswith("(") and line.endswith(")"):
            continue
        try:
            if line.startswith("@"):
                token = line[1:]
                if token.isdigit():
                    value = int(token)
                else:
                    if not SYMBOL.match(token):
                        raise ValueError("invalid A-instruction symbol")
                    if token not in symbols:
                        symbols[token] = next_var
                        next_var += 1
                    value = symbols[token]
                if not 0 <= value <= 32767:
                    raise ValueError("A-instruction value must be between 0 and 32767")
                result.append(f"{value:016b}")
            else:
                if line.count(";") > 1 or line.count("=") > 1:
                    raise ValueError("malformed C-instruction")
                left, *jump_parts = line.split(";")
                jump = jump_parts[0] if jump_parts else ""
                if jump not in JUMP:
                    raise ValueError("invalid jump mnemonic")
                if "=" in left:
                    dest, comp = left.split("=")
                else:
                    dest, comp = "", left
                if dest not in DEST:
                    raise ValueError("invalid destination mnemonic")
                if comp not in COMP:
                    raise ValueError("invalid computation mnemonic")
                result.append("111" + COMP[comp] + DEST[dest] + JUMP[jump])
        except ValueError as exc:
            error(n, str(exc), k)
    return result, symbols

def main():
    p = argparse.ArgumentParser()
    p.add_argument("source")
    p.add_argument("-o", "--output")
    p.add_argument("--k", type=int, default=91)
    a = p.parse_args()
    src = Path(a.source)
    out = Path(a.output) if a.output else src.with_suffix(".hack")
    try:
        machine, _ = assemble(src, a.k)
        out.write_text("\\n".join(machine) + "\\n", encoding="utf-8")
        print(f"Assembled {len(machine)} instructions: {out}")
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

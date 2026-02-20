register_map = {
    "$zero": 0, "$at": 1,
    "$v0": 2, "$v1": 3,
    "$a0": 4, "$a1": 5, "$a2": 6, "$a3": 7,
    "$t0": 8, "$t1": 9, "$t2": 10, "$t3": 11,
    "$t4": 12, "$t5": 13, "$t6": 14, "$t7": 15,
    "$s0": 16, "$s1": 17, "$s2": 18, "$s3": 19,
    "$s4": 20, "$s5": 21, "$s6": 22, "$s7": 23,
    "$t8": 24, "$t9": 25,
    "$k0": 26, "$k1": 27,
    "$gp": 28, "$sp": 29, "$fp": 30, "$ra": 31
}
# Full-ish MIPS instruction encoding reference
instructions = {
    "add":  {"type": "R", "opcode": 0, "funct": 32},
    "addu": {"type": "R", "opcode": 0, "funct": 33},
    "sub":  {"type": "R", "opcode": 0, "funct": 34},
    "subu": {"type": "R", "opcode": 0, "funct": 35},
    "and":  {"type": "R", "opcode": 0, "funct": 36},
    "or":   {"type": "R", "opcode": 0, "funct": 37},
    "xor":  {"type": "R", "opcode": 0, "funct": 38},
    "nor":  {"type": "R", "opcode": 0, "funct": 39},
    "slt":  {"type": "R", "opcode": 0, "funct": 42},
    "sltu": {"type": "R", "opcode": 0, "funct": 43},
    "sll":  {"type": "R", "opcode": 0, "funct": 0},
    "srl":  {"type": "R", "opcode": 0, "funct": 2},
    "sra":  {"type": "R", "opcode": 0, "funct": 3},
    "jr":   {"type": "R", "opcode": 0, "funct": 8},
    "jalr": {"type": "R", "opcode": 0, "funct": 9},

    "addi": {"type": "I", "opcode": 8},
    "addiu":{"type": "I", "opcode": 9},
    "andi": {"type": "I", "opcode": 12},
    "ori":  {"type": "I", "opcode": 13},
    "xori": {"type": "I", "opcode": 14},
    "lui":  {"type": "I", "opcode": 15},
    "lw":   {"type": "I", "opcode": 35},
    "sw":   {"type": "I", "opcode": 43},
    "lb":   {"type": "I", "opcode": 32},
    "lbu":  {"type": "I", "opcode": 36},
    "sb":   {"type": "I", "opcode": 40},
    "beq":  {"type": "I", "opcode": 4},
    "bne":  {"type": "I", "opcode": 5},

    "j":    {"type": "J", "opcode": 2},
    "jal":  {"type": "J", "opcode": 3}
}

def convert(instructionString) ->int:
    """Converts a string to a instruction in MIPS"""
    partsOfInstruction = instructionString.split(" ")
    opcodeNamespace = partsOfInstruction[0].replace(" ", "").lower()
    try:
        opcodeData = instructions[opcodeNamespace]
        opcodeHex = instructions[opcodeNamespace]["opcode"]
    except KeyError:
        raise KeyError(f"Invalid opcode namespace {opcodeNamespace}")
    match opcodeData["type"]:
        case "J":
            return encodeJType(opcodeHex, int(partsOfInstruction[1]))
        case "I":
            rt = register_map[partsOfInstruction[1].strip().replace(",", "")]
            rs = register_map[partsOfInstruction[2].strip().replace(",", "")]
            imm = int(partsOfInstruction[3].strip().replace(",", ""))
            return encodeIType(opcodeHex, rs, rt, imm)
        case "R":
            instr = opcodeNamespace
            funct = opcodeData["funct"]

            if instr in ["sll", "srl", "sra"]:
                rd = register_map[partsOfInstruction[1].strip().replace(",", "")]
                rt = register_map[partsOfInstruction[2].strip().replace(",", "")]
                shamt = int(partsOfInstruction[3].strip())
                rs = 0

            elif instr == "jr":
                rs = register_map[partsOfInstruction[1].strip()]
                rt = 0
                rd = 0
                shamt = 0

            elif instr == "jalr":
                rd = register_map[partsOfInstruction[1].strip()]
                rs = register_map[partsOfInstruction[2].strip()]
                rt = 0
                shamt = 0

            else:
                rd = register_map[partsOfInstruction[1].strip().replace(",", "")]
                rs = register_map[partsOfInstruction[2].strip().replace(",", "")]
                rt = register_map[partsOfInstruction[3].strip().replace(",", "")]
                shamt = 0

            return encodeRType(opcodeHex, rs, rt, rd, shamt, funct)
#Lots of these functions AI generated, I'm using them to make
#my work flow easier to fill in the simple byte conversion stuff
def encodeRType(opcode, rs, rt, rd, shamt, funct):
        return (opcode << 26) | (rs << 21) | (rt << 16) | (rd << 11) | (shamt << 6) | funct

def encodeIType(opcode, rs, rt, immediate):
    return (opcode << 26) | (rs << 21) | (rt << 16) | (immediate & 0xFFFF)

def encodeJType(opcode, addr):
    target = (addr >> 2) & 0x03FFFFFF
    return (opcode << 26) | target

#!/usr/bin/env python3
#
#    Build Latex tables of verilog module interface signals and registers
#

import sys
from parse import parse
import math

regvfile_name = ''

#name, type, address, width, default value, description

def write_hw(table):

    global regvfile_name
    fout = open (regvfile_name+'_gen.vh', 'w')

    fout.write("//This file was generated by script mkregs.py\n\n")

    fout.write("\n\n//write registers\n")
    for row in table:
        name = row[0]
        typ = row[1]
        address = row[2]
        width = row[3]
        default_val = row[4]

        if (typ == 'W'):
            fout.write("`IOB_REG_ARE(clk, rst, " + default_val + ", valid & wstrb & (address == " + address + "), " + name + ", wdata[" + width + "-1:0])\n")
        else:
            continue

    fout.write("\n\n//read registers\n")
    fout.write("`IOB_VAR(rdata_int, DATA_W)\n")
    fout.write("`IOB_VAR(rdata_int2, DATA_W)\n")
    fout.write("`IOB_REG_ARE(clk, rst, 0, valid, rdata_int2, rdata_int)\n")
    fout.write("`IOB_VAR2WIRE(rdata_int2, rdata)\n\n")

    fout.write("always @* begin\n")
    fout.write("   rdata_int = 1'b0;\n")
    fout.write("   case(address)\n")

    for row in table:
        name = row[0]
        typ = row[1]
        address = row[2]
        width = row[3]
        default_val = row[4]

        if (typ == 'R'):
            fout.write("     " + address + ": rdata_int = " + name + ";\n")
        else:
            continue

    fout.write("     default: rdata_int = 1'b0;\n")
    fout.write("   endcase\n")
    fout.write("end\n")

    #ready signal
    fout.write("`IOB_VAR(ready_int, 1)\n")
    fout.write("`IOB_REG_AR(clk, rst, 0, ready_int, valid)\n")
    fout.write("`IOB_VAR2WIRE(ready_int, ready)\n")

    fout.close()


def write_hwheader(table):

    global regvfile_name
    fout = open(regvfile_name+'_def.vh', 'w')

    fout.write("//This file was generated by script mkregs.py\n\n")

    fout.write("//address width\n")
    fout.write("`define " + regvfile_name + "_ADDR_W " + str(int(math.ceil(math.log(len(table), 2)))) + "\n\n")

    fout.write("//address macros\n")
    for row in table:
        name = row[0]
        address = row[2]
        fout.write("`define " + name + "_ADDR " + address + "\n")

    fout.write("\n//registers width\n")
    for row in table:
        name = row[0]
        width = row[3]
        fout.write("`define " + name + "_W " + width + "\n")

    fout.close()


def write_swheader(table):

    global regvfile_name
    fout = open(regvfile_name+'.h', 'w')

    fout.write("//This file was generated by script mkregs.py\n\n")

    fout.write("//register address mapping\n")
    for row in table:
        name = row[0]
        address = row[2]
        fout.write("#define " + name + " " + address + "\n")

    fout.close()


def swreg_parse (code, hwsw):

    swreg_cnt = 0
    table = [] #name, type, address, width, default value, description

    for line in code:

        swreg_flds = []
        swreg_flds_tmp = parse('{}`IOB_SWREG_{}({},{},{}){}//{}', line)

        if swreg_flds_tmp is None:
            swreg_flds_tmp = parse('`IOB_SWREG_{}({},{},{}){}//{}', line)
            if swreg_flds_tmp is None: continue #not a sw reg
        else:
            swreg_flds_tmp = swreg_flds_tmp[1:]

        #NAME
        swreg_flds.append(swreg_flds_tmp[1].strip(' '))

        #TYPE
        swreg_flds.append(swreg_flds_tmp[0])

        #ADDRESS
        swreg_flds.append(str(swreg_cnt))
        swreg_cnt = swreg_cnt + 1

        #WIDTH
        swreg_flds.append(swreg_flds_tmp[2])

        #DEFAULT VALUE
        swreg_flds.append(swreg_flds_tmp[3])

        #DESCRIPTION
        swreg_flds.append(swreg_flds_tmp[5])

        table.append(swreg_flds)


    if(hwsw == "HW"):
        write_hwheader(table)
        write_hw(table)

    elif(hwsw == "SW"):
        write_swheader(table)

def main () :

    global regvfile_name

    #parse command line
    if len(sys.argv) != 3:
        print("Usage: ./mkregs.py TOP_swreg.vh [HW|SW]")
        print(" TOP_swreg.vh:the software accessible registers definitions file")
        print(" [HW|SW]: use HW to generate the hardware files or SW to generate the software files")
        quit()
    else:
        regvfile_name = sys.argv[1]
        hwsw = sys.argv[2]

    #parse input file
    fin = open (regvfile_name, 'r')
    defsfile = fin.readlines()
    fin.close()

    regvfile_name = regvfile_name.split('/')[-1].split('.')[0]

    swreg_parse (defsfile, hwsw)

if __name__ == "__main__" : main ()

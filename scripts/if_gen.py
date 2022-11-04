#!/usr/bin/env python3

# Generates IOb Native, AXI4 Full and AXI4 Lite ports, port maps and signals
#
#   See "Usage" below
#

import sys

table = []

#
# IOb Native Bus Signals
#

iob=[ \
{'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'1',          'name':'iob_valid', 'default':'0', 'description':'Request valid.'}, \
{'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'ADDR_W',     'name':'iob_addr',  'default':'0', 'description':'Address.'}, \
{'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'DATA_W',     'name':'iob_wdata', 'default':'0', 'description':'Write data.'}, \
{'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'(DATA_W/8)', 'name':'iob_wstrb', 'default':'0', 'description':'Write strobe.'}, \
{'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width':'1',          'name':'iob_rvalid','default':'0', 'description':'Read data valid.'}, \
{'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width':'DATA_W',     'name':'iob_rdata', 'default':'0', 'description':'Read data.'}, \
{'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width':'1',          'name':'iob_ready', 'default':'0', 'description':'Interface ready.'}, \
]

#
# AXI4 Bus Signals
#

# bus constants
AXI_SIZE_W = '3'
AXI_BURST_W = '2'
AXI_LOCK_W = '2'
AXI_CACHE_W = '4'
AXI_PROT_W = '3'
AXI_QOS_W = '4'
AXI_RESP_W = '2'

axi_write=[ \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'AXI_ID_W',       'name':'axi_awid',    'default':'0', 'description':'Address write channel ID.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'AXI_ADDR_W',     'name':'axi_awaddr',  'default':'0', 'description':'Address write channel address.'}, \
{'lite':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'AXI_LEN_W',      'name':'axi_awlen',   'default':'0', 'description':'Address write channel burst length.'}, \
{'lite':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width': AXI_SIZE_W,      'name':'axi_awsize',  'default':'2', 'description':'Address write channel burst size. This signal indicates the size of each transfer in the burst.'}, \
{'lite':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width': AXI_BURST_W,     'name':'axi_awburst', 'default':'1', 'description':'Address write channel burst type.'}, \
{'lite':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width': AXI_LOCK_W,      'name':'axi_awlock',  'default':'0', 'description':'Address write channel lock type.'}, \
{'lite':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width': AXI_CACHE_W,     'name':'axi_awcache', 'default':'2', 'description':'Address write channel memory type. Transactions set with Normal, Non-cacheable, Modifiable, and Bufferable (0011).'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width': AXI_PROT_W,      'name':'axi_awprot',  'default':'2', 'description':'Address write channel protection type. Transactions set with Normal, Secure, and Data attributes (000).'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width': AXI_QOS_W,       'name':'axi_awqos',   'default':'0', 'description':'Address write channel quality of service.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'1',              'name':'axi_awvalid', 'default':'0', 'description':'Address write channel valid.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width':'1',              'name':'axi_awready', 'default':'1', 'description':'Address write channel ready.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'AXI_DATA_W',     'name':'axi_wdata',   'default':'0', 'description':'Write channel data.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'(AXI_DATA_W/8)', 'name':'axi_wstrb',   'default':'0', 'description':'Write channel write strobe.'}, \
{'lite':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'1',              'name':'axi_wlast',   'default':'0', 'description':'Write channel last word flag.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'1',              'name':'axi_wvalid',  'default':'0', 'description':'Write channel valid.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width':'1',              'name':'axi_wready',  'default':'1', 'description':'Write channel ready.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width':'AXI_ID_W',       'name':'axi_bid',     'default':'0', 'description':'Write response channel ID.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width': AXI_RESP_W,      'name':'axi_bresp',   'default':'0', 'description':'Write response channel response.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width':'1',              'name':'axi_bvalid',  'default':'0', 'description':'Write response channel valid.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'1',              'name':'axi_bready',  'default':'1', 'description':'Write response channel ready.'} \
]

axi_read=[ \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'AXI_ID_W',       'name':'axi_arid',    'default':'0', 'description':'Address read channel ID.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'AXI_ADDR_W',     'name':'axi_araddr',  'default':'0', 'description':'Address read channel address.'}, \
{'lite':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'AXI_LEN_W',      'name':'axi_arlen',   'default':'0', 'description':'Address read channel burst length.'}, \
{'lite':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width': AXI_SIZE_W,      'name':'axi_arsize',  'default':'2', 'description':'Address read channel burst size. This signal indicates the size of each transfer in the burst.'}, \
{'lite':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width': AXI_BURST_W,     'name':'axi_arburst', 'default':'1', 'description':'Address read channel burst type.'}, \
{'lite':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width': AXI_LOCK_W,      'name':'axi_arlock',  'default':'0', 'description':'Address read channel lock type.'}, \
{'lite':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width': AXI_CACHE_W,     'name':'axi_arcache', 'default':'2', 'description':'Address read channel memory type. Transactions set with Normal, Non-cacheable, Modifiable, and Bufferable (0011).'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width': AXI_PROT_W,      'name':'axi_arprot',  'default':'2', 'description':'Address read channel protection type. Transactions set with Normal, Secure, and Data attributes (000).'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width': AXI_QOS_W,       'name':'axi_arqos',   'default':'0', 'description':'Address read channel quality of service.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'1',              'name':'axi_arvalid', 'default':'0', 'description':'Address read channel valid.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width':'1',              'name':'axi_arready', 'default':'1', 'description':'Address read channel ready.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width':'AXI_ID_W',       'name':'axi_rid',     'default':'0', 'description':'Read channel ID.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width':'AXI_DATA_W',     'name':'axi_rdata',   'default':'0', 'description':'Read channel data.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width': AXI_RESP_W,      'name':'axi_rresp',   'default':'0', 'description':'Read channel response.'}, \
{'lite':0, 'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width':'1',              'name':'axi_rlast',   'default':'0', 'description':'Read channel last word.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width':'1',              'name':'axi_rvalid',  'default':'0', 'description':'Read channel valid.'}, \
{'lite':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'1',              'name':'axi_rready' , 'default':'1', 'description':'Read channel ready.'} \
]

#
# AMBA Bus Signals
#

# bus constants
AHB_BURST_W = '3'
AHB_PROT_W = '4'
AHB_SIZE_W = '3'
AHB_TRANS_W = '2'

APB_PROT_W = '3'

amba=[ \
{'ahb':1, 'apb':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'AHB_ADDR_W',     'name':'ahb_addr',     'default':'0', 'description':'Byte address of the transfer.'}, \
{'ahb':1, 'apb':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width': AHB_BURST_W,     'name':'ahb_burst',    'default':'0', 'description':'Burst type.'}, \
{'ahb':1, 'apb':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'1',              'name':'ahb_mastlock', 'default':'0', 'description':'Transfer is part of a lock sequence.'}, \
{'ahb':1, 'apb':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width': AHB_PROT_W,      'name':'ahb_prot',     'default':'1', 'description':'Protection type. Transactions set with Data, User access, Non-bufferrable, and Non-cacheable attributes (0001).'}, \
{'ahb':0, 'apb':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width': APB_PROT_W,      'name':'apb_prot',     'default':'2', 'description':'Protection type. Transactions set with Normal, Non-secure, and Data attributes (010).'}, \
{'ahb':1, 'apb':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width': AHB_SIZE_W,      'name':'ahb_size',     'default':'2', 'description':'Burst size. This signal indicates the size of each transfer in the burst.'}, \
{'ahb':1, 'apb':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'1',              'name':'ahb_nonsec',   'default':'0', 'description':'Non-secure transfer.'}, \
{'ahb':1, 'apb':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'1',              'name':'ahb_excl',     'default':'0', 'description':'Exclusive transfer.'}, \
{'ahb':1, 'apb':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'AHB_MASTER_W',   'name':'ahb_master',   'default':'0', 'description':'Master ID.'}, \
{'ahb':1, 'apb':0, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width': AHB_TRANS_W,     'name':'ahb_trans',    'default':'0', 'description':'Transfer type. This signal indicates the type of the transfer.'}, \
{'ahb':1, 'apb':1, 'master':0, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'1',              'name':'ahb_sel',      'default':'0', 'description':'Slave select.'}, \
{'ahb':0, 'apb':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'1',              'name':'ahb_enable',   'default':'0', 'description':'Enable. This signal indicates the number of clock cycles of the transfer.'}, \
{'ahb':1, 'apb':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'1',              'name':'ahb_write',    'default':'0', 'description':'Write. This signal indicates the direction of the operation.'}, \
{'ahb':1, 'apb':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'AHB_DATA_W',     'name':'ahb_wdata',    'default':'0', 'description':'Write data.'}, \
{'ahb':1, 'apb':1, 'master':1, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'(AHB_DATA_W/8)', 'name':'ahb_wstrb',    'default':'0', 'description':'Write strobe.'}, \
{'ahb':1, 'apb':1, 'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width':'AHB_DATA_W',     'name':'ahb_rdata',    'default':'0', 'description':'Read data.'}, \
{'ahb':1, 'apb':1, 'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width':'1',              'name':'ahb_ready',    'default':'0', 'description':'Ready. This signal indicates the end of a transfer.'}, \
{'ahb':1, 'apb':0, 'master':0, 'slave':1, 'signal':'`IOB_OUTPUT(', 'width':'1',              'name':'ahb_ready',    'default':'0', 'description':'Ready input. This signal indicates the end of the last transfer.'}, \
{'ahb':1, 'apb':0, 'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width':'1',              'name':'ahb_resp',     'default':'0', 'description':'Transfer response.'}, \
{'ahb':1, 'apb':0, 'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width':'1',              'name':'ahb_exokay',   'default':'1', 'description':'Exclusive transfer response.'}, \
{'ahb':0, 'apb':1, 'master':1, 'slave':1, 'signal':'`IOB_INPUT(',  'width':'1',              'name':'ahb_slverr',   'default':'0', 'description':'Slave error. This signal indicates if the transfer has falied.'}, \
]

#
# IOb Native
#

def make_iob():
    bus = []
    for i in range(len(iob)):
        bus.append(iob[i])
    return bus

#
# AXI4 Full
#

def make_axi_write():
    bus=[]
    for i in range(len(axi_write)):
        bus.append(axi_write[i])
    return bus

def make_axi_read():
    bus=[]
    for i in range(len(axi_read)):
        bus.append(axi_read[i])
    return bus

def make_axi():
    return make_axi_write() + make_axi_read()

#
# AXI4 Lite
#

def make_axil_write():
    bus=[]
    for i in range(len(axi_write)):
        if axi_write[i]['lite'] == 1:
            bus.append(axi_write[i])
            bus[-1]['name'] = bus[-1]['name'].replace('axi_', 'axil_')
            bus[-1]['width'] = bus[-1]['width'].replace('AXI_', 'AXIL_')
    return bus

def make_axil_read():
    bus=[]
    for i in range(len(axi_read)):
        if axi_read[i]['lite'] == 1:
            bus.append(axi_read[i])
            bus[-1]['name'] = bus[-1]['name'].replace('axi_', 'axil_')
            bus[-1]['width'] = bus[-1]['width'].replace('AXI_', 'AXIL_')
    return bus

def make_axil():
    return make_axil_write() + make_axil_read()

#
# AHB
#

def make_ahb():
    bus = []
    for i in range(len(amba)):
        if amba[i]['ahb'] == 1:
            bus.append(amba[i])
    return bus

#
# APB
#

def make_apb():
    bus = []
    for i in range(len(amba)):
        if amba[i]['apb'] == 1:
            bus.append(amba[i])
            bus[-1]['name'] = bus[-1]['name'].replace('ahb_', 'apb_')
            bus[-1]['width'] = bus[-1]['width'].replace('AHB_', 'APB_')
    return bus

#
# Auxiliary Functions
#

def reverse(direction):
    if direction == '`IOB_INPUT(':
        return '`IOB_OUTPUT('
    elif direction == '`IOB_OUTPUT(':
        return '`IOB_INPUT('
    else:
        print("ERROR: reverse_direction : invalid argument")
        quit()
        
def tbsignal(direction):
    if direction == '`IOB_INPUT(':
        return '`IOB_WIRE('
    elif direction == '`IOB_OUTPUT(':
        return '`IOB_VAR_INIT('
    else:
        print("ERROR: tb_reciprocal : invalid argument")
        quit()

def suffix(direction):
    if direction == '`IOB_INPUT(' or direction == '`IOB_VAR_INIT(':
        return '_i'
    elif direction == '`IOB_OUTPUT(' or direction == '`IOB_WIRE(':
        return '_o'
    else:
        print("ERROR: get_signal_suffix : invalid argument")
        quit()

#
# Port
#

def m_port(prefix, fout):
    for i in range(len(table)):
        if table[i]['master'] == 1:
            fout.write(' '+table[i]['signal']+prefix+table[i]['name']+suffix(table[i]['signal'])+', '+table[i]['width']+'), //'+table[i]['description']+'\n')
    
def s_port(prefix, fout):
    for i in range(len(table)):
        if table[i]['slave'] == 1:
            fout.write(' '+reverse(table[i]['signal'])+prefix+table[i]['name']+suffix(reverse(table[i]['signal']))+', '+table[i]['width']+'), //'+table[i]['description']+'\n')

#
# Portmap
#

def portmap(port_prefix, wire_prefix, fout):
    for i in range(len(table)):
        fout.write('.'+port_prefix+table[i]['name']+'('+wire_prefix+table[i]['name']+'), //'+table[i]['description']+'\n')

def m_portmap(port_prefix, wire_prefix, fout):
    for i in range(len(table)):
        if table[i]['master'] == 1:
            fout.write('.'+port_prefix+table[i]['name']+suffix(table[i]['signal'])+'('+wire_prefix+table[i]['name']+'), //'+table[i]['description']+'\n')

def s_portmap(port_prefix, wire_prefix, fout):
    for i in range(len(table)):
        if table[i]['slave'] == 1:
            fout.write('.'+port_prefix+table[i]['name']+suffix(reverse(table[i]['signal']))+'('+wire_prefix+table[i]['name']+'), //'+table[i]['description']+'\n')

def m_m_portmap(port_prefix, wire_prefix, fout):
    for i in range(len(table)):
        if table[i]['master'] == 1:
            fout.write('.'+port_prefix+table[i]['name']+suffix(table[i]['signal'])+'('+wire_prefix+table[i]['name']+suffix(table[i]['signal'])+'), //'+table[i]['description']+'\n')

def s_s_portmap(port_prefix, wire_prefix, fout):
    for i in range(len(table)):
        if table[i]['slave'] == 1:
            fout.write('.'+port_prefix+table[i]['name']+suffix(reverse(table[i]['signal']))+'('+wire_prefix+table[i]['name']+suffix(reverse(table[i]['signal']))+'), //'+table[i]['description']+'\n')

#
# Wire
#

def wire(prefix, fout):
    for i in range(len(table)):
        fout.write('`IOB_WIRE('+prefix+table[i]['name']+', '+table[i]['width']+') //'+table[i]['description']+'\n')

def m_tb_wire(prefix, fout):
    for i in range(len(table)):
        if table[i]['slave'] == 1:
            if tbsignal(table[i]['signal']) == '`IOB_VAR_INIT(':
                fout.write(tbsignal(table[i]['signal'])+prefix+table[i]['name']+suffix(tbsignal(table[i]['signal']))+', '+table[i]['width']+', '+table[i]['default']+') //'+table[i]['description']+'\n')
            else:
                fout.write(tbsignal(table[i]['signal'])+prefix+table[i]['name']+suffix(tbsignal(table[i]['signal']))+', '+table[i]['width']+') //'+table[i]['description']+'\n')
    fout.write('\n')
    
def s_tb_wire(prefix, fout):
    for i in range(len(table)):
        if table[i]['master'] == 1:
            if tbsignal(reverse(table[i]['signal'])) == '`IOB_VAR_INIT(':
                fout.write(tbsignal(reverse(table[i]['signal']))+prefix+table[i]['name']+suffix(tbsignal(reverse(table[i]['signal'])))+', '+table[i]['width']+', '+table[i]['default']+') //'+table[i]['description']+'\n')
            else:
                fout.write(tbsignal(reverse(table[i]['signal']))+prefix+table[i]['name']+suffix(tbsignal(reverse(table[i]['signal'])))+', '+table[i]['width']+') //'+table[i]['description']+'\n')
    fout.write('\n')

#
# Main
#
        
def main ():

    # parse command line arguments
    if len(sys.argv) < 2 or len(sys.argv) > 5:
        print(len(sys.argv))
        print("Usage: ./if_gen.py type [file_prefix port_prefix wire_prefix]")
        print(len(sys.argv))
        print("       where type can defined as")
        print("            iob_m_port: iob native master port")
        print("            iob_s_port: iob native slave port")
        print("            iob_portmap: iob native portmap")
        print("            iob_m_portmap: iob native master portmap")
        print("            iob_s_portmap: iob native slave portmap")
        print("            iob_m_m_portmap: iob native master to master portmap")
        print("            iob_s_s_portmap: iob native slave to slave portmap")
        print("            iob_wire: iob native wires for interconnection")
        print("            iob_m_tb_wire: iob native master wires for testbench")
        print("            iob_s_tb_wire: iob native slave wires for testbench")
        print("")
        print("            axi_m_port: axi full master port")
        print("            axi_s_port: axi full slave port")
        print("            axi_m_write_port: axi full master write port")
        print("            axi_s_write_port: axi full slave write port")
        print("            axi_m_read_port: axi full master read port")
        print("            axi_s_read_port: axi full slave read port")
        print("            axi_portmap: axi full portmap")
        print("            axi_m_portmap: axi full master portmap")
        print("            axi_s_portmap: axi full slave portmap")
        print("            axi_m_m_portmap: axi full master to master portmap")
        print("            axi_s_s_portmap: axi full slave to slave portmap")
        print("            axi_m_write_portmap: axi full master write portmap")
        print("            axi_s_write_portmap: axi full slave write portmap")
        print("            axi_m_m_write_portmap: axi full master to master write portmap")
        print("            axi_s_s_write_portmap: axi full slave to slave write portmap")
        print("            axi_m_read_portmap: axi full master read portmap")
        print("            axi_s_read_portmap: axi full slave read portmap")
        print("            axi_m_m_read_portmap: axi full master to master read portmap")
        print("            axi_s_s_read_portmap: axi full slave to slave read portmap")
        print("            axi_wire: axi full wires for interconnection")
        print("            axi_m_tb_wire: axi full master wires for testbench")
        print("            axi_s_tb_wire: axi full slave wires for testbench")
        print("")
        print("            axil_m_port: axi lite master port")
        print("            axil_s_port: axi lite slave port")
        print("            axil_m_write_port: axi lite master write port")
        print("            axil_s_write_port: axi lite slave write port")
        print("            axil_m_read_port: axi lite master read port")
        print("            axil_s_read_port: axi lite slave read port")
        print("            axil_portmap: axi lite portmap")
        print("            axil_m_portmap: axi lite master portmap")
        print("            axil_s_portmap: axi lite slave portmap")
        print("            axil_m_m_portmap: axi lite master to master portmap")
        print("            axil_s_s_portmap: axi lite slave to slave portmap")
        print("            axil_m_write_portmap: axi lite master write portmap")
        print("            axil_s_write_portmap: axi lite slave write portmap")
        print("            axil_m_m_write_portmap: axi lite master to master write portmap")
        print("            axil_s_s_write_portmap: axi lite slave to slave write portmap")
        print("            axil_m_read_portmap: axi lite master read portmap")
        print("            axil_s_read_portmap: axi lite slave read portmap")
        print("            axil_m_m_read_portmap: axi lite master to master read portmap")
        print("            axil_s_s_read_portmap: axi lite slave to slave read portmap")
        print("            axil_wire: axi lite wires for interconnection")
        print("            axil_m_tb_wire: axi lite master wires for testbench")
        print("            axil_s_tb_wire: axi lite slave wires for testbench")
        print("")
        print("            ahb_m_port: ahb master port")
        print("            ahb_s_port: ahb slave port")
        print("            ahb_portmap: ahb portmap")
        print("            ahb_m_portmap: ahb master portmap")
        print("            ahb_s_portmap: ahb slave portmap")
        print("            ahb_m_m_portmap: ahb master to master portmap")
        print("            ahb_s_s_portmap: ahb slave to slave portmap")
        print("            ahb_wire: ahb wires for interconnection")
        print("            ahb_m_tb_wire: ahb master wires for testbench")
        print("            ahb_s_tb_wire: ahb slave wires for testbench")
        print("")
        print("            apb_m_port: apb master port")
        print("            apb_s_port: apb slave port")
        print("            apb_portmap: apb portmap")
        print("            apb_m_portmap: apb master portmap")
        print("            apb_s_portmap: apb slave portmap")
        print("            apb_m_m_portmap: apb master to master portmap")
        print("            apb_s_s_portmap: apb slave to slave portmap")
        print("            apb_wire: apb wires for interconnection")
        print("            apb_m_tb_wire: apb master wires for testbench")
        print("            apb_s_tb_wire: apb slave wires for testbench")
        quit()

    # bus type
    typ = sys.argv[1]

    # port and wire prefix
    file_prefix = ''
    port_prefix = ''
    wire_prefix = ''
    if len(sys.argv) > 2: file_prefix = sys.argv[2]
    if len(sys.argv) > 3: port_prefix = sys.argv[3]
    if len(sys.argv) > 4: wire_prefix = sys.argv[4]

    # open output .vh file
    fout = open (file_prefix+typ+".vh", 'w')

    # make AXI bus

    global table

    if (typ.find("iob_")>=0):
        table = make_iob()

    if (typ.find("axi_")>=0):
        if (typ.find("write_")>=0): table = make_axi_write()
        elif (typ.find("read_")>=0): table = make_axi_read()
        else: table = make_axi()

    if (typ.find("axil_")>=0):
        if (typ.find("write_")>=0): table = make_axil_write()
        elif (typ.find("read_")>=0): table = make_axil_read()
        else: table = make_axil()

    if (typ.find("ahb_")>=0):
        table = make_ahb()

    if (typ.find("apb_")>=0):
        table = make_apb()

    port_name = typ

    # write pragma for doc production
    if (port_name.find("port")+1 and not port_name.find("portmap")+1):
        fout.write('  //START_IO_TABLE '+port_prefix+port_name+'\n')

    # call function func to generate .vh file
    func_name = port_name.replace("axil_", "").replace("axi_", "").replace("write_", "").replace("read_", "").replace("iob_", "").replace("apb_", "").replace("ahb_", "")
    if (port_name.find("portmap")+1):
        eval(func_name+"('"+port_prefix+"','"+wire_prefix+"', fout)")
    else:
        eval(func_name+"('"+port_prefix+"', fout)")

    fout.close()

if __name__ == "__main__" : main ()

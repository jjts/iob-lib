# (c) 2022-Present IObundle, Lda, all rights reserved
#
# This makefile is used at build-time
#

FPGA_SERVER=$(VIVADO_SERVER)
FPGA_USER=$(VIVADO_USER)
FPGA_SSH_FLAGS=$(VIVADO_SSH_FLAGS)
FPGA_SCP_FLAGS=$(VIVADO_SCP_FLAGS)
FPGA_SYNC_FLAGS=$(VIVADO_SYNC_FLAGS)


ifeq ($(IS_FPGA),1)
FPGA_OBJ=$(FPGA_TOP).bit
else
FPGA_OBJ=$(FPGA_TOP).edif
FPGA_STUB=$(FPGA_TOP)_stub.v
endif

FPGA_ENV:= bash $(VIVADOPATH)/settings64.sh
FPGA_PROG=$(FPGA_ENV) && $(VIVADOPATH)/bin/vivado -nojournal -log vivado.log -mode batch -source vivado/prog.tcl -tclargs $(FPGA_TOP) $(BOARD) $(IS_FPGA) $(USE_EXTMEM)

# work-around for http://svn.clifford.at/handicraft/2016/vivadosig11
export RDI_VERBOSE = False

VIVADO_FLAGS= -nojournal -log vivado.log -mode batch -source vivado/build.tcl -tclargs $(FPGA_TOP) $(BOARD) "$(VSRC)" "$(DEFINES)" "$(IP)" $(IS_FPGA) $(USE_EXTMEM)

$(FPGA_OBJ): $(VSRC) $(VHDR) $(IP) $(wildcard $(BOARD)/*.sdc)
	$(FPGA_ENV) && $(VIVADOPATH)/bin/vivado $(VIVADO_FLAGS) && mv vivado.log reports/

vivado-clean:
	@rm -rf .Xil

.PHONY: vivado-clean

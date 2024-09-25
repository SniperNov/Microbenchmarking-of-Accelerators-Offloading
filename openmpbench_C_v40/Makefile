include Makefile.defs.cray

# Variables
ASMFLAGS = -S # Add any additional flags for assembly generation if needed

.c.o:
	${CC} ${CFLAGS} -c $*.c

.c.s:
	${CC} ${ASMFLAGS} ${CFLAGS} -c $*.c -o $*.s

SYNCOBJS =  syncbench.o common.o
SCHEDOBJS = schedbench.o common.o
CPUVOBJS = cpuvalidate.o common.o
ARRAYOBJS = arraybench_$(IDA).o common.o
TASKOBJS =  taskbench.o common.o

# Define all targets
all: syncbench cpuvalidate schedbench taskbench
# $(MAKE) IDA=1 prog
# $(MAKE) IDA=3 prog
# $(MAKE) IDA=9 prog
	$(MAKE) IDA=27 prog
# $(MAKE) IDA=81 prog
# $(MAKE) IDA=243 prog
# $(MAKE) IDA=729 prog
# $(MAKE) IDA=2187 prog
# $(MAKE) IDA=6561 prog
# $(MAKE) IDA=19683 prog
# $(MAKE) IDA=59049 prog

prog: arraybench_$(IDA)

# Multiple header files due to multiple array sizes, makes header file arraybench_*.h
arraybench_$(IDA).h: arraybench.h
	$(CC) -o $@ -DIDA=$(IDA) $(CPPFLAGS) arraybench.h

# Multiple object files due to multiple array sizes, makes object file arraybench_*.o
arraybench_$(IDA).o: arraybench_$(IDA).h arraybench.c
	$(CC) -c -o $@ $(CFLAGS) -DIDA=$(IDA) arraybench.c

# Multiple executables due to multiple array sizes, makes exe file arraybench_*
arraybench_$(IDA): $(ARRAYOBJS) arraybench.c
	$(CC) -o $@ $(LDFLAGS) $(ARRAYOBJS) $(LIBS) 

cpuvalidate: $(CPUVOBJS)
	$(CC) -o $@ $(LDFLAGS) $(CPUVOBJS) $(LIBS)

syncbench: $(SYNCOBJS)
	$(CC) -o $@ $(LDFLAGS) $(SYNCOBJS) $(LIBS)

schedbench: $(SCHEDOBJS)
	$(CC) -o $@ $(LDFLAGS) $(SCHEDOBJS) $(LIBS)

taskbench: $(TASKOBJS)
	$(CC) -o $@ $(LDFLAGS) $(TASKOBJS) $(LIBS)

# Clean rule
clean:
	-rm syncbench schedbench taskbench cpuvalidate arraybench_* syncbench.o schedbench.o taskbench.o common.o *.s

# New target to generate assembly files
assembly: syncbench.s schedbench.s taskbench.s common.s 
# $(MAKE) IDA=1 asmprog
# $(MAKE) IDA=3 asmprog
# $(MAKE) IDA=9 asmprog
		$(MAKE) IDA=27 asmprog
# $(MAKE) IDA=81 asmprog
# $(MAKE) IDA=243 asmprog
# $(MAKE) IDA=729 asmprog
# $(MAKE) IDA=2187 asmprog
# $(MAKE) IDA=6561 asmprog
# $(MAKE) IDA=19683 asmprog
# $(MAKE) IDA=59049 asmprog

# Target for generating assembly files from arraybench with various IDA
asmprog: arraybench_$(IDA).s

arraybench_$(IDA).s: arraybench_$(IDA).h arraybench.c
	$(CC) $(ASMFLAGS) $(CFLAGS) -DIDA=$(IDA) arraybench.c -o $@

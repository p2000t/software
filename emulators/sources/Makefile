default:
	@echo "To compile M2000, use one of the following:"
	@echo " make allegro5 - Make the Windows version (requires Allegro5 libs)"
	@echo " make x        - Make the Unix/X version"
	@echo " make msdos    - Make the MS-DOS version (DJGPP only)"
	@echo "Please check Makefile.X and Z80.h before compiling M2000"

x:
	make -f Makefile.X

msdos:
	make -f Makefile.MSDOS

windows:
	make -f Makefile.Windows

OBJECTS = M2000.o P2000.o Z80.o Z80Debug.o \
		  Unix.o X.o allegro.o \
          MSDOS.o Asm.o DMA.o INT.o SB.o Bitmap.o
clean:
	rm -f $(OBJECTS)

distclean:
	make clean
	rm -f m2000 m2000.exe


all:
	make -C ../micropython/teensy MEMZIP_DIR=../../DragonTail/memzip_files

upload:
	make -C ../micropython/teensy MEMZIP_DIR=../../DragonTail/memzip_files upload


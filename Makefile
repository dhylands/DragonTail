BUILD = ../../DragonTail/build

all:
	mkdir -p build
	make -C ../micropython/teensy BUILD=$(BUILD) MEMZIP_DIR=../../DragonTail/memzip_files

upload:
	mkdir -p build
	make -C ../micropython/teensy BUILD=$(BUILD) MEMZIP_DIR=../../DragonTail/memzip_files upload


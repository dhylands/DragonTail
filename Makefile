all:
	make -C ../micropython/teensy MEMZIP_DIR=../../Dragon/memzip_files

upload:
	make -C ../micropython/teensy MEMZIP_DIR=../../Dragon/memzip_files upload

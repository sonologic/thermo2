CC=c++
CCFLAGS="-std=c++11"

.PHONY: all clean

all:	main

clean:
		rm -f main *.o

%.o:	%.cc
		$(CC) -c $(CCFLAGS) $< -o $@

main:	main.o Api.o
		$(CC) -o main main.o Api.o

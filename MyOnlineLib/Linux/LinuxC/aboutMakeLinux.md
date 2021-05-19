# why do we really need Make File , why not only GCC?
When you install any software from source, you typically execute commands like — “make”, “make install”, “make clean”, etc. Have you wondered what all these make commands are really making? Sure, we know that it is trying to compile and install the software. But, why make? What does it really do?

**For compiling a single C program, cc command is very helpful. For compiling multiple C programs, Make utility is very helpful.**

Also, C programmers and sysadmins will find it helpful to automate the compilation related tasks using make utility. In this article, let us review how to use make command.

##Create the Makefile for a Simple Compilation
Let us assume that you have the sample C program file called helloworld.c. Using cc command, typically you would compile it as shown below.

```code
$ gcc -o helloworld helloworld.c

OR

$ cc -o helloworld helloworld.c
```

While you don’t need to use make for compiling single a program, the following example will give you an idea on how to use make. Create a makefile as shown below.
```code
$ sudo nano makefile
helloworld : helloworld.c
	cc -o helloworld helloworld.c
```

Execute make to create the helloworld executable as shown below.
```code
$ make helloworld

(or)

$ make
```
Since makefile contains only one target “helloworld”, you can also call make command without any argument as shown above.”make”.Please ensure that both makefile and the source code are present in the same directory, otherwise specify the respective path of source files in makefile.

By default, make command expects the make filename to be either Makefile or makefile. If the make filename is different than any of these two, you should specify that to the make command using -f option as shown below.

```code
$ make -f sample.txt
```

## Create the Makefile to Compile More than One File
For the multiple file compilation, let us use three files — getname.c, getaccno.c and main.c.

Based on these three *.c files, let us create an executable called “getinto”.

Using the cc command, you would typically do the compilation as shown below.

```code
$ cc -o getinfo main.c getname.c getaccno.c header.h
```


You can also compile the individual *.c files as shown below and finally create the “getinfo” executable as shown below.

```code
$ cc -c getname.c
$ cc -c getaccno.c
$ cc -c main.c
$ cc -o getinfo main.o getname.o getaccno.o header.h
```

Using our friendly make utility, you can effectively do this as shown below.

```code
$ sudo nano makefile
getinfo:getname.o getaccno.o main.o header.h 
	cc -o getinfo getname.o getaccno.o main.o header.h 
main.o:main.c 
	cc -c main.c 
getaccno.o:getaccno.c 
	cc -c getaccno.c 
getname.o:getname.c 
	cc -c getname.c 
```

Finally, execute the make command as shown below.

```code
$ make getinfo
```

**Note: Everytime make command gets invoked, it checks and compiles only the file that are modified. This is huge for C programmers, where they typically have multiple C file, and compiling the whole project several times during development phase.**

##Add Target for Cleanup Process
Inside the makefile (or Makefile), you can also add target to cleanup the object files, as shown below.

```code
clean : 
	rm getname.o getaccno.o main.o
```
Now you can clean the object files from the current directory as shown below.

```code
$ make clean
```

Note: Instead of specifying the individual *.o file in the rm command, you can also give rm *.o.

## Variable Handling in Makefile
Inside makefile (or Makefile) you can use variables, which can be used throughout the makefile. An example usage is shown below, where $obj contains all the object file names.

```code
$ sudo nano makefile
obj= getname.o getaccno.o main.o
getinfo: $(obj) header.h
	cc -o getinfo getname.o getaccno.o main.o header.h
main.o:main.c
	cc -c main.c
getaccno.o:getaccno.c
	cc -c getaccno.c
getname.o:getname.c
	cc -c getname.c

clean:
	rm getinfo $(obj)
```

## Simplifying the Makefile Further and Insert Debug Messages inside Makefile

Make utility implicitly invokes the cc -c command to generate .o files for the corresponding .c file. We really don’t need to specify the “cc -c” inside the makefile. So, we can rewrite the makefile to reflect this implicit rule as shown below.

```code
$ sudo nano makefile
obj= getname.o getaccno.o main.o
getinfo: $(obj) header.h
	cc -o getinfo getname.o getaccno.o main.o header.h	
	@echo "make complete."
main.o:
getaccno.o:
getname.o:
clean:
	rm getinfo $(obj)
	@echo "getinfo, $(obj) files are removed."	
```
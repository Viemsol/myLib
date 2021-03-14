A makefile is a set of instructions used by make.exe . 
They can be instructions that build a program, install some files,
 or whatever you want make to do.
A linker is a program that takes object files as input and combines 
them into an output executable (or shared library).
So, a Makefile can invoke the compiler, linker, etc with the appropriate
 source files/object files, but it doesn't actually do the work itself.
Make is a build automation tool that automatically builds executable 
programs and libraries from source code.
by reading files called Makefiles which specify how to derive the target program.
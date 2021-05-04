

// char *argv[3] = {"./a.out", "asdf", "45"};   argv to acess we need to pass it as ** , ponter to *argv[3]
int main( int argc, char **argv ) 
{
    printf("argc = %d",rgc);
     for ( int i=0; i<argc; i++ ) 
    {
        printf("\n[ %d ]= %s", i,argv[i]);
    }
} // end of main()

/* Example 
unix$ ./a.out asdf 45
argc = 3
[0]=./a.out
[1]=asdf
[2]=45
*/
import argparse
import sys

################Configuration#############################

TOOL_DESCRIPTION = "This is CLI test Toll for Test Purpose, version 1.0"
# Create the parser
#With the prog keyword, you specify the name of the program that will be used in the help
#By default, the library uses the value of the sys.argv[0] element to set the name of the program, 
#which as you probably already know is the name of the Python script you have executed. However,
#you can specify the name of your program just by using the prog
parser = argparse.ArgumentParser(description=TOOL_DESCRIPTION)
# Add the arguments
# integer Input ant is positional argument i.e 1st parameter to python script and it must be supplied
parser.add_argument("length", help="get a length of a given object",
                    type=int)

                    
# integer Input ant is positional argument i.e 2nd parameter to python script and it must be supplied
parser.add_argument("cmd", help="get a command, FACT, SQUARE")

# Argument with choice, user can enter only values specified, and its 3rd positional argument and must be supplied
parser.add_argument("hight", help="get a hight of a given object",
                    type=int,choices=[0, 1, 2])
                    
# this is optional Argument, and if type is not specified its always a string, If its specified it takes True else False usage xyz.py --enc
#"store_true" means that, if the option is specified, assign the value True to args.verbose. Not specifying it implies False.
#user can use either "-E" or "--enc"
parser.add_argument("-E","--enc", help="enable Encryption",action="store_true")

# this is optional Argument, and if type is not specified its always a string, for this user must specify value. i.e usage  --Comment "Test string" OR -C "Ok Ok"
parser.add_argument("--Comment", help="Enter comment")

# optional argument but either -v or either -q but not both
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", help="visible", action="store_true")
group.add_argument("-q", "--quiet", help="quit",action="store_true")

#############################Test#######################################
args = parser.parse_args()

print("Length entered is: {}".format(args.length))
print("cmd entered is: {}".format(args.cmd))
print("Hight entered is: {}".format(args.hight))
if(args.enc):
    print(args.enc)
if(args.Comment):
   print("Comment entered is: {}".format(args.Comment))
if(args.verbose):
     print("verbose status: {}".format(args.verbose))
if(args.quiet):
     print("Quit Status: {}".format(args.quiet))

sys.exit(0)

# test on CLI  Valid
#C:\Users\ndhavalikar\Desktop\pythArgParse>python pythArg.py -h
#C:\Users\ndhavalikar\Desktop\pythArgParse>python pythArg.py 7 "cnd1" 0
#C:\Users\ndhavalikar\Desktop\pythArgParse>python pythArg.py 7 "cnd1" 0 -v --Comment "Hi How are you?" 
# test on CLI  in Valid
#C:\Users\ndhavalikar\Desktop\pythArgParse>python pythArg.py 7 "cnd1" 0 --Comment "Hi How are you?" -v -q

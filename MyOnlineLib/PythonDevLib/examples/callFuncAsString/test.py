def myFunc(para):
    print('This is a function. '+para)
    return 1

def myFunc2(para):
    print('This is another function.'+para)
    return 2

print(locals()['myFunc']("a"))
print(globals()['myFunc2']("b"))
import subprocess
# Fetches the list of all usb devices:
result = subprocess.run(['devcon', 'hwids', '=usb'], capture_output=True, text=True)
print(result)
'''
# To display status
#print(devcon_win.HP_TrueVision_HD()) 
# Or
print(devcon_win.HP_TrueVision_HD('status')) 

# To change status
print(devcon_win.HP_TrueVision_HD('enable')) # will show options after 'devcon_win.'
'''
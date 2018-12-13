#**********************************************************************************************************************************************************************#
#                                                              AUTHOR : TASMIYA SANA                                                                                   #                           #
#                                                              DATE   : 05/12/2018                                                                                     #                         #
#**********************************************************************************************************************************************************************#


import subprocess
import re
import os
import socket
import sys,ctypes,platform

arg1 = r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe'
arg2 = '-ExecutionPolicy'
arg3 = 'Unrestricted'
arg4 = r'C:\Users\tasmiya.sana\Desktop\rdp2.ps1'  #set powershell script path

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        raise False

if __name__ == '__main__':

    if platform.system() == "Windows":
        if is_admin():
            main(sys.argv[1:])
        else:
            # Re-run the program with admin rights, don't use __file__ since py2exe won't know about it
            # Use sys.argv[0] as script path and sys.argv[1:] as arguments, join them as lpstr, quoting each parameter or spaces will divide parameters
            lpParameters = ""
            # Litteraly quote all parameters which get unquoted when passed to python
            for i, item in enumerate(sys.argv[0:]):
                lpParameters += '"' + item + '" '
            try:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, lpParameters , None, 1)
            except:
                sys.exit(1)
    else:
        main(sys.argv[1:])

#setting execution policy & checking rdp status via powershell script

F1 = open('Audit_report.txt', 'w+')
psxmlgen = subprocess.Popen([arg1,arg2,arg3,arg4],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(stdout,stderr) = psxmlgen.communicate()

print(stdout)
F1.write('\n'+'***************************************************************'+'\n')
F1.write(str(stdout))
F1.write('\n'+'***************************************************************'+'\n')
F1.write('\n'+'Firewall Status:'+'\n')
F1.close()


#writing services list & firewall status 
os.system(r'netsh advfirewall show all state >> Audit_report.txt')
os.system('echo *************************************************************** >> Audit_report.txt')
os.system('echo Services List: >> Audit_report.txt')
os.system(r'tasklist/svc >> Audit_report.txt') 
os.system('echo *************************************************************** >> Audit_report.txt')
os.system('echo User Account Details: >> Audit_report.txt')

#writing user account details
os.system(r'net user administrator > admin_access.txt')
os.system(r'net user guest >> admin_access.txt')
F4 = open('admin_access.txt', 'r',).read()
F5 = open('Audit_report.txt', 'a',)
F4 = F4.split('\n')
for line in F4:

    if re.search('.*Memberships.*',line) or re.search('.*Password.*',line):
        
        os.system('echo off >> Audit_report.txt')       
        os.system('echo *************************************************************** >> Audit_report.txt')
        
        F5.write(str(line)+'\n')
        os.system('echo off >> Audit_report.txt')       
        os.system('echo *************************************************************** >> Audit_report.txt')  
os.system('echo off >> Audit_report.txt')       
os.system('echo *************************************************************** >> Audit_report.txt')       
F5.close()



#writing hostname in file
F2 = open('Audit_report.txt', 'a')
F2.write('\n'+'--------------------------------------------------------------'+'\n'+'\t')
F2.write('Hostname is:')
var=socket.gethostname()
F2.write(var)
F2.write('\n'+'--------------------------------------------------------------')
F2.write('\n'+'***************************************************************'+'\n')
F2.close()





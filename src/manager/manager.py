import paramiko
import argparse
parser=argparse.ArgumentParser()

def main(start,stop,schedule,speed,ip):
  print('RUN')
    

if __name__ == '__main__':
    parser.add_argument('--start', type=int, required=True, metavar='DDMMYYYY',help='Start date')
    parser.add_argument('--stop', type=int, required=True, metavar='DDMMYYYY',help='End date')
    parser.add_argument('--schedule', choices=['normal','247'], required=True,help='Which work-schedule to use') 
    parser.add_argument('--speed', type=int, required=True, help='Speed multiplier (1-30)',metavar='{10-30}')
    parser.add_argument('--ip', required=True,help='File with list of client IPs',metavar='dir_path')
    args=parser.parse_args()

    main(args.start,args.stop,args.schedule,args.speed)
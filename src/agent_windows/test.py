import argparse
parser=argparse.ArgumentParser()

# Argument for start date in format ddmmyyyy
parser.add_argument('--start', type=int, required=True)
# Argument for stop date in format ddmmyyyy
parser.add_argument('--stop', type=int, required=True)
# Argument for work schedule
parser.add_argument('--schedule', choices=['normal','247'], required=True)
# Argument for speed multiplier
parser.add_argument('--speed', type=int, required=True)

args=parser.parse_args()

print(args.speed)
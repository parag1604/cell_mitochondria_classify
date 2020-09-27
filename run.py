import sys, os

######################
# MODE 1 - PREPROCESS
# MODE 2 - CLASSIFY
######################

def check_and_get_system_args():
    if len(sys.argv) == 2:
        return int(sys.argv[1])
    print("Usage: python run.py <mode=1|2>")
    sys.exit(1)

def main(mode):
    if mode == 1:
        command = "python preprocess.py setting.json"
    elif mode == 2:
        command = "python train.py settings.json"
    else:
        print("INVALID MODE OPTION PROVIDED")
        print("VALID:\nMODE 1 - PREPROCESS\nMODE 2 - CLASSIFY")
        sys.exit(2)
    code = os.system(command)
    if code != 0:
        print("ERROR OCCURRED")
        sys.exit(code)

if __name__ == "__main__":
    main(check_and_get_system_args())
    sys.exit(0)

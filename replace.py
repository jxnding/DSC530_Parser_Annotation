#@Author: Zhaoxiong Ding
import sys

if len(sys.argv)<4:
    print("Format: [Input] [To Be Replaced] [Replacer]")
    sys.exit()

print(sys.argv[1].replace(sys.argv[2],sys.argv[3]))
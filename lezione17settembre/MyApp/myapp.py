import time
import sys
sys.stdout = open("./file_per_le_print.tx","w+")
i = 1
while (i<10):
    print("Ciao")
    sys.stdout()
    time.sleep(3)
    i+=1
sys.stdout.close()
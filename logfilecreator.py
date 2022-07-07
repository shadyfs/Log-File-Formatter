import os
import struct
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--bin', type=str, required=True)
parser.add_argument('--txt', type=str, required=True)
args = parser.parse_args()
filename = args.bin# show an "Open" dialog box and return the path to the selected file
writefile = args.txt
fileLocation = 0
file_size = os.path.getsize(filename)
message_list =[]
candump_list =[]
count = 0
with open(filename,'rb') as binFile:
    while(fileLocation < file_size):
        if count % 500 == 0:
            with open(writefile, 'a') as output:
                for row in candump_list:
                    output.write(str(row) + '\n')
            output.close()
            candump_list = []
        block = binFile.read(512) #read every 512 bytes
        fileLocation += 512
        for recordNum in range(19): #Parse through CAN message
            record = block[4 + recordNum * 25:4 + (recordNum + 1) * 25]
            channel = record[0]
            timeSeconds = struct.unpack("<L",record[1:5])[0]
            timeMicrosecondsAndDLC = struct.unpack("<L",record[13:17])[0]
            timeMicroseconds = timeMicrosecondsAndDLC & 0x00FFFFFF
            abs_time = timeSeconds + timeMicroseconds * 0.000001
            ID = struct.unpack("<L",record[9:13])[0]
            message_bytes = record[17:25]
            candump_list.append("({:0.6f}) can{:0.0f} {:08X}#{}".format(abs_time,channel,ID,''.join(["{:02X}".format(b) for b in message_bytes])))
            count = count +1

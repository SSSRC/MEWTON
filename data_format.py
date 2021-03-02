# coding: UTF-8
import re

def nyanpath(path):
    f = open(path,'r')
    lines = f.readlines()
    telem = []
    telems = []
    packet_num = -1
    filled_bytes = 0
    for line in lines:
        bytes = line.split()
        if bytes == None:
            continue
        if int(bytes[1], 16) == 0 and packet_num != -1:
             print('Packet Number ERROR!!\nTERMINATED')
             sys.exit()
        elif int(bytes[1], 16) == packet_num +1:
            bytes.pop(0)
            bytes.pop(0)
            packet_num += 1
        else:
            bytes.pop(0)
            byte_num = int(bytes.pop(0), 16) * 254
            while(byte_num % 35 != 0):
                bytes.pop(0)
                byte_num += 1

        #35バイトずつ取り出してtelemsの配列に格納する処理を書く
        for byte in bytes:
            #print(filled_bytes)
            if filled_bytes == 0:
                if int(byte, 16) != 0:
                    print('header number error')
                    break
                else:
                    telem = []
                    telem.append(byte)
                    filled_bytes += 1
            elif filled_bytes == 34:
                telem.append(byte)
                telems.append(telem)
                telem = []
                filled_bytes = 0
            else:
                telem.append(byte)
                filled_bytes += 1
    f.close()
    return telems

def filter(text):
    flag = re.search('[0-9]{3}:', text)
    if re.search('000:', text):
        flag = None

    if flag:
        new_text = re.sub('[0-9]{3}:', "", text)
        new_text = new_text.split('  ')
        new_text = new_text[2]
        new_text = new_text.split(" ")
        return new_text

def direwolf(path):
    f = open(path)
    s = f.readlines()
    telem = []
    telems = []

    for value in s:
        fixed = filter(value)
        if fixed:
            for byte in fixed:
                telem.append(byte)
        if len(telem) == 35:
            telems.append(telem)
            telem = []
    f.close()
    return telems

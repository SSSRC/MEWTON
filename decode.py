# coding: UTF-8
from math import log, pow
from calculate_ad_data import calculate_V, calculate_bat_I, calculate_R, calculate_T, calculate_solar_I_minus_y_dep, calculate_solar_I_plus_y_undep, calculate_solar_I_plus_x, calculate_solar_I_minus_x, calculate_solar_I_plus_y_dep, calculate_solar_I_minus_z, calculate_txCW_FM_I, calculate_rx_modem_I, calculate_mis5V_I, calculate_mobc5V_I, calculate_misbus_I

def judge_mode(mode_num):
    if(mode_num == 0 or mode_num == 9):
        return "antenna-expansion mode"
    elif(mode_num == 1):
        return "safe mode"
    elif(mode_num == 2):
        return "heater mode"
    elif(mode_num == 3):
        return "cw mode"
    elif(mode_num >= 4 and mode_num <= 7):
        return "user-setting-%d mode"%(mode_num-3)
    elif(mode_num == 8):
        return "command response mode"
    elif(mode_num == 10):
        return "DR format mode"
    else:
        return "???mode unknown???"

def judge_abnor(abnor_stat1,abnor_stat2):
    abnor_out = ''
    abnor_head = ['', '\n']
    while(len(abnor_stat2)!=4):
        abnor_stat2 = "0" + abnor_stat2
    put_flag=0
    if(int(abnor_stat1[3:4]) == 1):
        abnor_out = abnor_out + abnor_head[put_flag] + "fuse1 worked"
        put_flag=1
    if(int(abnor_stat2[2:3]) == 1):
        abnor_out = abnor_out + abnor_head[put_flag] + "fuse2 worked"
        put_flag=1
    if(int(abnor_stat2[3:4]) == 1):
        abnor_out = abnor_out + abnor_head[put_flag] + "fuse3 worked"
        put_flag=1
    if(int(abnor_stat2[0:1]) == 1):
        for i in range(8):
            if int(abnor_stat1[0:3],2) == 0:
                abnor_out = abnor_out + abnor_head[put_flag] + 'MOBC had a trouble'
                put_flag = 1
                break
            elif int(abnor_stat1[0:3],2) == i:
                abnor_out = abnor_out + abnor_head[put_flag] + 'Charasteristics Abnor ' + str(i)
                put_flag = 1
                break
    else:
        if int(abnor_stat1[0:1]) == 1:
            abnor_out = abnor_out + abnor_head[put_flag] + 'Wrong Command'
        if int(abnor_stat1[1:2]) == 1:
            abnor_out = abnor_out + abnor_head[put_flag] + 'UART B2M Abnor'
        if int(abnor_stat1[2:3]) == 1:
            abnor_out = abnor_out + abnor_head[put_flag] + 'SD Abnor'
    if(int(abnor_stat2[1:2]) == 1):
        abnor_out = abnor_out + abnor_head[put_flag] + "battery voltage was low"
        put_flag=1
    if(put_flag==0):
        abnor_out = abnor_out + "None"
    return abnor_out


def decode_FP(bytes): #Functional Performance (機能性能)
    decoded_list = []
    for byte in bytes:
        #テレメトリ全体
        full_telemetry = ''.join(byte)

        #テレメトリID
        telem_id = int(byte[0], 16)
        if telem_id != 0:
            print('Telemetry ID Error')
            return -1

        #モードID
        mode_id = int(byte[1], 16) % 16

        #BOBC時刻
        bobc_tlm = byte[2] + byte[3] + byte[4] + byte[5]
        bobc_time = int(bobc_tlm, 16)

        #異常ステータス
        abnor_stat1 = int(byte[6], 16)
        abnor_stat1 = format(int(byte[6][0], 16), '04b')
        abnor_stat2 = format(int(byte[6][1], 16), '04b')
        abnormity_status = judge_abnor(abnor_stat1,abnor_stat2)

        #ADデータ
        bat_V = "%.2f"%calculate_V(int(byte[7],16))
        bat_A = "%.2f"%calculate_bat_I(int(byte[8],16))
        bat_T = "%.2f"%calculate_T(int(byte[9],16))

        solar_A_minusY_dep = "%.2f"%calculate_solar_I_minus_y_dep(int(byte[10],16))
        solar_A_plusY_undep = "%.2f"%calculate_solar_I_plus_y_undep(int(byte[11],16))
        solar_A_plusX = "%.2f"%calculate_solar_I_plus_x(int(byte[12],16))
        solar_A_minusX = "%.2f"%calculate_solar_I_minus_x(int(byte[13],16))
        solar_A_plusY_dep = "%.2f"%calculate_solar_I_plus_y_dep(int(byte[14],16))
        solar_A_minusZ = "%.2f"%calculate_solar_I_minus_z(int(byte[15],16))

        transceiver_T = "%.2f"%calculate_T(int(byte[16],16))
        mission_board_T = "%.2f"%calculate_T(int(byte[17],16))
        plusX_T = "%.2f"%calculate_T(int(byte[18],16))
        plusZ_T = "%.2f"%calculate_T(int(byte[19],16))
        plusY_T = "%.2f"%calculate_T(int(byte[20],16))
        minusY_T = "%.2f"%calculate_T(int(byte[21],16))
        minusX_T = "%.2f"%calculate_T(int(byte[22],16))
        minusZ_T = "%.2f"%calculate_T(int(byte[23],16))
        eps1_T = "%.2f"%calculate_T(int(byte[24],16))

        #バイト番号25 割当なし
        tx_A = "%.2f"%calculate_txCW_FM_I(int(byte[26],16))
        rx_A = "%.2f"%calculate_rx_modem_I(int(byte[27],16))
        #バイト番号28 割当なし
        mission_board_5V_A = "%.2f"%calculate_mis5V_I(int(byte[29],16))
        mobc_5V_A = "%.2f"%calculate_mobc5V_I(int(byte[30],16))
        mission_board_bus_A = "%.2f"%calculate_misbus_I(int(byte[31],16))

        bussystem_5V2_V = "%.2f"%calculate_V(int(byte[32],16))
        bussystem_bus_V = "%.2f"%calculate_V(int(byte[33],16))

        #RSSI
        if int(byte[34],16) == 255:
            rssi = 'No Receipt'
        else:
            rssi = "%.2f"%calculate_V(int(byte[34],16))

        decoded_list.append([ full_telemetry, telem_id, mode_id, bobc_time, abnormity_status, bat_V, bat_A, bat_T, solar_A_minusY_dep, solar_A_plusY_undep, solar_A_plusX, solar_A_minusX, solar_A_plusY_dep, solar_A_minusZ, transceiver_T, mission_board_T, plusX_T, plusZ_T, plusY_T, minusY_T, minusX_T, minusZ_T, eps1_T, tx_A, rx_A, mission_board_5V_A, mobc_5V_A, mission_board_bus_A, bussystem_5V2_V, bussystem_bus_V, rssi ])
        for i in range(len(decoded_list[-1])):
            try:
                if decoded_list[-1][i] == 'nan':
                    continue
                decoded_list[-1][i] = float(decoded_list[-1][i])
            except:
                pass
    return decoded_list

# coding: UTF-8
import datetime
from math import log, pow
from calculate_ad_data import calculate_V, calculate_bat_I, calculate_R, calculate_T, calculate_solar_I_minus_y_dep, calculate_solar_I_plus_y_undep, calculate_solar_I_plus_x, calculate_solar_I_minus_x, calculate_solar_I_plus_y_dep, calculate_solar_I_minus_z, calculate_txCW_FM_I, calculate_rx_modem_I, calculate_mis5V_I, calculate_mobc5V_I, calculate_misbus_I
import sys
import openpyxl
import os
import data_format
import decode

def make_log(data, filename):
    #decoded_time = str(datetime.datetime.now())
    if not os.path.exists('mewton_log'):
        os.mkdir('mewton_log')
    wb = openpyxl.Workbook()
    ws = wb.worksheets[0]
    index = ['テレメトリ', 'テレメトリID', 'ミッションモードID', 'BOBC時刻 [sec]', '異常ステータス', 'バッテリー電圧 [V]', 'バッテリー電流 [A]', 'バッテリー温度 [deg]', '-Y Deployed Solar Current [A]', '＋Y Undeployed Solar Current [A]', '＋X Solar Current [A]', '-X Solar Current [A]', '＋Y Deployed Solar [A]', '-Z Solar Current [A]', 'Tranceiver Temp [A]', 'Mission-Board Temp [deg]', '＋X Panel Temp [deg]', '＋Z Panel Temp [deg]', '＋Y Panel Temp [deg]', '-Y Panel Temp [deg]', '-X Panel Temp [deg]', '-Z Panel Temp [deg]', 'EPS1-Shunt Temp [deg]', 'TX(CW/FM) Current [A]', 'RX, Modem(RX) etc. Current [A]', 'Mission-Board 5V-Line Current [A]', 'MOBC 5V-Line Current [A]', 'Mission-Board Bus-Line Current [A]', 'Bus-System 5V-Line2 Voltage [V]', 'Bus-System Bus-Line Voltage [V]', 'RSSI [V]']
    for i in range(len(index)):
        ws.cell(1, i+1).value = index[i]

    for i in range(len(data)):
        for k in range(len(data[0])):
            ws.cell(i+2, k+1).value = data[i][k]

    filename = filename.split('.txt')[0]
    wb.save("./mewton_log/" + filename + ".xlsx")


if __name__ == '__main__':
    print('input path:')
    #path = input()
    #path = 'BUS_function_AO40_GMSK9k6_2.txt'
    path = 'bus_fuction_log_direwolf.txt'
    #telems = data_format.nyanpath(path)
    telems = data_format.direwolf(path)
    make_log(decode.decode_FP(telems), path)

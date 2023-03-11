# Author: Malyshev Sergey 2022, Ekaterinburg
#
# References
#  - http://www.batronix.com/pdf/Rigol/ProgrammingGuide/DP800_ProgrammingGuide_EN.pdf
#
# Instructions
# - Download and install National Instruments VISA software (https://www.ni.com/visa/ OR https://skachat.freedownloadmanager.org/Windows-PC/NI-VISA-Runtime/FREE-5.4.html)
# - Download and install PyVISA (eg. "pip install -U pyvisa" from CMD)
# - Download and install PySimpleGUI ("python -m pip install pysimplegui" from CMD)

import PySimpleGUI as sg # https://www.pysimplegui.org/en/latest/cookbook/
import pyvisa
import time

#--------------------------GLOBAL VARIABLES CONST---------------------------------
VERSION_MAJOR = 0
VERSION_MINOR = 3
VERSION_PATCH = 0

DELAY_AFTER_MEAS = 0.01

DEBUG = False
NO_DEBUG_CONNECT_PSU = True # False для запуска без активного подключения
#--------------------------GENERAL CLASS------------------------------------------
# https://proglib.io/p/python-oop

class Canal_DP832(object): # Создали класс 
    measPower = 0 # Свойства класса(атрибуты)
    measVolt = 0
    measCurrent = 0
    
    def __init__(self, number, voltage, current, ovp, ocp): # Конструктор
        self.channelNumber = number
        self.voltage = voltage
        self.current = current
        self.ovp = ovp
        self.ocp = ocp
        
     
    def run_channel(self, voltage, current, ocp): # Создали метод запуска канала
        if NO_DEBUG_CONNECT_PSU:
            print(psu.query("*IDN?"))
            psu.write(f":INST CH{self.channelNumber}") # Select channel
            psu.write(f":CURR {current}")   # Set the current 
            psu.write(f":CURR:PROT {ocp}")  # Set the overcurrent protection value
            psu.write(":CURR:PROT:STAT ON") # Enable the overcurrent protection function
            psu.write(f":VOLT {voltage}")   # Set the voltage
            psu.write(f":OUTP CH{self.channelNumber},ON") # Enable the output of channel """
        window['quote'].update(f'CH{self.channelNumber}: {voltage} V, {current} A, OCP {ocp} A')
    
    def off_channel(self):
        if NO_DEBUG_CONNECT_PSU:
            psu.write(f":OUTP CH{self.channelNumber},OFF") # Disable the output of channel
        print(f"channel {self.channelNumber} DP832A disable")
        window['quote'].update(f'Output CH{self.channelNumber} disable')
           
#--------------------------GENERAL FUNCTIONS---------------------------------------
def off_all_channel():
    ch1.off_channel();
    ch2.off_channel();
    ch3.off_channel();
    window['quote'].update('Output all disable')
        
def measVolt(chan): 			
    cmd1 = ':MEAS:VOLT? CH%s' %chan
    V = psu.query(cmd1)
    V = float(V)
    time.sleep(DELAY_AFTER_MEAS)
    return V

def measCurrent(chan): 			
    cmd1 = ':MEAS:CURR? CH%s' %chan
    C = psu.query(cmd1)
    C = float(C)
    time.sleep(DELAY_AFTER_MEAS)
    return C

def measPower(chan): 			
    cmd1 = ':MEAS:POWE? CH%s' %chan
    P = psu.query(cmd1)
    P = float(P)
    time.sleep(DELAY_AFTER_MEAS)
    return P

def mainMeas(): 
    def debugOut(): 			
        print("Power: " + str(ch1.power) + " mW" + "    Voltage: " + str(ch1.volt) + " V" + "    Current: " + str(ch1.current) + " A")
        print("Power: " + str(ch2.power) + " mW" + "    Voltage: " + str(ch2.volt) + " V" + "    Current: " + str(ch2.current) + " A")
        print("Power: " + str(ch3.power) + " mW" + "    Voltage: " + str(ch3.volt) + " V" + "    Current: " + str(ch3.current) + " A")  
    
    ch1.measPower = measPower(1) # Создали атрибут объекта	
    ch1.measVolt = round(measVolt(1), 2)
    ch1.measCurrent = round(measCurrent(1), 4)
 
    ch2.measPower = measPower(2)	
    ch2.measVolt = round(measVolt(2), 2)
    ch2.measCurrent = round(measCurrent(2), 4)
    
    ch3.measPower = measPower(3)	
    ch3.measVolt = round(measVolt(3), 2)
    ch3.measCurrent = round(measCurrent(3), 4)
    
    if DEBUG: 
        debugOut()
    
def screenUpdateValue():
    window['-OUTPUT_VOLT_1-'].update(str(ch1.measVolt) + " V") 
    window['-OUTPUT_CURR_1-'].update(str(ch1.measCurrent) + " A") 
    window['-OUTPUT_VOLT_2-'].update(str(ch2.measVolt) + " V")  
    window['-OUTPUT_CURR_2-'].update(str(ch2.measCurrent) + " A") 
    window['-OUTPUT_VOLT_3-'].update(str(ch3.measVolt) + " V")  
    window['-OUTPUT_CURR_3-'].update(str(ch3.measCurrent) + " A")    
  
      
sg.theme('Dark Amber')  # Let's set our own color theme (sg.theme_previewer() # Просмотр всех доступных тем)
rm = pyvisa.ResourceManager()

if NO_DEBUG_CONNECT_PSU:
    try: 
      psu = rm.open_resource('USB0::0x1AB1::0x0E11::DP8B241601290::INSTR')
    except:
      sg.popup('Error: Not connection DP832A') 
      
# Экземпляры классов(объекты)
ch1 = Canal_DP832(1, 24, 0.2, 33, 3) # Установить номер канала и значения параметров по умолчанию 
ch2 = Canal_DP832(2, 24, 0.3, 33, 3) 
ch3 = Canal_DP832(3, 5, 0.3, 5.5, 0.5) 

#-------Сreate the GUI-----------
layout =  [ [sg.Frame('CH1', [[sg.Button('Set CH1'), sg.Button('Reset CH1'), sg.Text(f'{ch1.measVolt}', size=(6, 1), font=('Helvetica', 16), key='-OUTPUT_VOLT_1-', text_color='yellow'), sg.Text(f'{ch1.measCurrent}', size=(7, 1), font=('Helvetica', 16), key='-OUTPUT_CURR_1-', text_color='yellow')], 
            [sg.Text('Voltage, V:', size=(8, 1)), sg.Text(f'{ch1.voltage}', size=(4, 1), font=('Helvetica 11'), key='voltage_out'), sg.InputText(key='-VOLTAGE-', size=(6, 1)), sg.Text('OVP:', size=(4, 1)), sg.Text(f'{ch1.ovp}', size=(2, 1), font=('Helvetica 11'), key='OVP_out'), sg.InputText(key='-OVP-', size=(6, 1))],
            [sg.Text('Current, A:', size=(8, 1)), sg.Text(f'{ch1.current}', size=(4, 1), font=('Helvetica 11'), key='current_out'), sg.InputText(key='-CURRENT-', size=(6, 1)), sg.Text('OCP:', size=(4, 1)), sg.Text(f'{ch1.ocp}', size=(2, 1), font=('Helvetica 11'), key='OCP_out'), sg.InputText(key='-OCP-', size=(6, 1))]])],
            
            [sg.Frame('CH2', [[sg.Button('Set CH2'), sg.Button('Reset CH2'), sg.Text(f'{ch2.measVolt}', size=(6, 1), font=('Helvetica', 16), key='-OUTPUT_VOLT_2-', text_color = 'cyan'), sg.Text(f'{ch2.measCurrent}', size=(7, 1), font=('Helvetica', 16), key='-OUTPUT_CURR_2-', text_color = 'cyan')], 
            [sg.Text('Voltage, V:', size=(8, 1)), sg.Text(f'{ch2.voltage}', size=(4, 1), font=('Helvetica 11'), key='voltage_out2'), sg.InputText(key='-VOLTAGE2-', size=(6, 1)), sg.Text('OVP:', size=(4, 1)), sg.Text(f'{ch2.ovp}', size=(2, 1), font=('Helvetica 11'), key='OVP_out2'), sg.InputText(key='-OVP2-', size=(6, 1))],
            [sg.Text('Current, A:', size=(8, 1)), sg.Text(f'{ch2.current}', size=(4, 1), font=('Helvetica 11'), key='current_out2'), sg.InputText(key='-CURRENT2-', size=(6, 1)), sg.Text('OCP:', size=(4, 1)), sg.Text(f'{ch2.ocp}', size=(2, 1), font=('Helvetica 11'), key='OCP_out2'), sg.InputText(key='-OCP2-', size=(6, 1))]])],
            
            [sg.Frame('CH3', [[sg.Button('Set CH3'), sg.Button('Reset CH3'), sg.Text(f'{ch3.measVolt}', size=(6, 1), font=('Helvetica', 16), key='-OUTPUT_VOLT_3-', text_color = 'magenta'), sg.Text(f'{ch3.measCurrent}', size=(7, 1), font=('Helvetica', 16), key='-OUTPUT_CURR_3-', text_color = 'magenta')], 
            [sg.Text('Voltage, V:', size=(8, 1)), sg.Text(f'{ch3.voltage} ', size=(4, 1), font=('Helvetica 11'), key='voltage_out3'), sg.InputText(key='-VOLTAGE3-', size=(6, 1)), sg.Text('OVP:', size=(4, 1)), sg.Text(f'{ch3.ovp}', size=(2, 1), font=('Helvetica 11'), key='OVP_out3'), sg.InputText(key='-OVP3-', size=(6, 1))],
            [sg.Text('Current, A:', size=(8, 1)), sg.Text(f'{ch3.current}', size=(4, 1), font=('Helvetica 11'), key='current_out3'), sg.InputText(key='-CURRENT3-', size=(6, 1)), sg.Text('OCP:', size=(4, 1)), sg.Text(f'{ch3.ocp}', size=(2, 1), font=('Helvetica 11'), key='OCP_out3'), sg.InputText(key='-OCP3-', size=(6, 1))]])],
            
            [sg.Frame('Fast preset', [[sg.Button('CH1'), sg.Button('CH2'), sg.Button('CH3'), sg.Button('OFF')]]), sg.Frame('System', [[sg.Button('Exit', size=(5, 1)), sg.Button('About', size=(5, 1))]])],
            [sg.Text('This is GUI driving Rigol DP832A', key='quote')]
         ]
         
window = sg.Window('Run DP832A', layout)

while True:
  
    event, values = window.read(timeout=200)   # Read the event that happened and the values dictionary, timeout=200 - не блокирующий режим  
    if DEBUG: print(event, values)
    
    if event == sg.WIN_CLOSED or event == 'Exit':     # If user closed window with X or if user clicked "Exit" button then exit
        break
    if event == 'About': 
        sg.popup('Run DP832A', f'Version {VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}', '2022, Ekaterinburg', sg.get_versions())    
        
    if event == 'Set CH1':
        if values['-VOLTAGE-'] > '0':
            ch1.voltage = values['-VOLTAGE-']
            window['voltage_out'].update(values['-VOLTAGE-'])
        if values['-CURRENT-'] > '0':
            ch1.current = values['-CURRENT-']
            window['current_out'].update(values['-CURRENT-'])
        if values['-OVP-'] > '0':
            ch1.ovp = values['-OVP-']
            window['OVP_out'].update(values['-OVP-'])
        if values['-OCP-'] > '0':
            ch1.ocp = values['-OCP-']
            window['OCP_out'].update(values['-OCP-'])  
        ch1.run_channel(ch1.voltage, ch1.current, ch1.ocp)

    if event == 'Reset CH1':
        ch1.off_channel()
                
    if event == 'Set CH2':
        if values['-VOLTAGE2-'] > '0':
            ch2.voltage = values['-VOLTAGE2-']
            window['voltage_out2'].update(values['-VOLTAGE2-'])
        if values['-CURRENT2-'] > '0':
            ch2.current = values['-CURRENT2-']
            window['current_out2'].update(values['-CURRENT2-'])
        if values['-OVP2-'] > '0':
            ch2.ovp = values['-OVP2-']
            window['OVP_out2'].update(values['-OVP2-'])
        if values['-OCP2-'] > '0':
            ch2.ocp = values['-OCP2-']
            window['OCP_out2'].update(values['-OCP2-'])  
        ch2.run_channel(ch2.voltage, ch2.current, ch2.ocp)
                
    if event == 'Reset CH2':
        ch1.off_channel()
    
    if event == 'Set CH3':
        if values['-VOLTAGE3-'] > '0':
            ch3.voltage = values['-VOLTAGE3-']
            window['voltage_out3'].update(values['-VOLTAGE3-'])
        if values['-CURRENT3-'] > '0':
            ch3.current = values['-CURRENT3-']
            window['current_out3'].update(values['-CURRENT3-'])
        if values['-OVP3-'] > '0':
            ch3.ovp = values['-OVP3-']
            window['OVP_out3'].update(values['-OVP3-'])
        if values['-OCP3-'] > '0':
            ch3.ocp = values['-OCP3-']
            window['OCP_out3'].update(values['-OCP3-'])  
        ch3.run_channel(ch3.voltage, ch3.current, ch3.ocp)
                
    if event == 'Reset CH3':
        ch1.off_channel()
                
    if event == 'CH1':
        ch1.run_channel(ch1.voltage, ch1.current, ch1.ocp)
        
    if event == 'CH2':
        ch2.run_channel(ch2.voltage, ch2.current, ch2.ocp)
        
    if event == 'CH3':
        ch3.run_channel(ch3.voltage, ch3.current, ch3.ocp)
        
    if event == 'OFF':
        off_all_channel()

    if NO_DEBUG_CONNECT_PSU:
        mainMeas()
        
    screenUpdateValue()

     
window.close()

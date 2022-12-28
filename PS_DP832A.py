# Author: Malyshev Sergey 2022
#
# References
#  - http://www.batronix.com/pdf/Rigol/ProgrammingGuide/DP800_ProgrammingGuide_EN.pdf
#
# Instructions
# - Download and install National Instruments VISA software (https://www.ni.com/visa/ OR https://skachat.freedownloadmanager.org/Windows-PC/NI-VISA-Runtime/FREE-5.4.html)
# - Download and install PyVISA (eg. "pip install -U pyvisa" from CMD)
# - Download and install PySimpleGUI ("python -m pip install pysimplegui" from CMD)

import PySimpleGUI as sg
import pyvisa

sg.theme('Dark Amber')  # Let's set our own color theme

rm = pyvisa.ResourceManager()
psu = rm.open_resource('USB0::0x1AB1::0x0E11::DP8B241601290::INSTR')

work_mode = 'CH1'

# sg.theme_previewer() # Просмотр всех доступных тем
# https://proglib.io/p/python-oop

class canal_DP832(object): # Создали класс 
  voltage = 0 # Свойства классов
  current = 0
  ovp = 0
  ocp = 0
 
ch1 = canal_DP832() # Экземпляры классов
ch2 = canal_DP832()
ch3 = canal_DP832()

ch1.voltage = 24
ch1.current = 0.2
ch1_ovp = 33
ch1_ocp = 0.3

ch2.voltage = 24
ch2.current = 0.3
ch2_ovp = 33
ch2_ocp = 0.4

ch3.voltage = 5
ch3.current = 0.3
ch3.ovp = 5.5
ch3.ocp = 0.5

layout =  [ [sg.Frame('CH1', [[sg.Button('Set CH1')], [sg.Text('Voltage, V:'), sg.Text(f'{ch1.voltage}', font=('Helvetica 11'), key='voltage_out'), sg.InputText(key='-VOLTAGE-', size=(6, 1)), sg.Text('OVP:'), sg.Text(f'{ch1_ovp}', font=('Helvetica 11'), key='OVP_out'), sg.InputText(key='-OVP-', size=(6, 1))],
            [sg.Text('Current, A:'), sg.Text(f'{ch1.current}', font=('Helvetica 11'), key='current_out'), sg.InputText(key='-CURRENT-', size=(6, 1)), sg.Text('OCP:'), sg.Text(f'{ch1_ocp}', font=('Helvetica 11'), key='OCP_out'), sg.InputText(key='-OCP-', size=(6, 1))]])],
            
            [sg.Frame('CH2', [[sg.Button('Set CH2')], [sg.Text('Voltage, V:'), sg.Text(f'{ch2.voltage}', font=('Helvetica 11'), key='voltage_out2'), sg.InputText(key='-VOLTAGE2-', size=(6, 1)), sg.Text('OVP:'), sg.Text(f'{ch2_ovp}', font=('Helvetica 11'), key='OVP_out2'), sg.InputText(key='-OVP2-', size=(6, 1))],
            [sg.Text('Current, A:'), sg.Text(f'{ch2.current}', font=('Helvetica 11'), key='current_out2'), sg.InputText(key='-CURRENT2-', size=(6, 1)), sg.Text('OCP:'), sg.Text(f'{ch2_ocp}', font=('Helvetica 11'), key='OCP_out2'), sg.InputText(key='-OCP2-', size=(6, 1))]])],
            
            [sg.Frame('CH3', [[sg.Button('Set CH3')], [sg.Text('Voltage, V:'), sg.Text(f'{ch3.voltage} ', font=('Helvetica 11'), key='voltage_out3'), sg.InputText(key='-VOLTAGE3-', size=(6, 1)), sg.Text('OVP:'), sg.Text(f'{ch3.ovp}', font=('Helvetica 11'), key='OVP_out3'), sg.InputText(key='-OVP3-', size=(6, 1))],
            [sg.Text('Current, A:'), sg.Text(f'{ch3.current}', font=('Helvetica 11'), key='current_out3'), sg.InputText(key='-CURRENT3-', size=(6, 1)), sg.Text('OCP:'), sg.Text(f'{ch3.ocp}', font=('Helvetica 11'), key='OCP_out3'), sg.InputText(key='-OCP3-', size=(6, 1))]])],
            
            [sg.Frame('Fast preset', [[sg.Button('CH1'), sg.Button('CH2'), sg.Button('CH3'), sg.Button('OFF'), sg.Button('Exit')]])],
            [sg.Text('This is GUI driving Rigol DP832A', key='quote')]
         ]


def run_channel_1 ():
        work_mode ='CH1'
        print(psu.query("*IDN?"))
        psu.write(":INST CH1") # Select CH1
        psu.write(f":CURR {ch1.current}") # Set the current of CH1 to 0,2A
        psu.write(f":CURR:PROT {ch1_ocp}")  # Set the overcurrent protection value of CH1 to 0,4A
        psu.write(":CURR:PROT:STAT ON") # Enable the overcurrent protection function of CH1
        psu.write(f":VOLT {ch1.voltage}") # Set the voltage of CH1to 20,5V
        psu.write(":OUTP CH1,ON") # Enable the output of CH1  
        window['quote'].update(f'{work_mode}: {ch1.voltage} V, {ch1.current} A, OCP {ch1_ocp} A')
        
def run_channel_2 ():
        work_mode ='CH2'
        print(psu.query("*IDN?"))
        psu.write(":INST CH2") # Select CH1
        psu.write(f":CURR {ch2.current}") # Set the current of CH1 to 5A
        psu.write(f":CURR:PROT {ch2_ocp}")  # Set the overcurrent protection value of CH1 to 5.3A
        psu.write(":CURR:PROT:STAT ON") # Enable the overcurrent protection function of CH1
        psu.write(f":VOLT {ch2.voltage}") # Set the voltage of CH1to 5V
        psu.write(":OUTP CH2,ON") # Enable the output of CH1
        window['quote'].update(f'{work_mode}: {ch2.voltage} V, {ch2.current} A, OCP {ch2_ocp} A')

def run_channel_3 ():
        work_mode ='CH3'
        print(psu.query("*IDN?"))
        psu.write(":INST CH3") # Select CH1
        psu.write(f":CURR {ch3.current}") # Set the current of CH1 to 0.250A
        psu.write(f":CURR:PROT {ch3.ocp}")  # Set the overcurrent protection value of CH1 to 0.3A
        psu.write(":CURR:PROT:STAT ON") # Enable the overcurrent protection function of CH3
        psu.write(f":VOLT {ch3.voltage}") # Set the voltage of CH3 to 5V
        psu.write(":OUTP CH3,ON") # Enable the output of CH3
        window['quote'].update(f'{work_mode}: {ch3.voltage} V, {ch3.current} A, OCP {ch3.ocp} A')

def off_channel ():
        work_mode ='CH1'
        psu.write(":OUTP CH1,OFF") # disable the output of CH1
        psu.write(":OUTP CH2,OFF") # disable the output of CH2
        psu.write(":OUTP CH3,OFF") # disable the output of CH2
        print("DP832A disable")
        window['quote'].update('Output disable')
       
        
#STEP 2 - create the window
window = sg.Window('Run DP832A', layout)

# STEP3 - the event loop
while True:
    event, values = window.read()   # Read the event that happened and the values dictionary
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':     # If user closed window with X or if user clicked "Exit" button then exit
        break
    if event == 'Set CH1':
        match work_mode:
            case 'CH1':
                if values['-VOLTAGE-'] > '0':
                    ch1.voltage = values['-VOLTAGE-']
                    window['voltage_out'].update(values['-VOLTAGE-'])
                if values['-CURRENT-'] > '0':
                    ch1.current = values['-CURRENT-']
                    window['current_out'].update(values['-CURRENT-'])
                if values['-OVP-'] > '0':
                    ch1_ovp = values['-OVP-']
                    window['OVP_out'].update(values['-OVP-'])
                if values['-OCP-'] > '0':
                    ch1_ocp = values['-OCP-']
                    window['OCP_out'].update(values['-OCP-'])  
                run_channel_1 ()
            case 'CH2':
                pass
            case 'CH3':
                pass
                
    if event == 'Set CH2':
                if values['-VOLTAGE2-'] > '0':
                    ch2.voltage = values['-VOLTAGE2-']
                    window['voltage_out2'].update(values['-VOLTAGE2-'])
                if values['-CURRENT2-'] > '0':
                    ch2.current = values['-CURRENT2-']
                    window['current_out2'].update(values['-CURRENT2-'])
                if values['-OVP2-'] > '0':
                    ch2_ovp = values['-OVP2-']
                    window['OVP_out2'].update(values['-OVP2-'])
                if values['-OCP2-'] > '0':
                    ch2_ocp = values['-OCP2-']
                    window['OCP_out2'].update(values['-OCP2-'])  
                run_channel_2 ()
    
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
                run_channel_3 ()
                
    if event == 'CH1':
        run_channel_1 ()
        
    if event == 'CH2':
        run_channel_2 ()
        
    if event == 'CH3':
        run_channel_3 ()
        
    if event == 'OFF':
        off_channel ()
        
window.close()

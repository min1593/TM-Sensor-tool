import PySimpleGUI as sg
import pandas as pd

sg.theme('dark grey 9') # Add a touch of color

# All the stuff inside your window.
layout = [  [sg.Text('Spectrum Analyzer Data for TM')],
            [sg.Text('File Path :'), sg.InputText(key='path'), sg.FileBrowse('Browse', key= 'getfile', file_types=(("CSV files","*.csv"),)), sg.Button('OK', key='OK')],
            [sg.Text('   30  MHz :', size=(20,1), justification='center'), sg.InputText('', size=(30,1), key='out_1')],
            [sg.Text('  300  MHz :', size=(20,1), justification='center'), sg.InputText('', size=(30,1), key='out_2')],
            [sg.Text('  900  MHz :', size=(20,1), justification='center'), sg.InputText('', size=(30,1), key='out_3')],
            [sg.Text('All Data < -40 dBm:',size=(20,1),justification='center'), sg.Text('',key='out_4')],
            [sg.Column([[sg.Exit()]], justification='r')]
         ]

# Create the Window
window = sg.Window('Spectrum Analyzer Data for TM', layout, font='12')


# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks exit
       break
    if event == 'OK':
        filename = values['getfile']
        window['path'].update(filename)
        data = pd.read_csv(filename,skiprows=12)
        df = pd.DataFrame(data)
        try:
                if df.iloc[460]['Frequency(Hz)'] == 900000000:
                    window['out_1'].update(df.iloc[0]['Amplitude(dBm)'])
                    window['out_2'].update(df.iloc[143]['Amplitude(dBm)'])
                    window['out_3'].update(df.iloc[460]['Amplitude(dBm)'])
                    if df.index[df['Amplitude(dBm)']<-40].tolist() == []:
                        window['out_4'].update('Pass', text_color='white', font='12')
                    else:
                        window['out_4'].update('Fail', text_color='red', font='Arial 18 bold')
                else:
                    window['out_1'].update("")
                    window['out_2'].update("")
                    window['out_3'].update("")
                    window['out_4'].update("")
                    sg.popup_error('資料不符合')

        except:
                window['out_1'].update("")
                window['out_2'].update("")
                window['out_3'].update("")
                window['out_4'].update("")
                sg.popup_error('資料不符合')    

window.close()

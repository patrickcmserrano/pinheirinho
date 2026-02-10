import ac
import acsys
import math
import time
import os
import configparser
import queue
import threading

class SafeConfigParser(configparser.ConfigParser):

    def read(self, filenames, encoding=None):
        if isinstance(filenames, str):
            filenames = [filenames]
        for filename in filenames:
            try:
                with open(filename, 'r', encoding=encoding) as fp:
                    self._read(fp, filename)
            except (IOError, OSError) as e:
                log_message("Erro ao ler o arquivo %s: %s" % (filename, e))

    def _read(self, fp, fpname):
        cursect = None
        for lineno, line in enumerate(fp, start=1):
            line = line.strip()
            if not line or line.startswith(('#', ';')):
                continue
            if line.startswith('[') and line.endswith(']'):
                sectname = line[1:-1].strip()
                cursect = self._sections.setdefault(sectname, self._dict())
            else:
                if cursect is None:
                    raise configparser.MissingSectionHeaderError(fpname, lineno, line)
                if '=' in line:
                    key, value = map(str.strip, line.split('=', 1))
                    cursect[key] = value
                else:
                    log_message("Linha inválida ignorada: %s" % line)

button1_state = False
button1_enabled = True
button2_state = False
button2_enabled = True
button3_state = False
button3_enabled = True
button4_state = False
button4_enabled = True
button5_state = False
button5_enabled = True
button6_state = False
button6_enabled = True
button7_state = False
button7_enabled = True
button8_state = False
button8_enabled = True
button9_state = False
button9_enabled = True
button10_state = False
button10_enabled = True
button11_state = False
button11_enabled = True
button12_state = False
button12_enabled = True
button13_state = False
button13_enabled = True
button14_state = False
button14_enabled = True
button15_state = False
button15_enabled = True
button16_state = False
button16_enabled = True
button17_state = False
button17_enabled = True

buttons_enabled = True
button_last_click = 0  # Armazena o tempo do último clique de qualquer botão

button3_state = False
button4_state = False
button5_state = False
button6_state = False
button7_state = False
button8_state = False
button9_state = False
button10_state = False 
button11_state = False
button12_state = False
button13_state = False
button14_state = False
button15_state = False
button16_state = False
button17_state = False

prestage_left = None
prestage_right = None
stage_left = None
stage_right = None
extra_button5 = None
extra_button6 = None
extra_button7 = None
extra_button8 = None
extra_button9 = None
extra_button10 = None
extra_button11 = None
extra_button12 = None
extra_button13 = None
extra_button14 = None
extra_button15 = None
extra_button16 = None
extra_button17 = None
falseStart = False 
reaction_time = 0.000
best_reaction_time = float('inf')
timer_start = 0
timer_active = False
previous_pin_on_fire = True  
reset_time = 5  
reaction_time_label = None
best_reaction_time_label = None

message_queue = queue.Queue()  
send_queue = queue.Queue()    

buttons = {
    1: {"state": False, "enabled": True, "update_func": "update_button1_state1"},
    2: {"state": False, "enabled": True, "update_func": "update_button2_state1"},
    3: {"state": False, "enabled": True, "update_func": "update_button3_state1"},
    4: {"state": False, "enabled": True, "update_func": "update_button4_state1"},
    5: {"state": False, "enabled": True, "update_func": "update_button5_state1"},
    6: {"state": False, "enabled": True, "update_func": "update_button6_state1"},
    7: {"state": False, "enabled": True, "update_func": "update_button7_state1"},
    8: {"state": False, "enabled": True, "update_func": "update_button8_state1"},
    9: {"state": False, "enabled": True, "update_func": "update_button9_state1"},
    10: {"state": False, "enabled": True, "update_func": "update_button10_state1"},
    11: {"state": False, "enabled": True, "update_func": "update_button11_state1"},
    12: {"state": False, "enabled": True, "update_func": "update_button12_state1"},
    13: {"state": False, "enabled": True, "update_func": "update_button13_state1"},
    14: {"state": False, "enabled": True, "update_func": "update_button14_state1"},
    15: {"state": False, "enabled": True, "update_func": "update_button15_state1"},
    16: {"state": False, "enabled": True, "update_func": "update_button16_state1"},
    17: {"state": False, "enabled": True, "update_func": "update_button17_state1"},
}


def get_race_ini_path():
    def find_file(start_path, file_name):
        for root, dirs, files in os.walk(start_path):
            if file_name in files:
                return os.path.join(root, file_name)
        return None

    user_home = os.path.expanduser("~")
    
    onedrive_paths = [
        os.path.join(user_home, 'OneDrive', 'Documents'),
        os.path.join(user_home, 'OneDrive', 'Documentos')
    ]
    
    documentos_paths = [
        os.path.join(user_home, 'Documents'),
        os.path.join(user_home, 'Documentos')
    ]
    
    for path in onedrive_paths + documentos_paths:
        race_ini_path = find_file(path, 'race.ini')
        if race_ini_path:
            return race_ini_path

    other_drives = ['D:', 'E:', 'F:', 'G:', 'H:', 'I:','J:','K:'] 
    for drive in other_drives:
        for path in documentos_paths:
            custom_path = path.replace(user_home, drive)
            race_ini_path = find_file(custom_path, 'race.ini')
            if race_ini_path:
                return race_ini_path

        root_documents_paths = [
            os.path.join(drive, 'Documents'),
            os.path.join(drive, 'Documentos')
        ]
        for root_path in root_documents_paths:
            race_ini_path = find_file(root_path, 'race.ini')
            if race_ini_path:
                return race_ini_path

    raise FileNotFoundError("Arquivo race.ini não encontrado em nenhum dos caminhos especificados.")

def get_track_name_from_ini():
    race_ini_path = get_race_ini_path()
    config = configparser.ConfigParser()
    config.read(race_ini_path)
    if 'RACE' in config:
        if 'TRACK' in config['RACE']:
            return config['RACE']['TRACK'].strip()
        else:
            raise ValueError("A chave TRACK não foi encontrada na seção RACE do arquivo race.ini.")
    else:
        raise ValueError("A seção RACE não foi encontrada no arquivo race.ini.")

def get_config_path():
    track_name = get_track_name_from_ini()
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    three_levels_up = current_directory
    for _ in range(3):
        three_levels_up = os.path.dirname(three_levels_up)
    return os.path.join(three_levels_up, 'content', 'tracks', track_name, 'extension', 'ext_config.ini')

def verificar_arquivo(caminho_arquivo):
    return caminho_arquivo and os.path.isfile(caminho_arquivo)

try:
    caminho_arquivo = get_config_path()
    track_name = get_track_name_from_ini()
    print("Caminho do arquivo de configuração:", caminho_arquivo)
    ac.console("Pista detectada: %s" % track_name)
except Exception as e:
    print("Erro:", e)

is_max = False 
track_config_path = caminho_arquivo 
On = (1000, 1000, 1000)  
Off = (0, 0, 0)  
Yellow = (1500,1500,0)
Green = (0,1500,0)
Red = (2000,0,0)
Blue = (0,0,255)
material_name= None

timer_running = False
timer_start_time = 0
timer_duration = 5  
pin_on=False
pin_on_fire=False
is_left=False
is_right=False



pass_counter = 0
previous_lap_time = 0.0
first_pass_counted = False


def update_pass_counter():
    global pass_counter, previous_lap_time, first_pass_counted,button9_state,button15_state,is_left,is_right,falseStart,pin_on_fire
    car_id = 0
    current_lap_time = ac.getCarState(car_id, acsys.CS.LapTime)

    is_stage_left = is_car_in_stage_left()
    is_stage_right = is_car_in_stage_right()

    speed = ac.getCarState(0, acsys.CS.SpeedKMH)

    if pin_on_fire and speed > 1 and not falseStart:
        if is_stage_left and is_left:
            add_log_message("FalseStartLeft")
            enviar_mensagem_chat("False Start")
            button9_state = True
            update_button9_state()
            falseStart = True
        elif is_stage_right and is_right:
            add_log_message("FalseStartRight")
            enviar_mensagem_chat("False Start")
            button15_state = True
            update_button15_state()
            falseStart = True


    if not first_pass_counted:
        if current_lap_time > 0:
            first_pass_counted = True
            previous_lap_time = current_lap_time
            pass_counter += 1
            add_log_message("Crossed the line")
            enviar_mensagem_chat("Crossed the line")
    else:
        if current_lap_time < previous_lap_time:
            pass_counter += 1
            add_log_message("Crossed the line")
            enviar_mensagem_chat("Crossed the line")



    previous_lap_time = current_lap_time

    ac.setText(label_pass_counter, "Pass Count: {}".format(pass_counter))


def turn_emissive(material_name, color):
    r, g, b = color
    try:
        add_log_message("Ativando Emissive Máximo para %s com cor %s" % (material_name, color))
        set_emissive_in_config(material_name, r, g, b)  
    except Exception as e:
        add_log_message("Erro ao ativar emissivo: %s" % str(e))

def set_emissive_in_config(material_name, r, g, b):
    """
    Abre o arquivo ext_config.ini da pista e modifica os valores emissive do material especificado.
    """
    try:
        add_log_message("Modificando o ext_config.ini")

        with open(track_config_path, 'r') as file:
            lines = file.readlines()

        value_set = False
        new_lines = []

        for line in lines:
            
            if "MATERIALS = " + material_name in line:
                value_set = True
            if value_set and "VALUE_0" in line:
                new_lines.append("VALUE_0 = {}, {}, {}\n".format(r, g, b))
                value_set = False  
            else:
                new_lines.append(line)

        
        if value_set:
            new_lines.append("VALUE_0 = {}, {}, {}\n".format(r, g, b))

        
        with open(track_config_path, 'w') as file:
            file.writelines(new_lines)

        add_log_message("Emissive alterado com sucesso!")
    
    except Exception as e:
        add_log_message("Erro ao modificar ext_config.ini: %s" % str(e))



def enviar_mensagem_chat(mensagem):
    try:
        send_queue.put(mensagem)  # Coloca a mensagem na fila para envio
        add_log_message("Mensagem enfileirada: " + mensagem)
    except Exception as e:
        add_log_message("Erro ao enfileirar mensagem: " + str(e))



def onChatMessage(message, author):
    global button1_state, button1_enabled, button2_state, button2_enabled, button3_state, button3_enabled
    global button4_state, button4_enabled, button5_state, button5_enabled, button6_state, button6_enabled
    global button7_state, button7_enabled, button8_state, button8_enabled, button9_state, button9_enabled
    global button10_state, button10_enabled, button11_state, button11_enabled, button12_state, button12_enabled
    global button13_state, button13_enabled, button14_state, button14_enabled, button15_state, button15_enabled
    global button16_state, button16_enabled, button17_state, button17_enabled,buttons_enabled,button_last_click
    global timer_running, timer_start_time,pin_on,is_left,is_right,log_label
    global message_queue,pin_on_fire
    
    try:
        message_queue.put((message, author))  
        add_log_message("Mensagem recebida de {}: {}".format(author, message))
    except Exception as e:
        add_log_message("Erro ao receber mensagem: " + str(e))
    #add_log_message("%s: %s" % (author, message))
    
    if "StageLeftOn" in message:
        
        if button1_enabled and time.time() - button_last_click > 0.95:
           
            button1_state = True
            update_button1_state1()
            
            button_last_click = time.time()
            disable_all_buttons()  
    
    if "StageLeftOff" in message:
        if button1_enabled and time.time() - button_last_click > 0.95:
            button1_state = False
            update_button1_state1()
            button_last_click = time.time()
            disable_all_buttons()  


    if "PreStageLeft_On" in message:
        if button3_enabled and time.time() - button_last_click > 0.95:
            button3_state = True
            update_button3_state1()
            button_last_click = time.time()
            disable_all_buttons()  
    
    if "PreStageLeft_Off" in message:
        if button3_enabled and time.time() - button_last_click > 0.95:
            button3_state = False
            update_button3_state1()
            button_last_click = time.time()
            disable_all_buttons()  
    

    if "StageRightOn" in message:
        if button2_enabled and time.time() - button_last_click > 0.95:
            button2_state = True
            update_button2_state1()
            button_last_click = time.time()
            disable_all_buttons()  

    if "StageRightOff" in message:
        if button2_enabled and time.time() - button_last_click > 0.95:
            button2_state = False
            update_button2_state1()
            button_last_click = time.time()
            disable_all_buttons()  


    if "PreStageRight_On" in message:
        if button4_enabled and time.time() - button_last_click > 0.95:
            button4_state = True
            update_button4_state1()
            button_last_click = time.time()
            disable_all_buttons()  

    if "PreStageRight_Off" in message:
        if button4_enabled and time.time() - button_last_click > 0.95:
            button4_state = False
            update_button4_state1()
            button_last_click = time.time()
            disable_all_buttons()  

    if "Yellow_1_On" in message:
        if button5_enabled and time.time() - button_last_click > 0.95:
            button5_state = True
            update_button5_state1()
            button_last_click = time.time()
            disable_all_buttons()  

    if "Yellow_1_Off" in message:
        if button5_enabled and time.time() - button_last_click > 0.95:
            button5_state = False
            update_button5_state1()
            button_last_click = time.time()
            disable_all_buttons()  

    if "Yellow_2_On" in message:
        if button6_enabled and time.time() - button_last_click > 0.9:
            button6_state = True
            update_button6_state1()
            button_last_click = time.time()
            disable_all_buttons() 

    if "Yellow_2_Off" in message:
       if button6_enabled and time.time() - button_last_click > 0.95:
            button6_state = False
            update_button6_state1()
            button_last_click = time.time()
            disable_all_buttons()  

    if "Yellow_3_On" in message:
        if button7_enabled and time.time() - button_last_click > 0.95:
            button7_state = True
            update_button7_state1()
            button_last_click = time.time()
            disable_all_buttons()  


    if "Yellow_3_Off" in message:
        if button7_enabled and time.time() - button_last_click > 0.95:
            button7_state = False
            update_button7_state1()
            button_last_click = time.time()
            disable_all_buttons()  


    if "Yellow_4_On" in message:
        if button11_enabled and time.time() - button_last_click > 0.95:
            button11_state = True
            update_button11_state1()
            button_last_click = time.time()
            disable_all_buttons()  

    if "Yellow_4_Off" in message:
        if button11_enabled and time.time() - button_last_click > 0.95:
            button11_state = False
            update_button11_state1()
            button_last_click = time.time()
            disable_all_buttons()  

    if "Yellow_5_On" in message:
        if button12_enabled and time.time() - button_last_click > 0.95:
            button12_state = True
            update_button12_state1()
            button_last_click = time.time()
            disable_all_buttons()  


    if "Yellow_5_Off" in message:
        if button12_enabled and time.time() - button_last_click > 0.95:
            button12_state = False
            update_button12_state1()
            button_last_click = time.time()
            disable_all_buttons()  


    if "Yellow_6_On" in message:
        if button13_enabled and time.time() - button_last_click > 0.95:
            button13_state = True
            update_button13_state1()
            button_last_click = time.time()
            disable_all_buttons()  

    if "Yellow_6_Off" in message:
        if button13_enabled and time.time() - button_last_click > 0.95:
            button13_state = False
            update_button13_state1()
            button_last_click = time.time()
            disable_all_buttons()  

    if "Green_L_On" in message:
        if button8_enabled and time.time() - button_last_click > 0.95:
            button8_state = True
            update_button8_state1()
            button_last_click = time.time()
            disable_all_buttons()  

    if "Green_L_Off" in message:
        if button8_enabled and time.time() - button_last_click > 0.95:
            button8_state = False
            update_button8_state1()
            button_last_click = time.time()
            disable_all_buttons()  

    if "Green_R_On" in message:
        if button14_enabled and time.time() - button_last_click > 0.95:
            button14_state = True
            update_button14_state1()
            button14_last_click = time.time()
            disable_all_buttons()  

    if "Green_R_Off" in message:
        if button14_enabled and time.time() - button_last_click > 0.95:
            button14_state = False
            update_button14_state1()
            button_last_click = time.time()
            disable_all_buttons()  

    if "Red_L_On" in message:
        if button9_enabled and time.time() - button_last_click > 0.95:
            button9_state = True
            update_button9_state1()
            button_last_click = time.time()
            disable_all_buttons()  

    if "Red_L_Off" in message:
       if button9_enabled and time.time() - button_last_click > 0.95:
            button9_state = False
            update_button9_state1()
            button_last_click = time.time()
            disable_all_buttons()  

    if "Red_R_On" in message:
        if button15_enabled and time.time() - button_last_click > 0.95:
            button15_state = True
            update_button15_state1()
            button_last_click = time.time()
            disable_all_buttons()  

    if "Red_R_Off" in message:
        if button15_enabled and time.time() - button_last_click > 0.95:
            button15_state = False
            update_button15_state1()
            button_last_click = time.time()
            disable_all_buttons()  

    if "Pin_Left_On" in message:
        if  button10_enabled and time.time() - button_last_click > 0.95:
            button10_state = True
            update_button10_state1()
            button_last_click = time.time()
            disable_all_buttons()
            pin_on=True
            pin_on_fire=True
            is_left=True
            is_right=False

            if button10_state:
                Turn_Off_Before_Pin()
                timer_running = True
                timer_start_time = time.time()
            else:
                timer_running = False

            
   


    if "Pin_Right_On" in message:
        if  button16_enabled and time.time() - button_last_click > 0.95:
            button16_state = True
            update_button16_state1()
            button_last_click = time.time()
            disable_all_buttons()
            pin_on=True
            pin_on_fire=True
            is_left=False
            is_right=True

            if button16_state:
                Turn_Off_Before_Pin()
                timer_running = True
                timer_start_time = time.time()
            else:
                timer_running = False

              

    if "Pin_On" in message:
        if  button17_enabled and time.time() - button_last_click > 0.95:
            button17_state = True
            update_button17_state1()
            button_last_click = time.time()
            disable_all_buttons()
            pin_on=True
            pin_on_fire=True
            is_left=True
            is_right=True

            if button17_state:
                Turn_Off_Before_Pin()
                timer_running = True
                timer_start_time = time.time()
            else:
                timer_running = False


def handle_button_state(button_id, state_value=True):
    global button_last_click
    button = buttons.get(button_id)
    if button and button["enabled"] and (time.time() - button_last_click > 0.95):
        button["state"] = state_value
        update_func = globals().get(button["update_func"])
        if update_func:
            update_func()
        button_last_click = time.time()
        disable_all_buttons()

def handle_pin_left_on():
    global pin_on, pin_on_fire, is_left, is_right, timer_running, timer_start_time, button_last_click
    button_id = 10
    button = buttons.get(button_id)
    if button and button["enabled"] and (time.time() - button_last_click > 0.95):
        button["state"] = True
        update_button10_state1()
        button_last_click = time.time()
        disable_all_buttons()
        pin_on = True
        pin_on_fire = True
        is_left = True
        is_right = False

        Turn_Off_Before_Pin()
        timer_running = True
        timer_start_time = time.time()

def handle_pin_right_on():
    global pin_on, pin_on_fire, is_left, is_right, timer_running, timer_start_time, button_last_click
    button_id = 16
    button = buttons.get(button_id)
    if button and button["enabled"] and (time.time() - button_last_click > 0.95):
        button["state"] = True
        update_button16_state1()
        button_last_click = time.time()
        disable_all_buttons()
        pin_on = True
        pin_on_fire = True
        is_left = False
        is_right = True

        Turn_Off_Before_Pin()
        timer_running = True
        timer_start_time = time.time()

def handle_pin_on():
    global pin_on, pin_on_fire, is_left, is_right, timer_running, timer_start_time, button_last_click
    button_id = 17
    button = buttons.get(button_id)
    if button and button["enabled"] and (time.time() - button_last_click > 0.95):
        button["state"] = True
        update_button17_state1()
        button_last_click = time.time()
        disable_all_buttons()
        pin_on = True
        pin_on_fire = True
        is_left = True
        is_right = True

        Turn_Off_Before_Pin()
        timer_running = True
        timer_start_time = time.time()

def process_messages():
    global message_queue

    while True:
        try:
            message, author = message_queue.get()
            if "StageLeftOn" in message:
                handle_button_state(1, True)
            elif "StageLeftOff" in message:
                handle_button_state(1, False)
            elif "PreStageLeft_On" in message:
                handle_button_state(3, True)
            elif "PreStageLeft_Off" in message:
                handle_button_state(3, False)
            elif "StageRightOn" in message:
                handle_button_state(2, True)
            elif "StageRightOff" in message:
                handle_button_state(2, False)
            elif "PreStageRight_On" in message:
                handle_button_state(4, True)
            elif "PreStageRight_Off" in message:
                handle_button_state(4, False)
            elif "Yellow_1_On" in message:
                handle_button_state(5, True)
            elif "Yellow_1_Off" in message:
                handle_button_state(5, False)
            elif "Yellow_2_On" in message:
                handle_button_state(6, True)
            elif "Yellow_2_Off" in message:
                handle_button_state(6, False)
            elif "Yellow_3_On" in message:
                handle_button_state(7, True)
            elif "Yellow_3_Off" in message:
                handle_button_state(7, False)
            elif "Yellow_4_On" in message:
                handle_button_state(11, True)
            elif "Yellow_4_Off" in message:
                handle_button_state(11, False)
            elif "Yellow_5_On" in message:
                handle_button_state(12, True)
            elif "Yellow_5_Off" in message:
                handle_button_state(12, False)
            elif "Yellow_6_On" in message:
                handle_button_state(13, True)
            elif "Yellow_6_Off" in message:
                handle_button_state(13, False)
            elif "Green_L_On" in message:
                handle_button_state(8, True)
            elif "Green_L_Off" in message:
                handle_button_state(8, False)
            elif "Green_R_On" in message:
                handle_button_state(14, True)
            elif "Green_R_Off" in message:
                handle_button_state(14, False)
            elif "Red_L_On" in message:
                handle_button_state(9, True)
            elif "Red_L_Off" in message:
                handle_button_state(9, False)
            elif "Red_R_On" in message:
                handle_button_state(15, True)
            elif "Red_R_Off" in message:
                handle_button_state(15, False)
            elif "Pin_Left_On" in message:
                handle_pin_left_on()
            elif "Pin_Right_On" in message:
                handle_pin_right_on()
            elif "Pin_On" in message:
                handle_pin_on()
            else:
                add_log_message("Mensagem desconhecida: " + message)
            
            message_queue.task_done()
        except Exception as e:
            add_log_message("Error processing message: " + str(e))
            message_queue.task_done()


def process_send_queue():
    while True:
        try:
            mensagem = send_queue.get()

            ac.sendChatMessage(mensagem)
            add_log_message("Mensagem enviada: " + mensagem)

            send_queue.task_done()

            time.sleep(1)
        except Exception as e:
            add_log_message("Erro ao enviar mensagem: " + str(e))
            send_queue.task_done()


def enable_all_buttons():
    for button_id in buttons:
        buttons[button_id]["enabled"] = True


def disable_all_buttons():
    for button_id in buttons:
        buttons[button_id]["enabled"] = False
    threading.Timer(1, enable_all_buttons).start()
   


lines_coordinates = {
     "bdl_interlagos_toyo_livre": {
        "stage_left_start": (107.5, -1.78, 231.08),
        "stage_left_end": (100.69, -1.9, 229.2),
        "stage_right_start": (107.96, -1.82, 231.23),
        "stage_right_end": (114.53, -1.65, 233.02),
        "pre_stage_left_start": (107.44, -1.75, 231.29),
        "pre_stage_left_end": (100.63, -1.9, 229.4),
        "pre_stage_right_start": (107.9, -1.79, 231.43), 
        "pre_stage_right_end": (114.47, -1.63, 233.23),  
    },
         "bdl_interlagos_arrancada": {
        "stage_left_start": (107.5, -1.78, 231.08),
        "stage_left_end": (100.69, -1.9, 229.2),
        "stage_right_start": (107.96, -1.82, 231.23),
        "stage_right_end": (114.53, -1.65, 233.02),
        "pre_stage_left_start": (107.44, -1.75, 231.29),
        "pre_stage_left_end": (100.63, -1.9, 229.4),
        "pre_stage_right_start": (107.9, -1.79, 231.43), 
        "pre_stage_right_end": (114.47, -1.63, 233.23),  
    },
    "bdl_curitiba21_drag": {
        "stage_left_start": (-62.85, -1.04, -166.34),
        "stage_left_end": (-56.75, -1.02, -168.98),
        "stage_right_start": (-69.61, -0.979, -163.51),
        "stage_right_end": (-63.22, -0.977, -166.24),
        "pre_stage_left_start": (-62.94, -1.01, -166.54),
        "pre_stage_left_end": (-56.85, -1.04, -169.21),
        "pre_stage_right_start": (-69.66, -0.993, -163.65),
        "pre_stage_right_end": (-63.37, -1.02, -166.35),
    },
         "bdl_velopark_dragbdlnoprep": {
        "stage_left_start": (43.12, -0.026, -323.73),
        "stage_left_end": (36.26, -0.0188, -324.15),
        "stage_right_start": (35.79, -0.0219, -324.17),
        "stage_right_end": (28.82, -0.0275, -324.6),
        "pre_stage_left_start": (43.13, -0.029, -323.89),
        "pre_stage_left_end": (36.27, -0.0181, -324.31),
        "pre_stage_right_start": (35.8, -0.0213, -324.34), 
        "pre_stage_right_end": (28.83, -0.0247, -324.77),  
    },
         "bdl_velopark_dragbdl": {
        "stage_left_start": (43.12, -0.026, -323.73),
        "stage_left_end": (36.26, -0.0188, -324.15),
        "stage_right_start": (35.79, -0.0219, -324.17),
        "stage_right_end": (28.82, -0.0275, -324.6),
        "pre_stage_left_start": (43.13, -0.029, -323.89),
        "pre_stage_left_end": (36.27, -0.0181, -324.31),
        "pre_stage_right_start": (35.8, -0.0213, -324.34), 
        "pre_stage_right_end": (28.83, -0.0247, -324.77),  
    },
    "bdl_goiania_": {
        "stage_left_start": (263.93, 0.0756, 275.58),
        "stage_left_end": (259.89, 0.0726, 279.45),
        "stage_right_start": (264.25, 0.0593, 275.23),
        "stage_right_end": (268.29, 0.0763, 271.35),
        "pre_stage_left_start": (264.05, 0.0836, 275.71),
        "pre_stage_left_end": (260.03, 0.0845, 279.59),
        "pre_stage_right_start": (264.4, 0.0354, 275.38),
        "pre_stage_right_end": (268.42, 0.0584, 271.48),
    },
   "bdl_spid_prep201": {
        "stage_left_start": (37.91, -0.0596, -338.59),
        "stage_left_end": (44.77, -0.0433, -338.18),
        "stage_right_start": (37.44, -0.0608, -338.66),
        "stage_right_end": (30.47, -0.0417, -339.03),
        "pre_stage_left_start": (37.93, -0.0531, -338.78),
        "pre_stage_left_end": (44.78, -0.0394, -338.35),
        "pre_stage_right_start": (37.45, -0.0452, -338.8),
        "pre_stage_right_end": (30.48, -0.0422, -339.21),
    },
   "bdl_spid_noprep201": {
        "stage_left_start": (37.91, -0.0596, -338.59),
        "stage_left_end": (44.77, -0.0433, -338.18),
        "stage_right_start": (37.44, -0.0608, -338.66),
        "stage_right_end": (30.47, -0.0417, -339.03),
        "pre_stage_left_start": (37.93, -0.0531, -338.78),
        "pre_stage_left_end": (44.78, -0.0394, -338.35),
        "pre_stage_right_start": (37.45, -0.0452, -338.8),
        "pre_stage_right_end": (30.48, -0.0422, -339.21),
            },
   "bdl_spid_especial_prep": {
        "stage_left_start": (37.91, -0.0596, -338.59),
        "stage_left_end": (44.77, -0.0433, -338.18),
        "stage_right_start": (37.44, -0.0608, -338.66),
        "stage_right_end": (30.47, -0.0417, -339.03),
        "pre_stage_left_start": (37.93, -0.0531, -338.78),
        "pre_stage_left_end": (44.78, -0.0394, -338.35),
        "pre_stage_right_start": (37.45, -0.0452, -338.8),
        "pre_stage_right_end": (30.48, -0.0422, -339.21),
                    },
   "bdl_spid_especial_noprep": {
        "stage_left_start": (37.91, -0.0596, -338.59),
        "stage_left_end": (44.77, -0.0433, -338.18),
        "stage_right_start": (37.44, -0.0608, -338.66),
        "stage_right_end": (30.47, -0.0417, -339.03),
        "pre_stage_left_start": (37.93, -0.0531, -338.78),
        "pre_stage_left_end": (44.78, -0.0394, -338.35),
        "pre_stage_right_start": (37.45, -0.0452, -338.8),
        "pre_stage_right_end": (30.48, -0.0422, -339.21),
    },
     "bdl_mato_grosso_treino": {
        "stage_left_start": (65.17, -0.0233, 208.57),
        "stage_left_end": (59.37, 0.0226, 210.64),
        "stage_right_start": (65.62, 0.0165, 208.44),
        "stage_right_end": (70.64, 0.0194, 206.88),
        "pre_stage_left_start": (65.27, 0.03, 208.88),
        "pre_stage_left_end": (59.38, 0.0433, 210.66),
        "pre_stage_right_start": (65.71, -0.007, 208.71),
        "pre_stage_right_end": (70.72, 0.0281, 207.15),
    },
     "bdl_mato_grosso_campeonato": {
        "stage_left_start": (65.17, -0.0233, 208.57),
        "stage_left_end": (59.37, 0.0226, 210.64),
        "stage_right_start": (65.62, 0.0165, 208.44),
        "stage_right_end": (70.64, 0.0194, 206.88),
        "pre_stage_left_start": (65.27, 0.03, 208.88),
        "pre_stage_left_end": (59.38, 0.0433, 210.66),
        "pre_stage_right_start": (65.71, -0.007, 208.71),
        "pre_stage_right_end": (70.72, 0.0281, 207.15),
    },
     "hw_yello_belly_beta_": {
        "stage_left_start": (-25.26, -1.27, 176.42),
        "stage_left_end": (-30.31, -1.21, 176.37),
        "stage_right_start": (-24.78, -1.25, 176.41),
        "stage_right_end": (-19.77, -1.2, 176.47),
        "pre_stage_left_start": (-25.25, -1.23, 176.67),
        "pre_stage_left_end": (-30.3, -1.23, 176.64),
        "pre_stage_right_start": (-24.78, -1.24, 176.67),
        "pre_stage_right_end": (-19.77, -1.23, 176.78),
    },
    "bdl_londrina_drag": {
        "stage_left_start": (-357.09, -0.909, 171.7),
        "stage_left_end": (-359.2, -0.865, 165.52),
        "stage_right_start": (-356.99, -0.919, 171.98),
        "stage_right_end": (-354.89, -0.864, 178.13),
        "pre_stage_left_start":(-357.25, -0.912, 171.75),
        "pre_stage_left_end": (-359.36, -0.857, 165.57),
        "pre_stage_right_start": (-357.17, -0.926, 172.04),
        "pre_stage_right_end": (-355.06, -0.864, 178.18),
        },
    "do_cashdays_v3_": {
        "stage_left_start": (-1551.25, -25.3, 8351.151),
        "stage_left_end": (-1555.9, -25.31, 8349.87),
        "stage_right_start": (-1550.88, -25.3, 8351.26),
        "stage_right_end": (-1546.24, -25.31, 8352.54),
        "pre_stage_left_start":(-1551.33, -25.32, 8351.28),
        "pre_stage_left_end": (-1555.97, -25.23, 8350.03),
        "pre_stage_right_start": (-1550.92, -25.3, 8351.4),
        "pre_stage_right_end": (-1546.27, -25.31, 8352.68),
        },
    "do_cashdays_v2_": {
        "stage_left_start": (-1551.25, -25.3, 8351.151),
        "stage_left_end": (-1555.9, -25.31, 8349.87),
        "stage_right_start": (-1550.88, -25.3, 8351.26),
        "stage_right_end": (-1546.24, -25.31, 8352.54),
        "pre_stage_left_start":(-1551.33, -25.32, 8351.28),
        "pre_stage_left_end": (-1555.97, -25.23, 8350.03),
        "pre_stage_right_start": (-1550.92, -25.3, 8351.4),
        "pre_stage_right_end": (-1546.27, -25.31, 8352.68),
        },
           "bdl_race_valley_prep": {
        "stage_left_start": (-3.39, -0.652, -349.8),
        "stage_left_end": (3.51, -0.577, -349.45),
        "stage_right_start": (-6.34, -0.635, -349.91),
        "stage_right_end": (-12.66, -0.648, -350.2),
        "pre_stage_left_start":(-3.38, -0.624, -349.99),
        "pre_stage_left_end": (3.52, -0.624, -349.63),
        "pre_stage_right_start": (-6.33, -0.605, -350.16),
        "pre_stage_right_end": (-12.64, -0.639, -350.45),
        },
                   "bdl_race_valley_noprep": {
        "stage_left_start": (-40.59, -0.64, 170.14),
        "stage_left_end": (-33.09, -0.646, 170.51),
        "stage_right_start": (-31.39, -0.634, 170.59),
        "stage_right_end": (-24.3, -0.642, 170.93),
        "pre_stage_left_start":(-40.6, -0.637, 170.34),
        "pre_stage_left_end": (-33.1, -0.645, 170.71),
        "pre_stage_right_start": (-31.4, -0.633, 170.79),
        "pre_stage_right_end": (-24.31, -0.641, 171.14),
        },
}


def get_track_name():
    return "{}_{}".format(ac.getTrackName(0), ac.getTrackConfiguration(0))


def get_line_coordinates(track_name):
    return lines_coordinates.get(track_name, {
        "stage_left_start": (0.0, 0.0, 0.0),
        "stage_left_end": (0.0, 0.0, 0.0),
        "stage_right_start": (0.0, 0.0, 0.0),
        "stage_right_end": (0.0, 0.0, 0.0),
        "pre_stage_left_start": (0.0, 0.0, 0.0),
        "pre_stage_left_end": (0.0, 0.0, 0.0),
        "pre_stage_right_start": (0.0, 0.0, 0.0),
        "pre_stage_right_end": (0.0, 0.0, 0.0),
    })

def is_car_in_line(start, end):
    car_id = 0  
    world_position = ac.getCarState(car_id, acsys.CS.TyreContactPoint, acsys.WHEELS.FL)
    
    if world_position:
        px, py, pz = world_position
        
        x1, y1, z1 = start
        x2, y2, z2 = end
        
        line_vec = (x2 - x1, y2 - y1, z2 - z1)
        
        point_vec = (px - x1, py - y1, pz - z1)
        
        line_length_squared = sum(coord ** 2 for coord in line_vec)
        projection = sum(line_vec[i] * point_vec[i] for i in range(3)) / line_length_squared
        projection = max(0, min(1, projection))
        
        closest_point = (x1 + projection * line_vec[0], y1 + projection * line_vec[1], z1 + projection * line_vec[2])
        
        distance = math.sqrt(sum((closest_point[i] - world_position[i]) ** 2 for i in range(3)))
        
        return distance < 0.20
    
    return False

def is_car_in_stage_left():
    track_name = get_track_name()
    coords = get_line_coordinates(track_name)
    return is_car_in_line(coords["stage_left_start"], coords["stage_left_end"])

def is_car_in_stage_right():
    track_name = get_track_name()
    coords = get_line_coordinates(track_name)
    return is_car_in_line(coords["stage_right_start"], coords["stage_right_end"])

def is_car_in_pre_stage_left():
    track_name = get_track_name()
    coords = get_line_coordinates(track_name)
    return is_car_in_line(coords["pre_stage_left_start"], coords["pre_stage_left_end"])

def is_car_in_pre_stage_right():
    track_name = get_track_name()
    coords = get_line_coordinates(track_name)
    return is_car_in_line(coords["pre_stage_right_start"], coords["pre_stage_right_end"])

def add_log_message(message):
    global log_messages
    log_messages.append(message)
    if len(log_messages) > 5:  
        log_messages.pop(0)
    ac.setText(log_label, "\n".join(log_messages))

prev_stage_left = False
prev_stage_right = False
prev_pre_stage_left = False
prev_pre_stage_right = False

def on_stage_left_change(new_value):
    global button1_state
    if new_value:
        add_log_message("Entrou Stage Left On")
        button1_state = True
        update_button1_state()
    else:
        add_log_message("Entrou Stage Left Off")
        button1_state = False
        update_button1_state()
               
def on_stage_right_change(new_value):
    global button2_state
    if new_value:
        add_log_message("Entrou no Stage Right")
        button2_state = True
        update_button2_state()
    else:
        add_log_message("Saiu do Stage Right")
        button2_state = False
        update_button2_state()

def on_pre_stage_left_change(new_value):
    global button3_state
    if new_value:
        add_log_message("Entrou no Pre-Stage Left")
        button3_state = True
        update_button3_state()
    else:
        add_log_message("Saiu do Pre-Stage Left")
        button3_state = False
        update_button3_state()

def on_pre_stage_right_change(new_value):
    global button4_state
    if new_value:
        add_log_message("Entrou no Pre-Stage Right")
        button4_state = True
        update_button4_state()
    else:
        add_log_message("Saiu do Pre-Stage Right")
        button4_state = False
        update_button4_state()

def onFormRender(delta_t):
    global prev_stage_left, prev_stage_right, prev_pre_stage_left, prev_pre_stage_right
    
    update_pass_counter()

    stage_left = is_car_in_stage_left()
    stage_right = is_car_in_stage_right()
    pre_stage_left = is_car_in_pre_stage_left()
    pre_stage_right = is_car_in_pre_stage_right()

   
    ac.setText(label_stage_left, "Stage Left: {}".format("Yes" if stage_left else "No"))
    ac.setText(label_stage_right, "Stage Right: {}".format("Yes" if stage_right else "No"))
    ac.setText(label_pre_stage_left, "Pre-Stage Left: {}".format("Yes" if pre_stage_left else "No"))
    ac.setText(label_pre_stage_right, "Pre-Stage Right: {}".format("Yes" if pre_stage_right else "No"))

    
    if stage_left != prev_stage_left:
        on_stage_left_change(stage_left)
        prev_stage_left = stage_left

    if stage_right != prev_stage_right:
        on_stage_right_change(stage_right)
        prev_stage_right = stage_right

    if pre_stage_left != prev_pre_stage_left:
        on_pre_stage_left_change(pre_stage_left)
        prev_pre_stage_left = pre_stage_left

    if pre_stage_right != prev_pre_stage_right:
        on_pre_stage_right_change(pre_stage_right)
        prev_pre_stage_right = pre_stage_right


    


def acMain(ac_version):
    global app_window,log_label,track_label, pos_label, prestage_left, prestage_right, stage_left, stage_right, extra_button5, extra_button6, extra_button7, extra_button8, extra_button9, extra_button10, timer_label
    global extra_button11,extra_button12,extra_button12,extra_button13,extra_button14,extra_button15,extra_button16,extra_button17,extra_button18
    global label_stage_left,label_stage_right,label_pre_stage_left,label_pre_stage_right,label_pass_counter,log_messages,reaction_time_label,best_reaction_time_label
    

    threading.Thread(target=process_send_queue, daemon=True).start()

    app_window = ac.newApp("BDL RACE CONTROL FINAL V3")
    ac.setSize(app_window, 220, 420)
    ac.setTitle(app_window, "BDL RACE CONTROL FINAL V3")
    ac.addRenderCallback(app_window, onFormRender)
    track_label = ac.addLabel(app_window,track_name)
    ac.setPosition(track_label, 10, 390)
    ac.setSize(track_label, 230, 20)
    ac.setFontSize(track_label, 20)
    log_label = ac.addLabel(app_window, "Log")
    ac.setPosition(log_label, 20, 500)
    log_messages = []
    ac.setVisible(log_label,0)
    label_stage_left = ac.addLabel(app_window, "Stage Left: --")
    ac.setPosition(label_stage_left, 20, 390) 
    ac.setVisible(label_stage_left,0)
    label_stage_right = ac.addLabel(app_window, "Stage Right: --")
    ac.setPosition(label_stage_right, 20, 420)  
    ac.setVisible(label_stage_right,0)
    label_pre_stage_left = ac.addLabel(app_window, "Pre-Stage Left: --")
    ac.setPosition(label_pre_stage_left, 20, 450) 
    ac.setVisible(label_pre_stage_left,0)
    label_pre_stage_right = ac.addLabel(app_window, "Pre-Stage Right: --")
    ac.setPosition(label_pre_stage_right, 20, 480)  
    ac.setVisible(label_pre_stage_right,0)
    label_pass_counter = ac.addLabel(app_window, "Pass Count: 0")
    ac.setPosition(label_pass_counter, 20, 680)
    ac.setVisible(label_pass_counter,0)
    pos_label = ac.addLabel(app_window, "Posição: ")
    ac.setPosition(pos_label, 20, 700)
    ac.setFontSize(pos_label, 14)
    ac.setVisible(pos_label,0)
    timer_label = ac.addLabel(app_window, "00:00")
    ac.setPosition(timer_label, 120, 30)  
    ac.setSize(timer_label, 80, 40)  
    ac.setFontSize(timer_label, 24)
    ac.setCustomFont(timer_label, "Arial", 0, 1)
    ac.setFontAlignment(timer_label, "center")
    extra_button17 = ac.addLabel(app_window, "OFF")
    ac.setPosition(extra_button17, 110, 80)  
    ac.setSize(extra_button17, 110, 40) 
    ac.setFontSize(extra_button17, 20)
    ac.setCustomFont(extra_button17, "Arial", 0, 1)
    ac.setFontAlignment(extra_button17, "center")
    ac.addOnClickedListener(extra_button17, toggle_button17_clicked)
    prestage_left = ac.addLabel(app_window, "OFF")
    ac.setPosition(prestage_left, 10, 30)  
    ac.setSize(prestage_left, 40, 40)  
    ac.setFontSize(prestage_left, 14)
    ac.setCustomFont(prestage_left, "Arial", 0, 1)
    ac.setFontAlignment(prestage_left, "center")
    ac.addOnClickedListener(prestage_left, toggle_button3_clicked)
    prestage_right = ac.addLabel(app_window, "OFF")
    ac.setPosition(prestage_right, 60, 30)  
    ac.setSize(prestage_right, 40, 40)  
    ac.setFontSize(prestage_right, 14)
    ac.setCustomFont(prestage_right, "Arial", 0, 1)
    ac.setFontAlignment(prestage_right, "center")
    ac.addOnClickedListener(prestage_right, toggle_button4_clicked)
    stage_left = ac.addLabel(app_window, "OFF")
    ac.setPosition(stage_left, 10, 80)  
    ac.setSize(stage_left, 40, 40)  
    ac.setFontSize(stage_left, 14)
    ac.setCustomFont(stage_left, "Arial", 0, 1)
    ac.setFontAlignment(stage_left, "center")
    ac.addOnClickedListener(stage_left, toggle_button1_clicked)
    stage_right = ac.addLabel(app_window, "OFF")
    ac.setPosition(stage_right, 60, 80) 
    ac.setSize(stage_right, 40, 40)  
    ac.setFontSize(stage_right, 14)
    ac.setCustomFont(stage_right, "Arial", 0, 1)
    ac.setFontAlignment(stage_right, "center")
    ac.addOnClickedListener(stage_right, toggle_button2_clicked)
    extra_button5 = ac.addLabel(app_window, "OFF")
    ac.setPosition(extra_button5, 10, 130)  
    ac.setSize(extra_button5, 40, 40)  
    ac.setFontSize(extra_button5, 14)
    ac.setCustomFont(extra_button5, "Arial", 0, 1)
    ac.setFontAlignment(extra_button5, "center")
    ac.addOnClickedListener(extra_button5, toggle_button5_clicked)
    extra_button6 = ac.addLabel(app_window, "OFF")
    ac.setPosition(extra_button6, 10, 170)  
    ac.setSize(extra_button6, 40, 40)  
    ac.setFontSize(extra_button6, 14)
    ac.setCustomFont(extra_button6, "Arial", 0, 1)
    ac.setFontAlignment(extra_button6, "center")
    ac.addOnClickedListener(extra_button6, toggle_button6_clicked)
    extra_button7 = ac.addLabel(app_window, "OFF")
    ac.setPosition(extra_button7, 10, 210)  
    ac.setSize(extra_button7, 40, 40) 
    ac.setFontSize(extra_button7, 14)
    ac.setCustomFont(extra_button7, "Arial", 0, 1)
    ac.setFontAlignment(extra_button7, "center")
    ac.addOnClickedListener(extra_button7, toggle_button7_clicked)
    extra_button8 = ac.addLabel(app_window, "OFF")
    ac.setPosition(extra_button8, 10, 250)  
    ac.setSize(extra_button8, 40, 40)  
    ac.setFontSize(extra_button8, 14)
    ac.setCustomFont(extra_button8, "Arial", 0, 1)
    ac.setFontAlignment(extra_button8, "center")
    ac.addOnClickedListener(extra_button8, toggle_button8_clicked)
    extra_button9 = ac.addLabel(app_window, "OFF")
    ac.setPosition(extra_button9, 10, 290)  
    ac.setSize(extra_button9, 40, 40) 
    ac.setFontSize(extra_button9, 14)
    ac.setCustomFont(extra_button9, "Arial", 0, 1)
    ac.setFontAlignment(extra_button9, "center")
    ac.addOnClickedListener(extra_button9, toggle_button9_clicked)
    extra_button10 = ac.addLabel(app_window, "OFF")
    ac.setPosition(extra_button10, 10, 340)  
    ac.setSize(extra_button10, 40, 40)  
    ac.setFontSize(extra_button10, 14)
    ac.setCustomFont(extra_button10, "Arial", 0, 1)
    ac.setFontAlignment(extra_button10, "center")
    ac.addOnClickedListener(extra_button10, toggle_button10_clicked)
    extra_button11 = ac.addLabel(app_window, "OFF")
    ac.setPosition(extra_button11, 60, 130)  
    ac.setSize(extra_button11, 40, 40)  
    ac.setFontSize(extra_button11, 14)
    ac.setCustomFont(extra_button11, "Arial", 0, 1)
    ac.setFontAlignment(extra_button11, "center")
    ac.addOnClickedListener(extra_button11, toggle_button11_clicked)
    extra_button12 = ac.addLabel(app_window, "OFF")
    ac.setPosition(extra_button12, 60, 170)  
    ac.setSize(extra_button12, 40, 40)  
    ac.setFontSize(extra_button12, 14)
    ac.setCustomFont(extra_button12, "Arial", 0, 1)
    ac.setFontAlignment(extra_button12, "center")
    ac.addOnClickedListener(extra_button12, toggle_button12_clicked)
    extra_button13 = ac.addLabel(app_window, "OFF")
    ac.setPosition(extra_button13, 60, 210)  
    ac.setSize(extra_button13, 40, 40)  
    ac.setFontSize(extra_button13, 14)
    ac.setCustomFont(extra_button13, "Arial", 0, 1)
    ac.setFontAlignment(extra_button13, "center")
    ac.addOnClickedListener(extra_button13, toggle_button13_clicked)
    extra_button14 = ac.addLabel(app_window, "OFF")
    ac.setPosition(extra_button14, 60, 250)  
    ac.setSize(extra_button14, 40, 40)  
    ac.setFontSize(extra_button14, 14)
    ac.setCustomFont(extra_button14, "Arial", 0, 1)
    ac.setFontAlignment(extra_button14, "center")
    ac.addOnClickedListener(extra_button14, toggle_button14_clicked)
    extra_button15 = ac.addLabel(app_window, "OFF")
    ac.setPosition(extra_button15, 60, 290)  
    ac.setSize(extra_button15, 40, 40)  
    ac.setFontSize(extra_button15, 14)
    ac.setCustomFont(extra_button15, "Arial", 0, 1)
    ac.setFontAlignment(extra_button15, "center")
    ac.addOnClickedListener(extra_button15, toggle_button15_clicked)
    extra_button16 = ac.addLabel(app_window, "OFF")
    ac.setPosition(extra_button16, 60, 340) 
    ac.setSize(extra_button16, 40, 40) 
    ac.setFontSize(extra_button16, 14)
    ac.setCustomFont(extra_button16, "Arial", 0, 1)
    ac.setFontAlignment(extra_button16, "center")
    ac.addOnClickedListener(extra_button16, toggle_button16_clicked)

    reaction_time_label = ac.addLabel(app_window, "Last")
    ac.setPosition(reaction_time_label, 105, 150)
    ac.setFontSize(reaction_time_label, 17)
    ac.setFontColor(reaction_time_label, 0.8, 0.8, 0.8, 1)
    ac.setBackgroundOpacity(reaction_time_label, 0.5)
    ac.setSize(reaction_time_label, 55, 26)
    ac.setFontAlignment(reaction_time_label, "center")
    ac.setVisible(reaction_time_label,1)
        

    best_reaction_time_label = ac.addLabel(app_window, "Best")
    ac.setPosition(best_reaction_time_label, 165, 150)
    ac.setFontSize(best_reaction_time_label, 17)
    ac.setFontColor(best_reaction_time_label, 0, 0.8,0, 1)
    ac.setBackgroundColor(best_reaction_time_label, 0, 0, 0)  
    ac.setBackgroundOpacity(best_reaction_time_label, 0.5)
    ac.setSize(best_reaction_time_label, 55, 25)
    ac.setFontAlignment(best_reaction_time_label, "center")
    ac.setVisible(best_reaction_time_label,1)
        
    update_button1_state1()
    update_button2_state1()
    update_button3_state1()
    update_button4_state1()
    update_button5_state1()
    update_button6_state1()
    update_button7_state1()
    update_button8_state1()
    update_button9_state1()
    update_button10_state1() 
    update_button11_state1()
    update_button12_state1()
    update_button13_state1()
    update_button14_state1()
    update_button15_state1()
    update_button16_state1()
    update_button17_state1()

    global start_time
    start_time = time.time()

    ac.addOnChatMessageListener(app_window, onChatMessage)
    return app_window
    return "Car Info"


def toggle_button1_clicked(*args):
    global button1_state,button1_enabled,buttons_enabled,button_last_click
     # Verificar se o botão está habilitado (para evitar clique múltiplo)
    if  buttons_enabled and button1_enabled and time.time() - button_last_click > 0.9:        # Alternar o estado do botão
        button1_state = not button1_state
        update_button1_state()
        # Registrar o último clique e desabilitar o botão
        button_last_click = time.time()
        disable_all_buttons()
        

def toggle_button2_clicked(*args):
    global button2_state, button2_enabled,buttons_enabled,button_last_click

    if  buttons_enabled and button2_enabled and time.time() - button_last_click > 0.9:
        button2_state = not button2_state
        update_button2_state()
        button_last_click = time.time()
        disable_all_buttons()


def toggle_button3_clicked(*args):
    global button3_state, button3_enabled,button_last_click,buttons_enabled

    if  buttons_enabled and button3_enabled and time.time() - button_last_click > 0.9:
        button3_state = not button3_state
        update_button3_state()
        button_last_click = time.time()
        disable_all_buttons()

def toggle_button4_clicked(*args):
    global button4_state, button_last_click,buttons_enabled, button4_enabled

    if  buttons_enabled and button4_enabled and time.time() - button_last_click > 0.9:
        button4_state = not button4_state
        update_button4_state()
        button_last_click = time.time()
        disable_all_buttons()


def toggle_button5_clicked(*args):
    global button5_state, button_last_click,buttons_enabled, button5_enabled

    if  buttons_enabled and button5_enabled and time.time() - button_last_click > 0.9:
        button5_state = not button5_state
        update_button5_state()
        button_last_click = time.time()
        disable_all_buttons()


def toggle_button6_clicked(*args):
    global button6_state, button_last_click,buttons_enabled, button6_enabled

    if  buttons_enabled and button6_enabled and time.time() - button_last_click > 0.9:
        button6_state = not button6_state
        update_button6_state()
        button_last_click = time.time()
        disable_all_buttons()


def toggle_button7_clicked(*args):
    global button7_state, button_last_click,buttons_enabled, button7_enabled

    if  buttons_enabled and button7_enabled and time.time() - button_last_click > 0.9:
        button7_state = not button7_state
        update_button7_state()
        button_last_click = time.time()
        disable_all_buttons()


def toggle_button8_clicked(*args):
    global button8_state, button_last_click,buttons_enabled, button8_enabled

    if  buttons_enabled and button8_enabled and time.time() - button_last_click > 0.9:
        button8_state = not button8_state
        update_button8_state()
        button_last_click = time.time()
        disable_all_buttons()


def toggle_button9_clicked(*args):
    global button9_state, button_last_click,buttons_enabled, button9_enabled

    if  buttons_enabled and button9_enabled and time.time() - button_last_click > 0.9:
        button9_state = not button9_state
        update_button9_state()
        button_last_click = time.time()
        disable_all_buttons()

def toggle_button10_clicked(*args):
    global button10_state, button_last_click,buttons_enabled, button10_enabled
    global timer_running,timer_start_time,pin_on,is_left,is_right,pin_on_fire

    if  buttons_enabled and button10_enabled and time.time() - button_last_click > 0.95:
        button10_state = not button10_state
        update_button10_state()
        button_last_click = time.time()
        disable_all_buttons()
        pin_on=True
        pin_on_fire=True
        is_left=True
        is_right=False

        if button10_state:
            Turn_Off_Before_Pin()
            timer_running = True
            timer_start_time = time.time()
        else:
            timer_running = False
    
                

def toggle_button11_clicked(*args):
    global button11_state, button_last_click,buttons_enabled, button11_enabled

    if  buttons_enabled and button11_enabled and time.time() - button_last_click > 0.9:
        button11_state = not button11_state
        update_button11_state()
        button_last_click = time.time()
        disable_all_buttons()


def toggle_button12_clicked(*args):
    global button12_state, button_last_click,buttons_enabled, button12_enabled

    if  buttons_enabled and button12_enabled and time.time() - button_last_click > 0.9:
        button12_state = not button12_state
        update_button12_state()
        button_last_click = time.time()
        disable_all_buttons()


def toggle_button13_clicked(*args):
    global button13_state, button_last_click,buttons_enabled, button13_enabled

    if  buttons_enabled and button13_enabled and time.time() - button_last_click > 0.9:
        button13_state = not button13_state
        update_button13_state()
        button_last_click = time.time()
        disable_all_buttons()


def toggle_button14_clicked(*args):
    global button14_state, button_last_click,buttons_enabled, button14_enabled

    if  buttons_enabled and button14_enabled and time.time() - button_last_click > 0.9:
        button14_state = not button14_state
        update_button14_state()
        button_last_click = time.time()
        disable_all_buttons()


def toggle_button15_clicked(*args):
    global button15_state, button_last_click,buttons_enabled, button15_enabled

    if  buttons_enabled and button15_enabled and time.time() - button_last_click > 0.9:
        button15_state = not button15_state
        update_button15_state()
        button_last_click = time.time()
        disable_all_buttons()

def toggle_button16_clicked(*args):
    global button16_state, button_last_click,buttons_enabled, button16_enabled
    global timer_running,timer_start_time,pin_on,is_left,is_right, pin_on_fire

    if  buttons_enabled and button16_enabled and time.time() - button_last_click > 0.95:
        button16_state = not button16_state
        update_button16_state()
        button_last_click = time.time()
        disable_all_buttons()
        pin_on=True
        pin_on_fire=True
        is_left=False
        is_right=True

        if button16_state:
            Turn_Off_Before_Pin()
            timer_running = True
            timer_start_time = time.time()
        else:
            timer_running = False

def toggle_button17_clicked(*args):
    global button17_state, button_last_click,buttons_enabled, button17_enabled
    global timer_running,timer_start_time,pin_on,is_left,is_right,pin_on_fire

    if  buttons_enabled and button17_enabled and time.time() - button_last_click > 0.95:
        button17_state = not button17_state
        update_button17_state()
        button_last_click = time.time()
        disable_all_buttons()
        pin_on=True
        pin_on_fire=True
        is_left=True
        is_right=True

        if button17_state:
            Turn_Off_Before_Pin()
            timer_running = True
            timer_start_time = time.time()
        else:
            timer_running = False

def Turn_Off_All_Locally():
    global button1_state , button2_state , button3_state , button4_state
    global button5_state,button6_state,button7_state,button8_state,button9_state ,button10_state
    global button11_state,button12_state,button13_state,button14_state,button15_state,button16_state,button17_state
    button1_state = False
    update_button1_state1() 
    button2_state = False
    update_button2_state1() 
    button3_state = False
    update_button3_state1() 
    button4_state = False
    update_button4_state1()
    button8_state = False
    update_button8_state1() 
    button9_state = False
    update_button9_state1()
    button5_state = False
    update_button5_state1()
    button6_state = False
    update_button6_state1()
    button7_state = False
    update_button7_state1()
    button11_state = False
    update_button11_state1()
    button12_state = False
    update_button12_state1()
    button13_state = False
    update_button13_state1()
    button14_state = False
    update_button14_state1()
    button15_state = False
    update_button15_state1()
    button10_state=False
    update_button10_state1()
    button16_state = False  
    update_button16_state1()
    button17_state = False  
    update_button17_state1()

def Turn_Off_Before_Pin():
    global button1_state , button2_state , button3_state , button4_state
    global button5_state,button6_state,button7_state,button8_state,button9_state ,button10_state
    global button11_state,button12_state,button13_state,button14_state,button15_state,button16_state,button17_state
   
    button1_state = False
    update_button1_state1() 
    button2_state = False
    update_button2_state1() 
    button3_state = False
    update_button3_state1() 
    button4_state = False
    update_button4_state1()
    button8_state = False
    update_button8_state1() 
    button9_state = False
    update_button9_state1()
    button5_state = False
    update_button5_state1()
    button6_state = False
    update_button6_state1()
    button7_state = False
    update_button7_state1()
    button11_state = False
    update_button11_state1()
    button12_state = False
    update_button12_state1()
    button13_state = False
    update_button13_state1()
    button14_state = False
    update_button14_state1()
    button15_state = False
    update_button15_state1()
 

previous_button1_state = False

def update_button1_state():
    global button1_state, previous_button1_state

    background_color = (1, 1, 0)
    opacity = 1.0 if button1_state else 0.3
    text = "ON" if button1_state else "OFF"

    ac.setText(stage_left, text)
    ac.setFontColor(stage_left, 0, 0, 0, 1)
    ac.setBackgroundColor(stage_left, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(stage_left, opacity)

    if button1_state != previous_button1_state:
        if button1_state:
            enviar_mensagem_chat("StageLeftOn")
            turn_emissive("StageLeft", Yellow)
        else:
            enviar_mensagem_chat("StageLeftOff")
            turn_emissive("StageLeft", Off)

        previous_button1_state = button1_state

def update_button1_state1():
    global button1_state, previous_button1_state

    background_color = (1, 1, 0)
    opacity = 1.0 if button1_state else 0.3
    text = "ON" if button1_state else "OFF"

    ac.setText(stage_left, text)
    ac.setFontColor(stage_left, 0, 0, 0, 1)
    ac.setBackgroundColor(stage_left, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(stage_left, opacity)

    if button1_state != previous_button1_state:
        if button1_state:
            #enviar_mensagem_chat("StageLeftOn")
            turn_emissive("StageLeft", Yellow)
        else:
            #enviar_mensagem_chat("StageLeftOff")
            turn_emissive("StageLeft", Off)
            


        previous_button1_state = button1_state

previous_button2_state = False

def update_button2_state():
    global button2_state, previous_button2_state

    background_color = (1, 1, 0)
    opacity = 1.0 if button2_state else 0.3
    text = "ON" if button2_state else "OFF"

    ac.setText(stage_right, text)
    ac.setFontColor(stage_right, 0, 0, 0, 1)
    ac.setBackgroundColor(stage_right, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(stage_right, opacity)

    if button2_state != previous_button2_state:
        if button2_state:
            enviar_mensagem_chat("StageRightOn")
            turn_emissive("StageRight", Yellow)
        else:
            enviar_mensagem_chat("StageRightOff")
            turn_emissive("StageRight", Off)

        previous_button2_state = button2_state

def update_button2_state1():
    global button2_state, previous_button2_state

    background_color = (1, 1, 0)
    opacity = 1.0 if button2_state else 0.3
    text = "ON" if button2_state else "OFF"

    ac.setText(stage_right, text)
    ac.setFontColor(stage_right, 0, 0, 0, 1)
    ac.setBackgroundColor(stage_right, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(stage_right, opacity)

    if button2_state != previous_button2_state:
        if button2_state:
            #enviar_mensagem_chat("StageRightOn")
            turn_emissive("StageRight", Yellow)
        else:
            #enviar_mensagem_chat("StageRightOff")
            turn_emissive("StageRight", Off)

        previous_button2_state = button2_state

previous_button3_state = False

def update_button3_state():
    global button3_state, previous_button3_state

    background_color = (1, 1, 0)
    opacity = 1.0 if button3_state else 0.3
    text = "ON" if button3_state else "OFF"

    ac.setText(prestage_left, text)
    ac.setFontColor(prestage_left, 0, 0, 0, 1)
    ac.setBackgroundColor(prestage_left, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(prestage_left, opacity)

    if button3_state != previous_button3_state:
        if button3_state:
            enviar_mensagem_chat("PreStageLeft_On")
            turn_emissive("PreStageLeft", Yellow)
        else:
            enviar_mensagem_chat("PreStageLeft_Off")
            turn_emissive("PreStageLeft", Off)

        previous_button3_state = button3_state

def update_button3_state1():
    global button3_state, previous_button3_state

    background_color = (1, 1, 0)
    opacity = 1.0 if button3_state else 0.3
    text = "ON" if button3_state else "OFF"

    ac.setText(prestage_left, text)
    ac.setFontColor(prestage_left, 0, 0, 0, 1)
    ac.setBackgroundColor(prestage_left, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(prestage_left, opacity)

    if button3_state != previous_button3_state:
        if button3_state:
            #enviar_mensagem_chat("PreStageLeft_On")
            turn_emissive("PreStageLeft", Yellow)
        else:
            #enviar_mensagem_chat("PreStageLeft_Off")
            turn_emissive("PreStageLeft", Off)

        previous_button3_state = button3_state

previous_button4_state = False

def update_button4_state():
    global button4_state, previous_button4_state

    background_color = (1, 1, 0)
    opacity = 1.0 if button4_state else 0.3
    text = "ON" if button4_state else "OFF"

    ac.setText(prestage_right, text)
    ac.setFontColor(prestage_right, 0, 0, 0, 1)
    ac.setBackgroundColor(prestage_right, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(prestage_right, opacity)

    if button4_state != previous_button4_state:
        if button4_state:
            enviar_mensagem_chat("PreStageRight_On")
            turn_emissive("PreStageRight", Yellow)
        else:
            enviar_mensagem_chat("PreStageRight_Off")
            turn_emissive("PreStageRight", Off)

        previous_button4_state = button4_state

def update_button4_state1():
    global button4_state, previous_button4_state

    background_color = (1, 1, 0)
    opacity = 1.0 if button4_state else 0.3
    text = "ON" if button4_state else "OFF"

    ac.setText(prestage_right, text)
    ac.setFontColor(prestage_right, 0, 0, 0, 1)
    ac.setBackgroundColor(prestage_right, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(prestage_right, opacity)

    if button4_state != previous_button4_state:
        if button4_state:
            #enviar_mensagem_chat("PreStageRight_On")
            turn_emissive("PreStageRight", Yellow)
        else:
            #enviar_mensagem_chat("PreStageRight_Off")
            turn_emissive("PreStageRight", Off)

        previous_button4_state = button4_state

previous_button5_state = False

def update_button5_state():
    global button5_state, previous_button5_state

    background_color = (1, 1, 0)  
    opacity = 1.0 if button5_state else 0.3
    text = "ON" if button5_state else "OFF"
    
    ac.setText(extra_button5, text)
    ac.setFontColor(extra_button5, 0, 0, 0, 1) 
    ac.setBackgroundColor(extra_button5, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button5, opacity)

    if button5_state != previous_button5_state:
        if button5_state:
            enviar_mensagem_chat("Yellow_1_On")
            turn_emissive("Yellow_1", Yellow)
        else:
            enviar_mensagem_chat("Yellow_1_Off")
            turn_emissive("Yellow_1", Off)

        previous_button5_state = button5_state

def update_button5_state1():
    global button5_state, previous_button5_state,button1_enabled

    background_color = (1, 1, 0)  
    opacity = 1.0 if button5_state else 0.3
    text = "ON" if button5_state else "OFF"
    
    ac.setText(extra_button5, text)
    ac.setFontColor(extra_button5, 0, 0, 0, 1) 
    ac.setBackgroundColor(extra_button5, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button5, opacity)

    if button5_state != previous_button5_state:
        if button5_state:
            #enviar_mensagem_chat("Yellow_1_On")
            turn_emissive("Yellow_1", Yellow)
        else:
            #enviar_mensagem_chat("Yellow_1_Off")
            turn_emissive("Yellow_1", Off)

        previous_button5_state = button5_state

previous_button6_state = False

def update_button6_state():
    global button6_state, previous_button6_state

    background_color = (1, 1, 0)  
    opacity = 1.0 if button6_state else 0.3
    text = "ON" if button6_state else "OFF"
    
    ac.setText(extra_button6, text)
    ac.setFontColor(extra_button6, 0, 0, 0, 1)  
    ac.setBackgroundColor(extra_button6, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button6, opacity)

    if button6_state != previous_button6_state:
        if button6_state:
            enviar_mensagem_chat("Yellow_2_On")
            turn_emissive("Yellow_2", Yellow)
        else:
            enviar_mensagem_chat("Yellow_2_Off")
            turn_emissive("Yellow_2", Off)

        previous_button6_state = button6_state

def update_button6_state1():
    global button6_state, previous_button6_state

    background_color = (1, 1, 0)  
    opacity = 1.0 if button6_state else 0.3
    text = "ON" if button6_state else "OFF"
    
    ac.setText(extra_button6, text)
    ac.setFontColor(extra_button6, 0, 0, 0, 1)  
    ac.setBackgroundColor(extra_button6, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button6, opacity)

    if button6_state != previous_button6_state:
        if button6_state:
            #enviar_mensagem_chat("Yellow_2_On")
            turn_emissive("Yellow_2", Yellow)
        else:
            #enviar_mensagem_chat("Yellow_2_Off")
            turn_emissive("Yellow_2", Off)

        previous_button6_state = button6_state


previous_button7_state = False

def update_button7_state():
    global button7_state, previous_button7_state

    background_color = (1, 1, 0)  
    opacity = 1.0 if button7_state else 0.3
    text = "ON" if button7_state else "OFF"

    ac.setText(extra_button7, text)
    ac.setFontColor(extra_button7, 0, 0, 0, 1)  
    ac.setBackgroundColor(extra_button7, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button7, opacity)

    if button7_state != previous_button7_state:
        if button7_state:
            enviar_mensagem_chat("Yellow_3_On")
            turn_emissive("Yellow_3", Yellow)
        else:
            enviar_mensagem_chat("Yellow_3_Off")
            turn_emissive("Yellow_3", Off)

        previous_button7_state = button7_state

def update_button7_state1():
    global button7_state, previous_button7_state

    background_color = (1, 1, 0)  
    opacity = 1.0 if button7_state else 0.3
    text = "ON" if button7_state else "OFF"

    ac.setText(extra_button7, text)
    ac.setFontColor(extra_button7, 0, 0, 0, 1)  
    ac.setBackgroundColor(extra_button7, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button7, opacity)

    if button7_state != previous_button7_state:
        if button7_state:
            #enviar_mensagem_chat("Yellow_3_On")
            turn_emissive("Yellow_3", Yellow)
        else:
            #enviar_mensagem_chat("Yellow_3_Off")
            turn_emissive("Yellow_3", Off)

        previous_button7_state = button7_state

previous_button8_state = False

def update_button8_state():
    global button8_state, previous_button8_state

    background_color = (0, 1, 0)  
    opacity = 1.0 if button8_state else 0.3
    text = "ON" if button8_state else "OFF"

    ac.setText(extra_button8, text)
    ac.setFontColor(extra_button8, 0, 0, 0, 1)  
    ac.setBackgroundColor(extra_button8, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button8, opacity)

    if button8_state != previous_button8_state:
        if button8_state:
            enviar_mensagem_chat("Green_L_On")
            turn_emissive("GreenLeft", Green)
        else:
            enviar_mensagem_chat("Green_L_Off")
            turn_emissive("GreenLeft", Off)

        previous_button8_state = button8_state

def update_button8_state1():
    global button8_state, previous_button8_state

    background_color = (0, 1, 0)  
    opacity = 1.0 if button8_state else 0.3
    text = "ON" if button8_state else "OFF"

    ac.setText(extra_button8, text)
    ac.setFontColor(extra_button8, 0, 0, 0, 1)  
    ac.setBackgroundColor(extra_button8, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button8, opacity)

    if button8_state != previous_button8_state:
        if button8_state:
            #enviar_mensagem_chat("Green_L_On")
            turn_emissive("GreenLeft", Green)
        else:
            #enviar_mensagem_chat("Green_L_Off")
            turn_emissive("GreenLeft", Off)

        previous_button8_state = button8_state

previous_button9_state = False

def update_button9_state():
    global button9_state, previous_button9_state

    background_color = (1, 0, 0)  
    opacity = 1.0 if button9_state else 0.3
    text = "ON" if button9_state else "OFF"

    ac.setText(extra_button9, text)
    ac.setFontColor(extra_button9, 0, 0, 0, 1)  
    ac.setBackgroundColor(extra_button9, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button9, opacity)

    if button9_state != previous_button9_state:
        if button9_state:
            enviar_mensagem_chat("Red_L_On")
            turn_emissive("RedLeft", Red)
        else:
            enviar_mensagem_chat("Red_L_Off")
            turn_emissive("RedLeft", Off)

        previous_button9_state = button9_state

def update_button9_state1():
    global button9_state, previous_button9_state

    background_color = (1, 0, 0)  
    opacity = 1.0 if button9_state else 0.3
    text = "ON" if button9_state else "OFF"

    ac.setText(extra_button9, text)
    ac.setFontColor(extra_button9, 0, 0, 0, 1)  
    ac.setBackgroundColor(extra_button9, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button9, opacity)

    if button9_state != previous_button9_state:
        if button9_state:
            #enviar_mensagem_chat("Red_L_On")
            turn_emissive("RedLeft", Red)
        else:
            #enviar_mensagem_chat("Red_L_Off")
            turn_emissive("RedLeft", Off)

        previous_button9_state = button9_state

previous_button10_state = False

def update_button10_state():
    global button10_state, previous_button10_state

    background_color = (0, 0, 1) if button10_state else (0.5, 0.5, 0.5)  
    opacity = 1.0 if button10_state else 0.3
    text = "ON" if button10_state else "OFF"

    ac.setText(extra_button10, text)
    ac.setFontColor(extra_button10, 1, 1, 1, 1) 
    ac.setBackgroundColor(extra_button10, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button10, opacity)

    if button10_state != previous_button10_state:
        if button10_state:
            enviar_mensagem_chat("Pin_Left_On")
        else:
            enviar_mensagem_chat("Pin_Left_Off")

        previous_button10_state = button10_state

def update_button10_state1():
    global button10_state, previous_button10_state

    background_color = (0, 0, 1) if button10_state else (0.5, 0.5, 0.5)  
    opacity = 1.0 if button10_state else 0.3
    text = "ON" if button10_state else "OFF"

    ac.setText(extra_button10, text)
    ac.setFontColor(extra_button10, 1, 1, 1, 1) 
    ac.setBackgroundColor(extra_button10, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button10, opacity)

    if button10_state != previous_button10_state:
        previous_button10_state = button10_state

previous_button11_state = False

def update_button11_state():
    global button11_state, previous_button11_state
        
    background_color = (1, 1, 0)  
    opacity = 1.0 if button11_state else 0.3
    text = "ON" if button11_state else "OFF"

    ac.setText(extra_button11, text)
    ac.setFontColor(extra_button11, 0, 0, 0, 1)  
    ac.setBackgroundColor(extra_button11, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button11, opacity)
        
    if button11_state != previous_button11_state:
        if button11_state:
            enviar_mensagem_chat("Yellow_4_On")
            turn_emissive("Yellow_4", Yellow)
        else:
            enviar_mensagem_chat("Yellow_4_Off")
            turn_emissive("Yellow_4", Off)

        previous_button11_state = button11_state

def update_button11_state1():
    global button11_state, previous_button11_state
        
    background_color = (1, 1, 0)  
    opacity = 1.0 if button11_state else 0.3
    text = "ON" if button11_state else "OFF"

    ac.setText(extra_button11, text)
    ac.setFontColor(extra_button11, 0, 0, 0, 1)  
    ac.setBackgroundColor(extra_button11, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button11, opacity)
        
    if button11_state != previous_button11_state:
        if button11_state:
            #enviar_mensagem_chat("Yellow_4_On")
            turn_emissive("Yellow_4", Yellow)
        else:
            #enviar_mensagem_chat("Yellow_4_Off")
            turn_emissive("Yellow_4", Off)

        previous_button11_state = button11_state

previous_button12_state = False

def update_button12_state():
    global button12_state, previous_button12_state

    background_color = (1, 1, 0)  
    opacity = 1.0 if button12_state else 0.3
    text = "ON" if button12_state else "OFF"

    ac.setText(extra_button12, text)
    ac.setFontColor(extra_button12, 0, 0, 0, 1)  
    ac.setBackgroundColor(extra_button12, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button12, opacity)

    if button12_state != previous_button12_state:
        if button12_state:
            enviar_mensagem_chat("Yellow_5_On")
            turn_emissive("Yellow_5", Yellow)
        else:
            enviar_mensagem_chat("Yellow_5_Off")
            turn_emissive("Yellow_5", Off)

        previous_button12_state = button12_state

def update_button12_state1():
    global button12_state, previous_button12_state

    background_color = (1, 1, 0)  
    opacity = 1.0 if button12_state else 0.3
    text = "ON" if button12_state else "OFF"

    ac.setText(extra_button12, text)
    ac.setFontColor(extra_button12, 0, 0, 0, 1)  
    ac.setBackgroundColor(extra_button12, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button12, opacity)

    if button12_state != previous_button12_state:
        if button12_state:
            #enviar_mensagem_chat("Yellow_5_On")
            turn_emissive("Yellow_5", Yellow)
        else:
            #enviar_mensagem_chat("Yellow_5_Off")
            turn_emissive("Yellow_5", Off)

        previous_button12_state = button12_state

previous_button13_state = False

def update_button13_state():
    global button13_state, previous_button13_state

    background_color = (1, 1, 0)  
    opacity = 1.0 if button13_state else 0.3
    text = "ON" if button13_state else "OFF"

    ac.setText(extra_button13, text)
    ac.setFontColor(extra_button13, 0, 0, 0, 1)  
    ac.setBackgroundColor(extra_button13, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button13, opacity)

    if button13_state != previous_button13_state:
        if button13_state:
            enviar_mensagem_chat("Yellow_6_On")
            turn_emissive("Yellow_6", Yellow)
        else:
            enviar_mensagem_chat("Yellow_6_Off")
            turn_emissive("Yellow_6", Off)

        previous_button13_state = button13_state

def update_button13_state1():
    global button13_state, previous_button13_state

    background_color = (1, 1, 0)  
    opacity = 1.0 if button13_state else 0.3
    text = "ON" if button13_state else "OFF"

    ac.setText(extra_button13, text)
    ac.setFontColor(extra_button13, 0, 0, 0, 1)  
    ac.setBackgroundColor(extra_button13, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button13, opacity)

    if button13_state != previous_button13_state:
        if button13_state:
            #enviar_mensagem_chat("Yellow_6_On")
            turn_emissive("Yellow_6", Yellow)
        else:
            #enviar_mensagem_chat("Yellow_6_Off")
            turn_emissive("Yellow_6", Off)

        previous_button13_state = button13_state

previous_button14_state = False

def update_button14_state():
    global button14_state, previous_button14_state

    background_color = (0, 1, 0)  
    opacity = 1.0 if button14_state else 0.3
    text = "ON" if button14_state else "OFF"

    ac.setText(extra_button14, text)
    ac.setFontColor(extra_button14, 0, 0, 0, 1)  
    ac.setBackgroundColor(extra_button14, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button14, opacity)

    if button14_state != previous_button14_state:
        if button14_state:
            enviar_mensagem_chat("Green_R_On")
            turn_emissive("GreenRight", Green)
        else:
            enviar_mensagem_chat("Green_R_Off")
            turn_emissive("GreenRight", Off)

        previous_button14_state = button14_state

def update_button14_state1():
    global button14_state, previous_button14_state

    background_color = (0, 1, 0)  
    opacity = 1.0 if button14_state else 0.3
    text = "ON" if button14_state else "OFF"

    ac.setText(extra_button14, text)
    ac.setFontColor(extra_button14, 0, 0, 0, 1)  
    ac.setBackgroundColor(extra_button14, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button14, opacity)

    if button14_state != previous_button14_state:
        if button14_state:
            #enviar_mensagem_chat("Green_R_On")
            turn_emissive("GreenRight", Green)
        else:
            #enviar_mensagem_chat("Green_R_Off")
            turn_emissive("GreenRight", Off)

        previous_button14_state = button14_state

previous_button15_state = False

def update_button15_state():
    global button15_state, previous_button15_state

    background_color = (1, 0, 0)  
    opacity = 1.0 if button15_state else 0.3
    text = "ON" if button15_state else "OFF"

    ac.setText(extra_button15, text)
    ac.setFontColor(extra_button15, 0, 0, 0, 1)  
    ac.setBackgroundColor(extra_button15, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button15, opacity)

    if button15_state != previous_button15_state:
        if button15_state:
            enviar_mensagem_chat("Red_R_On")
            turn_emissive("RedRight", Red)
        else:
            enviar_mensagem_chat("Red_R_Off")
            turn_emissive("RedRight", Off)

        previous_button15_state = button15_state

def update_button15_state1():
    global button15_state, previous_button15_state

    background_color = (1, 0, 0)  
    opacity = 1.0 if button15_state else 0.3
    text = "ON" if button15_state else "OFF"

    ac.setText(extra_button15, text)
    ac.setFontColor(extra_button15, 0, 0, 0, 1)  
    ac.setBackgroundColor(extra_button15, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button15, opacity)

    if button15_state != previous_button15_state:
        if button15_state:
            #enviar_mensagem_chat("Red_R_On")
            turn_emissive("RedRight", Red)
        else:
            #enviar_mensagem_chat("Red_R_Off")
            turn_emissive("RedRight", Off)

        previous_button15_state = button15_state

previous_button16_state = False

def update_button16_state():
    global button16_state, previous_button16_state

    background_color = (0, 0, 1) if button16_state else (0.5, 0.5, 0.5)  
    opacity = 1.0 if button16_state else 0.3
    text = "ON" if button16_state else "OFF"

    ac.setText(extra_button16, text)
    ac.setFontColor(extra_button16, 1, 1, 1, 1)  
    ac.setBackgroundColor(extra_button16, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button16, opacity)

    if button16_state != previous_button16_state:
        if button16_state:
            enviar_mensagem_chat("Pin_Right_On")
        else:
            enviar_mensagem_chat("Pin_Right_Off")

        previous_button16_state = button16_state

def update_button16_state1():
    global button16_state, previous_button16_state

    background_color = (0, 0, 1) if button16_state else (0.5, 0.5, 0.5)  
    opacity = 1.0 if button16_state else 0.3
    text = "ON" if button16_state else "OFF"

    ac.setText(extra_button16, text)
    ac.setFontColor(extra_button16, 1, 1, 1, 1)  
    ac.setBackgroundColor(extra_button16, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button16, opacity)

    if button16_state != previous_button16_state:
        previous_button16_state = button16_state

previous_button17_state = False

def update_button17_state():
    global button17_state, previous_button17_state

    background_color = (0, 0, 1) if button17_state else (0.5, 0.5, 0.5)  
    opacity = 1.0 if button17_state else 0.3
    text = "PLAYING..." if button17_state else "START"

    ac.setText(extra_button17, text)
    ac.setFontColor(extra_button17, 1, 1, 1, 1) 
    ac.setBackgroundColor(extra_button17, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button17, opacity)

    if button17_state != previous_button17_state:
        if button17_state:
            enviar_mensagem_chat("Pin_On")
        else:
            enviar_mensagem_chat("Pin_Off")

        previous_button17_state = button17_state

def update_button17_state1():
    global button17_state, previous_button17_state

    background_color = (0, 0, 1) if button17_state else (0.5, 0.5, 0.5)  
    opacity = 1.0 if button17_state else 0.3
    text = "PLAYING..." if button17_state else "START"

    ac.setText(extra_button17, text)
    ac.setFontColor(extra_button17, 1, 1, 1, 1) 
    ac.setBackgroundColor(extra_button17, background_color[0], background_color[1], background_color[2])
    ac.setBackgroundOpacity(extra_button17, opacity)

    if button17_state != previous_button17_state:
        previous_button17_state = button17_state



def update_timer():
    global pin_on,pin_on_fire, timer_running, timer_start_time, timer_duration , button8_state ,  button9_state , button10_state ,button5_state ,  button6_state ,  button7_state
    global button11_state,button12_state,button13_state,button14_state,button15_state,button16_state ,button17_state, is_left ,  is_right, falseStart   
    
    if timer_running:
        elapsed_time = time.time() - timer_start_time
        remaining_time = max(timer_duration - elapsed_time, 0)
        
        minutes = int(remaining_time) // 60
        seconds = int(remaining_time) % 60
        timer_text = "{:02}:{:02}".format(minutes, seconds)
        ac.setText(timer_label,timer_text)

        if is_left:
            if 2 <= remaining_time <= 2.5:   
                button5_state = True
                update_button5_state1() 
            else:
                button5_state = False
                update_button5_state1() 
    
            if 1.5 <= remaining_time <= 2:   
                button6_state = True
                update_button6_state1() 
            else:
                button6_state = False
                update_button6_state1() 
    
            if 1 <= remaining_time <= 1.5:   
                button7_state = True
                update_button7_state1() 
            else:
                button7_state = False
                update_button7_state1()
    
            if 0.9 <= remaining_time <= 1:   
                button8_state = True
                update_button8_state1()  
                pin_on_fire = False
    
            if remaining_time <= 0:
                timer_running = False
                button8_state = False
                update_button8_state1()
                button10_state = False
                update_button10_state1()
                button17_state = False
                update_button17_state1()
                pin_on = False
                falseStart = False 
    
        if is_right:
            if 2 <= remaining_time <= 2.5:   
                button11_state = True
                update_button11_state1() 
            else:
                button11_state = False
                update_button11_state1() 
        
            if 1.5 <= remaining_time <= 2:   
                button12_state = True
                update_button12_state1() 
            else:
                button12_state = False
                update_button12_state1() 
        
            if 1 <= remaining_time <= 1.5:   
                button13_state = True
                update_button13_state1() 
            else:
                button13_state = False
                update_button13_state1()
        
            if 0.9 <= remaining_time <= 1:   
                button14_state = True
                update_button14_state1()  
                pin_on_fire=False               
        
            if remaining_time <= 0:
                timer_running = False
                button14_state = False
                update_button14_state1()
                button16_state = False
                update_button16_state1()
                button17_state = False
                update_button17_state1()
                pin_on = False
                falseStart = False 

    

def resetTimer():
    global reaction_time, timer_active, timer_start
    timer_start = None
    reaction_time = 0
    timer_active = False
    updateReactionTimeLabel(reaction_time)

def updateReactionTimeLabel(time_value):
    global reaction_time_label
    ac.setText(reaction_time_label,"{:.3f}".format(time_value))

def updateBestReactionTimeLabel(best_time_value):
    global best_reaction_time_label
    ac.setText(best_reaction_time_label,"{:.3f}".format(best_time_value))


def update_on_stage():
    global on_stage
    on_stage = is_car_on_stage()

def is_car_on_stage():
    is_stage_left = is_car_in_stage_left()
    is_stage_right = is_car_in_stage_right()
    
    return is_stage_left or is_stage_right


def acUpdate(deltaT):
   # Definição das variáveis globais
    global buttons_enabled,button_last_click,pin_on,falseStart
    global pin_on_fire, on_stage, car_moving, reaction_time, best_reaction_time, timer_start, timer_active, previous_pin_on_fire

    update_timer()
    pos = ac.getCarState(0, acsys.CS.WorldPosition)
    x = round(pos[0], 2)
    y = round(pos[1], 2)
    z = round(pos[2], 2)
    ac.setText(pos_label, "Posição: X=" + str(x) + ", Y=" + str(y) + ", Z=" + str(z))

    if not pin_on:
        if not buttons_enabled and time.time() - button_last_click > 0.95:
        # Reativar todos os botões após 1 segundo
            enable_all_buttons()

    update_on_stage()
   
    speed_kmh = ac.getCarState(0, acsys.CS.SpeedKMH)
 
    if int(speed_kmh) > 1:
        car_moving = True
    else:
        car_moving =  False

    
    if previous_pin_on_fire and not pin_on_fire and on_stage and not falseStart:
        if not timer_active:
            timer_start = time.time()  
            timer_active = True
            reaction_time = 0 
         
            
    if not falseStart and on_stage:
        if car_moving and timer_active:
            reaction_time = time.time() - timer_start
            add_log_message("Reaction time: {:.3f} seconds".format(reaction_time))
            enviar_mensagem_chat("Reacted in: {:.3f} seconds".format(reaction_time))
            updateReactionTimeLabel(reaction_time)
            #startMeasuring()

            if reaction_time < best_reaction_time and not reaction_time==0:
                best_reaction_time = reaction_time
                updateBestReactionTimeLabel(best_reaction_time)

            timer_active = False
    
    if timer_active and timer_start is not None:
        current_time = time.time()  
        if current_time - timer_start >= reset_time:
           resetTimer()

    previous_pin_on_fire = pin_on_fire



def acShutdown():
    pass

import socket
from threading import Thread, Lock, Condition
from RSA import generate_keys, encrypt, decrypt
import json
import sys
from PyQt5.QtWidgets import *
from time import sleep

#  ---------------  Função do servidor  --------------------

def chat_receive(port, private_key):
    """Função responsável por ficar aguardando receber a mensagem"""

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', port))
        message_display.append("Aguardando mensagens na porta: " + str(port))

        v = 0

        while True:
            data, _ = sock.recvfrom(1024)
            if v == 0:
                v = 1
                message = data.decode('utf-8')
                public_key2 = json.loads(message)

                with open('public_key.json', 'w') as file:
                    json.dump(public_key2, file)

                message_display.append('Chave recebida')
                
            else:
                message = decrypt(data, private_key)
                message_display.append(message)
            
            sleep(0.01)
            scrollbar = message_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
            
    except socket.error as e:
        print("Erro ao receber mensagem:", str(e))

    finally:
        sock.close()

#  ---------------  Função do cliente  --------------------

def chat_send(public_key, host, port, seu_nome, lock, condition):
    """Função responsável por enviar a mensagem ao destino"""

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(str(public_key).encode('UTF-8'), (host, port))

        while True:
            message = receber_texto('Digite a mensagem: ' , lock, condition)
            message2 = 'Você: ' + message
            message = seu_nome + ': ' + message
            
            try:
                with open('public_key.json', 'r') as file:
                    public_key2 = json.load(file)

                message = encrypt(message, public_key2)
                sock.sendto(message, (host, port))
                message_display.append(message2)

            except:
                message_display.append("Você não possui a chave!")

            sleep(0.01)
            scrollbar = message_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    except socket.error as e:
        print("Erro ao enviar mensagem:", str(e))

    finally:
        sock.close()

#  ---------------  Inicia as threads de servidor e cliente  --------------------

def client_server():
    """Funcão responsável por iniciar as threads do cliente e servidor, e setar as configurações iniciais"""

    try:
        with open('mykeys.json', 'r') as file:
            mykeys = list(json.load(file))

        public_key = mykeys[0]
        private_key = mykeys[1]

    except:
        label_status.setText('Gerando Chaves')
        public_key, private_key = generate_keys(2000, 5000)
        with open('mykeys.json', 'w') as file:
            json.dump([public_key, private_key], file)

    tr1 = Thread(target=chat_receive, args=(12345, private_key))
    tr1.daemon = True
    tr1.start()

    seu_nome = receber_texto('Digite seu nome: ' , lock, condition)
    host = receber_texto('Digite o IP de destino: ' , lock, condition)

    tr2 = Thread(target=chat_send, args=(public_key ,host, 12345, seu_nome, lock, condition))
    tr2.daemon = True
    tr2.start()
    
#  ---------------  Destrava as treads em aguardo  --------------------

def destravar_thread(condition):
    """Destrava a thread bloqueada"""

    with condition:
        condition.notify() 

#  ---------------  Captura o texto digitado no input da interface  --------------------

def receber_texto(texto , lock, condition):
    """Faz a thread aguardar até que seja desbloqueada pela função destravar_thread() e logo opós desbloqueda faz a leitura do texto no input"""

    label_status.setText(texto)

    with lock:
        condition.wait() 
        
    message = message_input.text()
    message_input.clear()
    return message

#  ---------------  Inicia a thread client_server  --------------------

def start_thread_server_cliente(send_button2):
    """Inicia a thread que inicia as outras threads cliente e servidor"""

    layout.removeWidget(send_button2)
    send_button2.deleteLater()

    send_button = QPushButton("Enviar")
    send_button.clicked.connect(lambda: destravar_thread(condition))
    layout.addWidget(send_button)

    message_input.returnPressed.connect(lambda: destravar_thread(condition)) 

    tr3 = Thread(target=client_server) 
    tr3.start()


#########################  Código principal  #########################


#  ---------------  Bloqueadores de threads  --------------------

lock = Lock()
condition = Condition(lock)

#  ---------------  App de interface grafica  -------------------

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Chat")
window.resize(500, 500)

layout = QVBoxLayout(window)

message_display = QTextEdit()
message_display.setReadOnly(True)
layout.addWidget(message_display)

label_status = QLabel("Aperte em iniciar")
layout.addWidget(label_status)

message_input = QLineEdit()
layout.addWidget(message_input)

send_button = QPushButton("Iniciar")
send_button.clicked.connect(lambda: start_thread_server_cliente(send_button))
layout.addWidget(send_button)

send_button.click()

window.show()
app.exec_()

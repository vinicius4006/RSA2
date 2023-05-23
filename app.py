import socket
from threading import Thread, Lock, Condition
from RSA import generate_keys, encrypt, decrypt
import json
import sys
from PyQt5.QtWidgets import *

def chat_receive(port, private_key):
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
            
    except socket.error as e:
        print("Erro ao receber mensagem:", str(e))

    finally:
        sock.close()


def chat_send(public_key, host, port, seu_nome, lock, condition):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        label_status.setText('Aperte Enviar para enviar a chave publica: ')

        with lock:
            condition.wait() 

        sock.sendto(str(public_key).encode('UTF-8'), (host, port))

        while True:
            message = receber_texto('Digite a mensagem: ' , lock, condition)
            message2 = 'Você: ' + message
            message = seu_nome + ': ' + message
            message_display.append(message2)
            
            with open('public_key.json', 'r') as file:
                public_key2 = json.load(file)

            message = encrypt(message, public_key2)
            sock.sendto(message, (host, port))

    except socket.error as e:
        print("Erro ao enviar mensagem:", str(e))

    finally:
        sock.close()

#  ---------------  Inicia as threads de servidor e cliente  --------------------

def client_server():
    public_key, private_key = generate_keys(100, 200)

    tr1 = Thread(target=chat_receive, args=(12345, private_key))
    tr1.daemon = True

    seu_nome = receber_texto('Digite seu nome: ' , lock, condition)
    host = receber_texto('Digite o IP de destino: ' , lock, condition)

    tr2 = Thread(target=chat_send, args=(public_key ,host, 12345, seu_nome, lock, condition))
    tr2.daemon = True

    tr1.start()
    tr2.start()
    
#  ---------------  Destrava as treads em aguardo  --------------------

def destravar_tread(condition):
    with condition:
        condition.notify() 

#  ---------------  Captura o texto digitado no input da interface  --------------------

def receber_texto(texto , lock, condition):
    label_status.setText(texto)
    with lock:
        condition.wait() 
        
    message = message_input.text()
    message_input.clear()
    return message

#  ---------------  Inicia a thread client_server  --------------------

def remover_widget():
    button = app.focusWidget()
    if button:
        layout.removeWidget(button)
        button.deleteLater()

    send_button = QPushButton("Enviar")
    send_button.clicked.connect(lambda: destravar_tread(condition))
    layout.addWidget(send_button)

    tr3 = Thread(target=client_server) 
    tr3.start()


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
send_button.clicked.connect(remover_widget)
layout.addWidget(send_button)

window.show()
app.exec_()

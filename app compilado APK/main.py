import socket
from threading import Thread, Lock, Condition
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
import math
import random
from random import sample
import base64
import json


def mdc(n1: int, n2: int) -> int:
    while n2:
        n1, n2 = n2, n1 % n2
    return n1


def co_primos(z:int) -> int:
    b = 1
    coprimos = []
    while len(coprimos) < z:
        res = mdc(z, b)
        if res == 1:
            coprimos.append(b)
        b += 1

    d = sample(coprimos, 1)
    return int(d[0])


def find_e(d: int, z: int) -> int:
    e = 1
    while True:
        if d * e % z == 1:
            return e
        e += 1


def calculate_N(P, Q):
    N = P * Q
    return N


def calculate_Z(P, Q):
    Z = (P - 1) * (Q - 1)
    return Z


def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False

    sqrt_num = int(math.sqrt(num)) + 1
    for divisor in range(5, sqrt_num, 6):
        if num % divisor == 0 or num % (divisor + 2) == 0:
            return False

    return True


def generate_prime_number(inicio, fim):
        stop = True 
        num_prime = 2
        while stop:
             new_num = random.randint(inicio, fim)
             if is_prime(new_num):
                  num_prime = new_num
                  stop = False
        return num_prime
    

def generate_keys(range_in, range_out):
    p = generate_prime_number(range_in, range_out) 
    q = generate_prime_number(range_in, range_out) 
    n = calculate_N(p, q)
    z = calculate_Z(p, q)
    d = co_primos(z)
    e = find_e(d, z)
    public_key, private_key = [e, n], [d, n]
    return public_key, private_key


def encrypt(message, public_key):
    e, n = public_key
    encrypt_list = [pow(ord(char.encode("latin1")), e, n) for char in message]
    encrypt_list = str(encrypt_list)
    return base64.b64encode(encrypt_list.encode('UTF-8'))


def decrypt(encrypt_list, private_key):
    encrypt_list = list(json.loads(str(base64.b64decode(encrypt_list))[2:-1]))
    d, n = private_key
    message = ''.join([chr(pow(char, d, n)) for char in encrypt_list])
    return message

# Global variables
message_display = None
message_input = None
label_status = None
lock = Lock()
condition = Condition(lock)

# Server function
def chat_receive(port, private_key):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', port))
        Clock.schedule_once(lambda dt: setattr(message_display, 'text', message_display.text + "\nAguardando mensagens na porta: " + str(port)))

        v = 0

        while True:
            data, _ = sock.recvfrom(1024)
            if v == 0:
                v = 1
                message = data.decode('utf-8')
                public_key2 = json.loads(message)

                with open('public_key.json', 'w') as file:
                    json.dump(public_key2, file)

                Clock.schedule_once(lambda dt: setattr(message_display, 'text', message_display.text + "\nChave recebida"))
                
            else:
                message = decrypt(data, private_key)
                Clock.schedule_once(lambda dt: setattr(message_display, 'text', message_display.text + "\n" + message))
            
            
            scrollbar = message_display.scroll_y
            if scrollbar < 0:
                scrollbar = 0
            Clock.schedule_once(lambda dt: setattr(message_display, 'scroll_y', 1))
            
    except socket.error as e:
        print("Erro ao receber mensagem:", str(e))

    finally:
        sock.close()

# Client function
def chat_send(public_key, host, port, seu_nome):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(str(public_key).encode('UTF-8'), (host, port))

        while True:
            message = receber_texto('Digite a mensagem: ')
            message2 = 'Você: ' + message
            message = seu_nome + ': ' + message
            
            try:
                with open('public_key.json', 'r') as file:
                    public_key2 = json.load(file)

                message = encrypt(message, public_key2)
                sock.sendto(message, (host, port))
                Clock.schedule_once(lambda dt: setattr(message_display, 'text', message_display.text + "\n" + message2))

            except:
                Clock.schedule_once(lambda dt: setattr(message_display, 'text', message_display.text + "\nVocê não possui a chave!"))

            
            scrollbar = message_display.scroll_y
            if scrollbar < 0:
                scrollbar = 0
            Clock.schedule_once(lambda dt: setattr(message_display, 'scroll_y', 1))

    except socket.error as e:
        print("Erro ao enviar mensagem:", str(e))

    finally:
        sock.close()

# Helper function to receive input
def receber_texto(texto):
    Clock.schedule_once(lambda dt: setattr(label_status, 'text', texto))
    with lock:
        condition.wait() 
        
    message = message_input.text
    Clock.schedule_once(lambda dt: setattr(message_input, 'text', ''))
    return message

# Start server and client threads
def remover_widget(instance):
    layout = instance.parent
    layout.remove_widget(instance)

    send_button = Button(text="Enviar", size_hint=(1, 0.1))
    send_button.bind(on_press=destravar_tread)
    layout.add_widget(send_button)

    message_input.bind(on_text_validate=destravar_tread)

    tr3 = Thread(target=client_server) 
    tr3.start()

def destravar_tread(instance):
    with condition:
        condition.notify() 

def client_server():
    try:
        with open('mykeys.json', 'r') as file:
            mykeys = list(json.load(file))

        public_key = mykeys[0]
        private_key = mykeys[1]

    except:
        Clock.schedule_once(lambda dt: setattr(label_status, 'text', 'Gerando Chaves'))
        public_key, private_key = generate_keys(2000, 5000)
        with open('mykeys.json', 'w') as file:
            json.dump([public_key, private_key], file)

    tr1 = Thread(target=chat_receive, args=(12345, private_key))
    tr1.daemon = True
    tr1.start()

    seu_nome = receber_texto('Digite seu nome: ')
    host = receber_texto('Digite o IP de destino: ')

    tr2 = Thread(target=chat_send, args=(public_key ,host, 12345, seu_nome))
    tr2.daemon = True
    tr2.start()

# Main app class
class ChatApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        global message_display, message_input, label_status

        message_display = TextInput(readonly=True, size_hint=(1, 0.8), multiline=True, text="")
        layout.add_widget(message_display)

        label_status = Label(text="Aperte em iniciar", size_hint=(1, 0.1))
        layout.add_widget(label_status)

        message_input = TextInput(size_hint=(1, 0.1))
        layout.add_widget(message_input)

        send_button = Button(text="Iniciar", size_hint=(1, 0.1))
        send_button.bind(on_press=remover_widget)
        layout.add_widget(send_button)

        return layout

if __name__ == '__main__':
    ChatApp().run()

import socket
from threading import Thread
from RSA import generate_keys, encrypt, decrypt
import json
from time import sleep

def chat_receive(port, private_key):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', port))
        print("Aguardando mensagens na porta", port)

        v = 0

        while True:
            data, addr = sock.recvfrom(1024)
            if v == 0:
                v = 1
                message = data.decode('utf-8')
                public_key2 = json.loads(message)
                with open('public_key.json', 'w') as file:
                    json.dump(public_key2, file)
                print('\nChave recebida')
                
            else:
                message = decrypt(data, private_key)
                print('\n' + message)
            
    except socket.error as e:
        print("Erro ao receber mensagem:", str(e))

    finally:
        sock.close()


def chat_send(public_key, host, port, seu_nome):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sleep(0.5)
        input('Aperte Enter para enviar a chave publica: ')
        sock.sendto(str(public_key).encode('UTF-8'), (host, port))

        while True:
            message = input('Digite a mensagem: ')
            message = seu_nome + ': ' + message
            # print(message)
            with open('public_key.json', 'r') as file:
                public_key2 = json.load(file)

            message = encrypt(message, public_key2)
            sock.sendto(message, (host, port))

    except socket.error as e:
        print("Erro ao enviar mensagem:", str(e))

    finally:
        sock.close()


public_key, private_key = generate_keys(100, 200)

print(public_key)

tr1 = Thread(target=chat_receive, args=(12345, private_key))
tr1.daemon = True

seu_nome = input('Digite seu nome: ')
host = input('Digite o ip de destino: ')
tr2 = Thread(target=chat_send, args=(public_key ,host, 12345, seu_nome))
tr2.daemon = True

tr1.start()
tr2.start()

tr1.join()
tr2.join()

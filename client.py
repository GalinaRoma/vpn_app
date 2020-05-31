import socket
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from crypro import encrypt, decrypt


def create_client_app():
    sock = socket.socket()
    sock.connect(('localhost', 9090))

    f = open('secret.txt', 'r')

    p = f.read().encode()
    if len(p) != 16:
        print('Common key should be 16 digit')
        return

    session_key = prepare_session_key(sock, p)
    if not session_key:
        print('session key is not established')
        return

    open_text = input('Enter message: ')
    print('Sending text: ' + open_text)
    print('Length of text: ' + str(len(open_text)))

    open_text = pad(open_text.encode(), 16)
    cipher = encrypt(open_text, session_key)
    sock.send(cipher)

    sock.close()


def prepare_session_key(sock, p):
    # encrypt random key and send to server
    client_key = get_random_bytes(16)
    encrypted_data = encrypt(client_key, p)
    sock.send(encrypted_data)

    # receive session key and decrypt by p key
    encrypted_data = sock.recv(48)
    encrypted_data = decrypt(encrypted_data, p)

    # decrypt by client random key
    session_key = decrypt(encrypted_data, client_key)

    # check the created session key
    r_client = get_random_bytes(16)
    encrypted_data = encrypt(r_client, session_key)
    sock.send(encrypted_data)

    # receive the encrypted r_client + r_server and decrypted them
    encrypted_data = sock.recv(48)
    r_client_server = decrypt(encrypted_data, session_key)
    r_client_received = r_client_server[:16]

    # if texts are the same, decrypt r_server and send it
    if r_client == r_client_received:
        encrypted_data = encrypt(r_client_server[16:], session_key)
        sock.send(encrypted_data)
        return session_key

    return

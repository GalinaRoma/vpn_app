import socket
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad, pad
from crypro import encrypt, decrypt


def create_server_app():
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen(1)
    conn, addr = sock.accept()

    f = open('secret.txt', 'r')

    p = f.read().encode()
    if len(p) != 16:
        print('Common key should be 16 digit')
        return

    session_key = prepare_session_key(conn, p)
    if not session_key:
        print('session key is not established')
        return

    encrypted_data = b''
    while True:
        data = conn.recv(1024)
        if data:
            encrypted_data += data
        else:
            break

    decrypted_data = decrypt(encrypted_data, session_key)
    decrypted_data = unpad(decrypted_data, 16)
    decrypted_data = decrypted_data.decode()
    print('Receiving text: ' + decrypted_data)
    print('Length of text: ' + str(len(decrypted_data)))

    conn.close()


def prepare_session_key(conn, p):
    # receive encrypted random client key
    encrypted_data = conn.recv(32)
    client_key = decrypt(encrypted_data, p)

    # create session key and encrypt it by client key
    session_key = get_random_bytes(16)
    encrypted_data = encrypt(session_key, client_key)

    # encrypt session key by p key and send it
    encrypted_data = encrypt(encrypted_data, p)
    conn.send(encrypted_data)

    # check the created session key
    encrypted_data = conn.recv(32)
    r_client = decrypt(encrypted_data, session_key)

    # create random r_server and encrypt sum of texts
    r_server = get_random_bytes(16)
    r_client_server = r_client + r_server
    encrypted_data = encrypt(r_client_server, session_key)
    conn.send(encrypted_data)

    # receive encrypted r_server, decrypt it and check
    encrypted_data = conn.recv(1024)
    r_server_receive = decrypt(encrypted_data, session_key)

    if r_server == r_server_receive:
        return session_key

    return

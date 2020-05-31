from Crypto.Cipher import AES


def decrypt(data, key):
    iv = data[:16]
    aes = AES.new(key, AES.MODE_CBC, iv=iv)
    return aes.decrypt(data[16:])


def encrypt(data, key):
    aes = AES.new(key, AES.MODE_CBC)
    encrypted_data = aes.encrypt(data)
    return aes.iv + encrypted_data

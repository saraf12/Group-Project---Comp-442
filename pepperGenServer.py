from cryptography.fernet import Fernet
key = Fernet.generate_key()
with open("pepper.bin", 'wb') as fout:
    fout.write(key)

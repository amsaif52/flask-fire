from flask import Flask, request
import base64
from Crypto.Cipher import AES

BLOCK_SIZE = 16
PADDING = '{'
mode = AES.MODE_ECB
hash_key = '-z%c{-V{TowG5Gi]T3!(VNwGuR$Cl9DF'
def pad(s):
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
def EncodeAES(c, s):
    return base64.b64encode(c.encrypt(pad(s).encode('UTF-8')))
def DecodeAES(c, e):
    return c.decrypt(base64.b64decode(e)).rstrip(PADDING)
def ogEncryption(s):
    cipher = AES.new(hash_key.encode('UTF-8'), mode)
    encoded = EncodeAES(cipher, s).decode('UTF-8')
    return encoded
x = ogEncryption('11/2021')
y = ogEncryption('Ali Asgar Merchant')
z = ogEncryption('xxxxxxxxxxxx1111')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        request_data = request.get_json()
        print(request_data)
    return 'Query String Example'

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
from flask import Flask, request, jsonify
import base64
from Crypto.Cipher import AES
import requests
import json

app = Flask(__name__)


@app.route('/ogauth',methods = ['POST', 'GET'])
def ogauth():
    if request.method == 'POST':
        BLOCK_SIZE = 16
        PADDING = '{'
        mode = AES.MODE_ECB
        hash_key = '-z%c{-V{TowG5Gi]T3!(VNwGuR$Cl9DF'
        def pad(s):
            return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
        def EncodeAES(c, s):
            return base64.b64encode(c.encrypt(pad(s).encode('UTF-8')))
        def ogEncryption(s):
            cipher = AES.new(hash_key.encode('UTF-8'), mode)
            encoded = EncodeAES(cipher, s).decode('UTF-8')
            return encoded
        data = request.get_json()
        authorization = request.headers["authorization"]
        expiry = ogEncryption(data["payment"]["cc_exp_date"])
        last4 = ogEncryption(data["payment"]["cc_last_4"])
        data["payment"]["cc_exp_date"] = expiry
        data["payment"]["cc_last_4"] = last4
        url = "https://staging.sc.ordergroove.com/subscription/create"
        payload = "create_request={}".format(json.dumps(data, separators=(',', ':')))
        headers = {
        'Authorization': authorization,
        'Content-Type': 'application/json'
        }
        print(payload)
        print(headers)
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text
    else:
        return 'Working'

if __name__ == '__main__':
   app.run(debug = True, port=5000)
from amazoncaptcha import AmazonCaptcha
from PIL import Image
import io
import numpy as np
from jose import jwt
from jose import jws
from jwcrypto import jwk
import json
import json
import base64
from io import BytesIO
from scapy.all import RawPcapReader, rdpcap, DNS, UDP, IP
from bisect import insort_right

def cipher_solver(question):
    encoded_string = question
    padding = len(encoded_string) & 3
    if padding != 0:
        encoded_string += '=' * (4 - padding)

    decoded_string = base64.b64decode(encoded_string).decode('utf-8')

    decoded_string = decoded_string[1:len(decoded_string) - 1]

    pair = decoded_string.split(",")
    shift = int(pair[1], 2);
    sz = len(pair[0]) / 7;
    ans = "";
    ind = 0;
    for i in range(int(sz)):
        bit_str = "";
        for j in range(7):
            bit_str += pair[0][ind];
            ind += 1;
        ch = int(bit_str, 2)
        if chr(ch).isupper():
            ch -= shift;
            if ch < ord('A'):
                ch += 26;
        else:
            ch -= shift;
            if ch < ord('a'):
                ch += 26;
        ans += chr(ch);
    
    return ans;

def captcha_solver(question):
    img = Image.fromarray(np.uint8(question))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img = img_byte_arr.getvalue()
    img = io.BytesIO(img)
    
    # Create an AmazonCaptcha object with the image
    captcha = AmazonCaptcha(img)

    # Get the captcha solution
    solution = captcha.solve()
    return solution
    

def pcap_solver(question):
    decoded_data = base64.b64decode(question)

    required_portions = []
    for pkt in rdpcap(BytesIO(decoded_data)):
        if UDP in pkt and pkt[UDP].dport == 53 and pkt[IP].dst == '188.68.45.12':
            dns = pkt[DNS].qd.qname.decode()
            cnt, dta = dns.split('.')[:2]
            rank = int(base64.b64decode(cnt + '=' * (4 - (len(cnt) & 3))).decode('utf-8'))
            decoded_secret = base64.b64decode(dta + '=' * (4 - (len(dta) & 3))).decode('utf-8')
            insort_right(required_portions, (rank, decoded_secret))

    return ''.join([portion[1] for portion in required_portions])


def server_solver(question):
    headers = jwt.get_unverified_header(question)
    payload = jwt.get_unverified_claims(question)

    # We don't need to generate a new key pair every time. So we just fixed a the pair of (private_key, public_key) 
    private_key = {'d': 'gsqMAw5ppfg1jEmHhiadjN1ThQnjUQdNbFE9R6oagPJWrOd9_8pB7e8I_kigeaT3JOK0wi5txSS8nRvfi9n5YQ', 'dp': 'u862hZE6hEjW2urFKQ2x5ArG3fHmfH8C0Ovo6Ndf2gk', 'dq': 'ikUDZNe9fM0emzuKsTknKg3i-PhNNBr_CqyMmF7ig00', 'e': 'AQAB', 'kid': '92c5a551-261e-4999-8d23-0235a8653561', 'kty': 'RSA', 'n': 'kg9MIJrccyKgAfNC9VbijYorgpoFphAZNjvWwUcR1leDocH6HJqT3AY6pCZd-g0UP46zQyFQmQigFVyApfR8Fw', 'p': 'wqtFGpBX_zQsuzYv0Rvrx1m3GS7ohaLU-unZBz6gj5k', 'q': 'wBOFl_wbEbFhk66NLHZASTd-lqEFDHLsa5bxlP3Kdy8', 'qi': 'gBiU7QN4XUd3ZZ6I2KJLqivOHER8GuUrbFnjJKLx-Rg'}
    public_key = {'e': 'AQAB', 'kid': '92c5a551-261e-4999-8d23-0235a8653561', 'kty': 'RSA', 'n': 'kg9MIJrccyKgAfNC9VbijYorgpoFphAZNjvWwUcR1leDocH6HJqT3AY6pCZd-g0UP46zQyFQmQigFVyApfR8Fw'}

    payload['admin'] = 'true'
    headers['jwk'] = public_key
    headers['kid'] = public_key['kid']

    return jws.sign(payload, key=private_key, algorithm="RS256", headers=headers);
   
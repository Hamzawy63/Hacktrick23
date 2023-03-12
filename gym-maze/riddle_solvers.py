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

def cipher_solver(question):
    encoded_string = question
    padding = len(encoded_string) % 4
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

    packets = rdpcap(BytesIO(decoded_data))
    
    dns_packets = [pkt for pkt in packets if UDP in pkt and pkt[UDP].dport == 53 and pkt[IP].dst == '188.68.45.12']

    sent_data = []
    # Process each DNS packet
    for packet in dns_packets:
        # Extract DNS information from the packet
        dns = packet[DNS]
        sent_data.append(f"{dns.qd.qname.decode()}")

    required_portions = []
    for item in sent_data:
        cnt, dta = item.split('.')[:2]
        rank = int(base64.b64decode(cnt + '=' * (4 - len(cnt) % 4)).decode('utf-8'))
        decoded_secret = base64.b64decode(dta + '=' * (4 - len(dta) % 4)).decode('utf-8')
        required_portions.append([rank, decoded_secret])

    result = ''
    for _, plain in sorted(required_portions, key=lambda x: x[0]):
        result += plain
    
    return result


def server_solver(question):
    pass
    # headers = jwt.get_unverified_header(question)
    # payload = jwt.get_unverified_claims(question)
    # key = headers['jwk']
    # algorithm = headers['alg']
    # kid = headers['jwk']['kid']
    # kty = headers['jwk']['kty']
    # e = headers['jwk']['e']

    # key = jwk.JWK.generate(kty=kty, size=512, kid=kid, e=e)
    # private_key = json.loads(key.export_private())
    # public_key = json.loads(key.export_public())

    # payload['admin'] = 'true'
    # headers['jwk'] = public_key

    # return jws.sign(payload, key=private_key, algorithm=algorithm, headers=headers)
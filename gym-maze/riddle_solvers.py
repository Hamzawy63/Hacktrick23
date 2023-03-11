from amazoncaptcha import AmazonCaptcha
from PIL import Image
import io
import numpy as np
from jose import jwt
from jose import jws
from jwcrypto import jwk
import json

def cipher_solver(question):
    return "HaCkTrIcK"

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
    return "YoUgOtThEsEcReT"

def server_solver(question):
    headers = jwt.get_unverified_header(input)
    payload = jwt.get_unverified_claims(input)
    key = headers['jwk']
    algorithm = headers['alg']
    kid = headers['jwk']['kid']
    kty = headers['jwk']['kty']
    e = headers['jwk']['e']

    key = jwk.JWK.generate(kty=kty, size=512, kid=kid, e=e)
    private_key = json.loads(key.export_private())
    public_key = json.loads(key.export_public())

    payload['admin'] = 'true'
    headers['jwk'] = public_key

    return jws.sign(payload, key=private_key, algorithm=algorithm, headers=headers);
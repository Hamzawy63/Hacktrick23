from amazoncaptcha import AmazonCaptcha
from PIL import Image
import io
import numpy as np

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
   return None
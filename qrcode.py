!pip install qrcode[pil]

import qrcode
from PIL import Image
from google.colab import files
import io

link = input("Digite seu link: ")
cor_qr = input("Digite a cor do QR code em código hex: ")
cor_fundo = input("Digite a cor do fundo em código hex: ")

print("Selecione a imagem da logo:")
uploaded = files.upload()
logo_filename = list(uploaded.keys())[0]

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=2)

qr.add_data(link)
qr.make(fit=True)

img_qr = qr.make_image(fill_color=cor_qr, back_color=cor_fundo).convert('RGB')

largura_qr, altura_qr = img_qr.size
tamanho_logo = largura_qr // 4
pos_x = (largura_qr - tamanho_logo) // 2
pos_y = (altura_qr - tamanho_logo) // 2

from PIL import ImageDraw
draw = ImageDraw.Draw(img_qr)
draw.rectangle([pos_x, pos_y, pos_x + tamanho_logo, pos_y + tamanho_logo], fill=cor_qr)

logo = Image.open(logo_filename).convert('L')

logo = logo.point(lambda x: 0 if x < 128 else 255, '1')
logo = logo.convert('RGB')

datas = logo.getdata()
new_data = []
for item in datas:

  if item[0] < 128:
        new_data.append(Image.new('RGB', (1,1), cor_qr).getpixel((0,0)))
  else:
        new_data.append(Image.new('RGB', (1,1), cor_fundo).getpixel((0,0)))
logo.putdata(new_data)
logo = logo.resize((tamanho_logo, tamanho_logo), Image.LANCZOS)
img_qr.paste(logo, (pos_x, pos_y))

img_qr.save("qrcode_final.png")
display(img_qr)

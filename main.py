""" Create a QR Code that contains the logo """
import qrcode
from PIL import Image

QR_TEXT = "http://www.hurriyet.com.tr"

# logo must be squere
LOGO_FILE = "logo.png"

# Output file name
OUTPUT_FILE_NAME = "output.png"

# http://www.qrcode.com/en/about/version.html
QR_VERSION = 2

# http://www.qrcode.com/en/about/error_correction.html
# ex. ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
ERROR_CORRECTION = qrcode.constants.ERROR_CORRECT_H

# Box size in the qr code
BOX_SIZE = 10

# The white space around the qr code (BORDER * BOX_SIZE)
BORDER = 4

# If True, find the best fit (increse the qr version) for the data to avoid data overflow errors
# ex. True, False
FIT = True

def create_logo():
    """ main function """
    qr_img = get_qr_image(QR_TEXT, QR_VERSION, ERROR_CORRECTION, BOX_SIZE, BORDER, FIT)
    qr_img_w, qr_img_h = qr_img.size

    logo_img = get_logo_image(qr_img_h, ERROR_CORRECTION, BOX_SIZE, BORDER, LOGO_FILE)
    logo_img_w, logo_img_h = logo_img.size

    offset = (int((qr_img_w - logo_img_w) / 2), int((qr_img_h - logo_img_h) / 2))
    qr_img.paste(logo_img, offset)

    qr_img.save(OUTPUT_FILE_NAME)

def get_qr_image(qr_text, qr_version, error_correction, box_size, border, fit):
    """ creates qr image """
    qr_code = qrcode.QRCode(qr_version, error_correction, box_size, border)
    qr_code.add_data(qr_text)
    qr_code.make(fit=fit)

    return qr_code.make_image()

def get_logo_image(qr_img_h, error_correction, box_size, border, logo_file):
    "creates logo image"
    thumbnail_logo_h = qr_img_h - (2 * (box_size * border))
    if error_correction == qrcode.constants.ERROR_CORRECT_L:
        thumbnail_logo_h = int(thumbnail_logo_h / 6)
    elif error_correction == qrcode.constants.ERROR_CORRECT_M:
        thumbnail_logo_h = int(thumbnail_logo_h / 5)
    else:
        thumbnail_logo_h = int(thumbnail_logo_h / 4)

    thumbnail_logo_h = thumbnail_logo_h - (thumbnail_logo_h % box_size)
    if (thumbnail_logo_h % (2 * box_size)) == 0:
        thumbnail_logo_h += box_size

    new_logo_size = thumbnail_logo_h, thumbnail_logo_h

    logo = Image.open(logo_file, "r")
    logo.thumbnail(new_logo_size, Image.LINEAR)
    return logo

if __name__ == "__main__":
    create_logo()

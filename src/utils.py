# 煩雑なツールをここに記述
import os
import base64


def img_encode(img_name):
    img_path = os.getcwd() + "/figures/" + img_name
    if os.path.exists(img_path):
        with open(img_path, "rb") as img:
            data = base64.b64encode(img.read())
    else:
        return "not found"

    return data.decode("utf-8")

from openalpr import Alpr
from os import getenv

alpr = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")

test = alpr.recognize_file(f"{getenv('WORKSPACE_PATH')}/test_run/1.jpg")

print(test["results"][0]["plate"])

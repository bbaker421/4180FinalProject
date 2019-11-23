import pycurl
from io import BytesIO

buffer = BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, '10.0.0.236:5000')
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()

body = buffer.getvalue()
print(body)
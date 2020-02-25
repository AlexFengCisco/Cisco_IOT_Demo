# coding=utf-8

'''

     needs pre-install pip install pyOpenSSL

    Generate self signed SSL key certificate with openSSL

    openssl genrsa -des3 -out server.key 1024
    openssl req -new -key server.key -out server.csr
    cp server.key server.key.org
    openssl rsa -in server.key.org -out server.key
    openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

    note: common name should be server ip address or domain name such as 127.0.0.1
          so far , chrome is not ready , safari and firefox(not verified) is good

          python requests is good

'''

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000, ssl_context=('server.crt', 'server.key'))

    #app.run(debug=True, host='127.0.0.1', port=5000)

    #app.run(debug=True, host='127.0.0.1', port=5000, ssl_context=('adhoc'))
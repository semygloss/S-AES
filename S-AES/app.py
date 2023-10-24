import flask
from flask import Flask, request, render_template

from s_ase import Decry, aes_multiple_encry, aes_multiple_decry, aes_CBC_encry, aes_CBC_decry
from s_ase import Encry

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/S_DES', methods=['GET', 'POST'])
def S_DES():
    message = ""
    plaintext = request.args.get('plaintext')
    print(plaintext)
    key = request.args.get('key')
    print(key)
    ciphertext = request.args.get('ciphertext')
    print(ciphertext)
    if key != '' and len(key) ==16:
        if plaintext != '' and ciphertext == '' and len(plaintext)>=16 and len(plaintext)<32:
            print('加密调用@@@@len:%d'%(len(plaintext)))
            get_ciphertext = Encry(plaintext, key)
            print(get_ciphertext)
            message = "完成明文加码！密文为:" + get_ciphertext
            return render_template('index.html', message=message)
        elif plaintext !='' and ciphertext=='' and len(plaintext)>=32 :
            print(f'CBC工作模式aes加密{len(plaintext)}')
            get_ciphertext=aes_CBC_encry(plaintext, key)
            print(get_ciphertext)
            message='完成CBC模式下的aes加密！密文为:'+get_ciphertext
            return render_template('index.html',message=message)
        elif ciphertext !='' and plaintext=='' and len(ciphertext)>=32:
            print('CBC工作模式下的aes解密')
            get_plaintext=aes_CBC_decry(ciphertext, key)
            print(get_plaintext)
            message='完成CBC模式下的aes解密！明文为:'+get_plaintext
            return render_template('index.html', message=message)
        elif ciphertext != '' and plaintext == '' and len(ciphertext)>=16 and len(ciphertext)<32:
            get_plaintext = Decry(ciphertext, key)
            message = "完成密文解码！明文为:" + get_plaintext
            return render_template('index.html', message=message)
        elif plaintext == '' and ciphertext == '':
            message = "必须输入明文或密文！"
            return render_template('index.html', message=message)
    if key == '':
        message = "密钥不能为空！"
        return render_template('index.html', message=message)
    if key !='' and len(key) != 16:
        if plaintext !='' and ciphertext == '':
            print('多重加密调用len:%d' % (len(key)))
            get_ciphertext=aes_multiple_encry(plaintext,key)
            print(get_ciphertext)
            message='完成多重S-AES明文加密！密文为:' + get_ciphertext
            return render_template('index.html',message=message)
        elif plaintext =='' and ciphertext !='':
            print('多重解密调用len:%d' %(len(key)))
            get_plaintext = aes_multiple_decry(ciphertext, key)
            print(get_plaintext)
            message = "完成多重S-AES密文解码！明文为:" + get_plaintext
            return render_template('index.html', message=message)
        elif plaintext =='' and ciphertext =='' :
            message = "必须输入明文或密文！"
            return render_template('index.html', message=message)


if __name__ == '__main__':
    app.run()
    print('run')

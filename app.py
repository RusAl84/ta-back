from flask import Flask, json, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os
import time
import convertQA as conv
import urllib.request
import process_nlp

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
ListOfMessages = []


@app.route('/')
def dafault_route():
    return 'API'


@app.route('/up')
def default():
    return '''
    <html>
    <body>
        <form action = "http://localhost:5000/uploadsa" method = "POST" enctype = "multipart/form-data">
            <input type = "file" name = "File" />
            <input type = "submit" value = "Submit" />
        </form>
    </body>
    </html>
    '''

@app.route('/uploads/<path:path>')
def send_photo(path):
    return send_from_directory('uploads', path)


@app.route('/uploadae', methods=['POST'])
@cross_origin()
def uploadae():
    for fname in request.files:
        f = request.files.get(fname)
        print(f)
        milliseconds = int(time.time() * 1000)
        filename = f"./uploads/{milliseconds}.json"
        # f.save('./uploads/%s' % secure_filename(fname))
        f.save(filename)
        text = conv.convertJsonMessages2text(filename)
    return text

# получение сообщений
@app.route("/get_pattern", methods=['POST'])
def get_pattern(id):
    msg = request.json
    print(msg)
    return process_nlp.get_pattern(msg['text'])
    



@app.route('/uploadsa', methods=['POST'])
def uploadsa():
    if request.method == 'POST':
        f = request.files['File']
        # filename = secure_filename(f.filename)
        milliseconds = int(time.time() * 1000)
        filename = f"./uploads/{milliseconds}.pcap"
        f.save(filename)
        # text = conv.convertJsonMessages2text(filename)
        # str1 = text
        from scan_detector import all_check
        str1 = all_check(filename)
        print(str1)
        str1 += "<br> <a href=""javascript:history.back()"">Назад</a>"
        return str1




# отправка сообщений
@app.route("/api/Messanger", methods=['POST'])
def SendMessage():
    msg = request.json
    print(msg)
    # messages.append({"UserName":"RusAl","MessageText":"Privet na sto let!!!","TimeStamp":"2021-03-05T18:23:10.932973Z"})
    ListOfMessages.append(msg)
    print(msg)
    msgtext = f"{msg['UserName']} <{msg['TimeStamp']}>: {msg['MessageText']}"
    print(
        f"Всего сообщений: {len(ListOfMessages)} Посланное сообщение: {msgtext}")
    return f"Сообщение отослано успешно. Всего сообщений: {len(ListOfMessages)} ", 200


# отправка сообщений
@app.route("/reverse", methods=['POST'])
def reverse():
    text = request.json
    print(text)
    text = str(text["text"])
    reverseText = ""
    for i in range(1, len(text) + 1):
        reverseText += text[-1 * i]
    return f"{reverseText}", 200


# получение сообщений
@app.route("/api/Messanger/<int:id>")
def GetMessage(id):
    print(id)
    if id >= 0 and id < len(ListOfMessages):
        print(ListOfMessages[id])
        return ListOfMessages[id], 200
    else:
        return "Not found", 400


if __name__ == '__main__':
    app.run(host="0.0.0.0")
app.run(host="0.0.0.0")

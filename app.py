from flask import Flask, json, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os
import time
import convertQA as conv
import urllib.request


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


# app.secret_key = "caircocoders-ednalan"

# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 900 * 1024 * 1024

# ALLOWED_EXTENSIONS = set(['json'])


# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/uploadae', methods=['POST'])
# def uploadae():
#     # check if the post request has the file part
#     if 'files[]' not in request.files:
#         resp = jsonify({'message': 'No file part in the request'})
#         resp.status_code = 400
#         return resp

#     files = request.files.getlist('files[]')

#     errors = {}
#     success = False

#     for file in files:
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             success = True
#         else:
#             errors[file.filename] = 'File type is not allowed'

#     if success and errors:
#         errors['message'] = 'File(s) successfully uploaded'
#         resp = jsonify(errors)
#         resp.status_code = 500
#         return resp
#     if success:
#         resp = jsonify({'message': 'Files successfully uploaded'})
#         resp.status_code = 201
#         return resp
#     else:
#         resp = jsonify(errors)
#         resp.status_code = 500
#         return resp


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
    # print(request)

    # if request.method == 'POST':
    #     f = request.files['File']
    #     # filename = secure_filename(f.filename)
    #     milliseconds = int(time.time() * 1000)
    #     filename = f"./uploads/{milliseconds}.json"
    #     f.save(filename)
    #     text = conv.convertJsonMessages2text(filename)
    #     str1 = text
    #     print(text)
    #     # from scan_detector import all_check
    #     # str1 = all_check('1.pcap')
    #     # print(str1)
    #     # str1 += "<br> <a href=""javascript:history.back()"">Назад</a>"
    #     return str1


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

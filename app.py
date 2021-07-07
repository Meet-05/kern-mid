
# import re
# import cloudinary
# import cloudinary.uploader
# import cloudinary.api
from flask import Flask, render_template, request, jsonify
import numpy as np
from test import Preprocess
from melodygenerator import MelodyGenerator
from flask import Flask, send_from_directory

app = Flask(__name__)


@app.route("/upload", methods=['POST', "GET"])
def upload_file():
    #   cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'),
    #     api_secret=os.getenv('API_SECRET'))
    upload_result = None
    if request.method == "GET":
        return render_template('index.html')

    if request.method == 'POST':
        print('-----')
        file_to_upload = request.files['file']
        file_to_upload.save(f'{file_to_upload.filename}')
        app.logger.info('%s file_to_upload', file_to_upload)
        mg = MelodyGenerator()
        obj = Preprocess()
        seed = obj.getString(file_to_upload.filename)
        print(f' in class -> {seed}')
        #seed2 = "67 _ 67 _ 67 _ _ 65 64 _ 64 _ 64 _ _"
        #seed = "67 _ _ _ _ _ 65 _ 64 _ 62 _ 60 _ _ _ 67 _ 67 _ 67 _ _ 65 64 _ 64 _ 64 _ _ 67 _ _ _ _ _ 65 _ 64 _ 62 _ 60 _ _ _ 67 _ 67 _ 67 _ _ 65 64 _ 64 _ 64 _ _"
        melody = mg.generate_melody(seed, 500, 64, 0.3)
        mg.save_melody(melody, file_name='midd.mid')
        print(type(mg))
        return send_from_directory('', filename='midd.mid', as_attachment=True)
        # if file_to_upload:
        #     #   upload_result = cloudinary.uploader.upload(file_to_upload)
        #     # app.logger.info(upload_result)
        #     upload_result = cloudinary.uploader.upload(file_to_upload)
        #     return jsonify(True)


# ===============================================================================================
if __name__ == '__main__':
    app.run(debug=True)

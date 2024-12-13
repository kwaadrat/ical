from flask import Flask, request, send_from_directory
import os
import location

app = Flask(__name__)

# Konfiguracja katalogu do przechowywania plików iCalendar
UPLOAD_FOLDER = 'ical'
ALLOWED_EXTENSIONS = {'ics'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/ical', methods=['POST'])  # Zmieniliśmy ścieżkę na '/ical'
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Wywołanie funkcji z location.py
            output_file = location.add_location(file_path)

            return send_from_directory(app.config['UPLOAD_FOLDER'], output_file, as_attachment=True)
    return '''
    <!doctype html>
    <title>upload new file</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(host='::', port=8080, debug=True)
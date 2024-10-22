from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
from location import add_location_to_ical
# ... (reszta kodu)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Wywołaj funkcję przetwarzania pliku
            output_file = "output.ics"
            add_location_to_ical(filepath, output_file)
            return send_file(output_file, as_attachment=True)
    return render_template('index.html')
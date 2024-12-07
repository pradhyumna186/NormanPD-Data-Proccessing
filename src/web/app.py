from flask import Flask, render_template, request, jsonify
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import io
import sys
import os
from pypdf import PdfReader
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core.project0 import fetchincidents, extractincidents, createdb, populatedb
from src.visualization.visualizations import visualize_data

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def process_pdf_data(pdf_data):
    try:
        pdf_file = io.BytesIO(pdf_data)
        pdf_reader = PdfReader(pdf_file)
        content = []
        for page in pdf_reader.pages:
            content.append(page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False))
        return '\n'.join(content)
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")

def convert_plot_to_base64(fig):
    img_bytes = io.BytesIO()
    fig.savefig(img_bytes, format='png', bbox_inches='tight', dpi=300)
    img_bytes.seek(0)
    return base64.b64encode(img_bytes.getvalue()).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_incidents():
    try:
        incident_data = None
        
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            pdf_data = file.read()
            incident_data = process_pdf_data(pdf_data)
        elif 'url' in request.form and request.form['url']:
            url = request.form['url']
            raw_data = fetchincidents(url)
            if isinstance(raw_data, bytes):
                incident_data = process_pdf_data(raw_data)
            else:
                incident_data = raw_data

        if not incident_data:
            return jsonify({'status': 'error', 'message': 'No data provided'})

        incidents = extractincidents(incident_data)
        if not incidents:
            return jsonify({'status': 'error', 'message': 'No incidents found in data'})

        db = createdb()
        populatedb(db, incidents)

        figs = visualize_data(incidents)
        plot_data = []
        for fig in figs:
            plot_data.append(convert_plot_to_base64(fig))
            plt.close(fig)

        db.close()

        return jsonify({
            'status': 'success',
            'message': f'Successfully processed {len(incidents)} incidents',
            'plots': plot_data
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
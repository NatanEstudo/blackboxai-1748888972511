#!/usr/bin/env python3
import os
from flask import Flask, request, jsonify, send_file
from PyPDF2 import PdfReader, PdfWriter
from googletrans import Translator
import os

translator = Translator()
from PyPDF2 import PdfReader, PdfWriter
from googletrans import Translator
import re
import time
import paramiko
import configparser
from datetime import datetime

class SwitchLogMonitor:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.error_patterns = self.config.get('settings', 'error_patterns').split(',')
        self.error_logs_dir = 'error_logs'
        os.makedirs(self.error_logs_dir, exist_ok=True)

    def connect_to_switch(self, switch_info):
        ip, port, username, password = switch_info.split(':')
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(ip, port=int(port), username=username, password=password)
            return client
        except Exception as e:
            print(f"Failed to connect to {ip}: {str(e)}")
            return None

    def get_switch_logs(self, ssh_client):
        stdin, stdout, stderr = ssh_client.exec_command('show logging')
        return stdout.read().decode('utf-8')

    def extract_errors(self, logs):
        errors = []
        for line in logs.split('\n'):
            if any(pattern.lower() in line.lower() for pattern in self.error_patterns):
                errors.append(line)
        return errors

    def save_errors(self, switch_name, errors):
        if not errors:
            return
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.error_logs_dir}/{switch_name}_errors_{timestamp}.log"
        with open(filename, 'w') as f:
            f.write('\n'.join(errors))
        print(f"Saved {len(errors)} errors to {filename}")

    def monitor_switches(self):
        while True:
            for switch_name, switch_info in self.config.items('switches'):
                print(f"Checking {switch_name}...")
                ssh_client = self.connect_to_switch(switch_info)
                if ssh_client:
                    logs = self.get_switch_logs(ssh_client)
                    errors = self.extract_errors(logs)
                    self.save_errors(switch_name, errors)
                    ssh_client.close()
            
            sleep_minutes = int(self.config.get('settings', 'poll_interval'))
            print(f"Waiting {sleep_minutes} minutes before next check...")
            time.sleep(sleep_minutes * 60)

# New route for PDF translation
app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate_pdf():
    if 'pdfFile' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['pdfFile']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Read the PDF file
    reader = PdfReader(file)
    writer = PdfWriter()

    # Extract text and translate
    for page in reader.pages:
        text = page.extract_text()
        translated_text = translator.translate(text, dest='pt').text
        # Create a new page with translated text
        writer.add_page(PdfWriter().add_blank_page())
        writer.pages[-1].insert_text(translated_text)

    # Save the translated PDF
    translated_pdf_path = 'translated.pdf'
    with open(translated_pdf_path, 'wb') as f:
        writer.write(f)

    return send_file(translated_pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

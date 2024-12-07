# -*- coding: utf-8 -*-
import urllib.request
import io
import re
import sqlite3
import os
from pypdf import PdfReader

def fetchincidents(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(request)
        pdf_data = response.read()
        
        pdf_file = io.BytesIO(pdf_data)
        pdf_reader = PdfReader(pdf_file)

        content = []
        for page in pdf_reader.pages:
            content.append(page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False))

        data = '\n'.join(content)
        return data
        
    except Exception as e:
        raise Exception(f"Error fetching PDF: {e}")

def extractincidents(data):
    if isinstance(data, bytes):
        try:
            pdf_file = io.BytesIO(data)
            pdf_reader = PdfReader(pdf_file)
            content = []
            for page in pdf_reader.pages:
                content.append(page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False))
            data = '\n'.join(content)
        except Exception as e:
            raise Exception(f"Error processing PDF data: {str(e)}")

    lines = data.split('\n')
    if len(lines) > 2:
        lines = lines[1:-1]  

    parsed_results = []
    for line in lines:
        line = line.strip()
        if line: 
            parsed_incident = parse_incident(line)
            if parsed_incident:
                parsed_results.append(parsed_incident)
    return parsed_results

def parse_incident(line):
    parts = re.split(r'\s{2,}', line.strip())

    if len(parts) < 5:
        return None  
    date_time = parts[0] 
    incident_number = parts[1]  
    location = parts[2]  
    nature = parts[3]  
    ori = parts[4] 
   
    return [date_time, incident_number, location, nature.strip(), ori.strip()]

def createdb():
    db_path = os.path.join('resources', 'normanpd.db')
    os.makedirs('resources', exist_ok=True) 

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
        )
    ''')
    conn.commit()

    return conn

def populatedb(conn, incidents):
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori) 
        VALUES (?, ?, ?, ?, ?)
    ''', incidents)
    conn.commit()
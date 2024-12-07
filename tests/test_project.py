import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.project0 import fetchincidents, extractincidents, createdb, populatedb
from src.visualization.visualizations import visualize_data
import sqlite3
from src.core.project0 import fetchincidents, extractincidents, createdb, populatedb
from src.visualization.visualizations import visualize_data

def test_fetch_incidents():
    # Test valid URL
    url = "https://www.normanok.gov/sites/default/files/documents/2024-12/2024-12-01_daily_incident_summary.pdf"
    data = fetchincidents(url)
    assert data is not None
    assert isinstance(data, (str, bytes))

def test_extract_incidents():
    # Test incident extraction
    sample_data = "12/1/2024 8:54  2024-00001  1234 Main St  Traffic Stop  OK0140200"
    incidents = extractincidents(sample_data)
    assert len(incidents) > 0
    assert len(incidents[0]) == 5  # Check all fields are present

def test_database_creation():
    # Test database creation
    db = createdb()
    assert isinstance(db, sqlite3.Connection)
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents'")
    assert cursor.fetchone() is not None
    db.close()

def test_database_population():
    # Test database population
    db = createdb()
    sample_incidents = [
        ["12/1/2024 8:54", "2024-00001", "1234 Main St", "Traffic Stop", "OK0140200"]
    ]
    populatedb(db, sample_incidents)
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM incidents")
    assert cursor.fetchone()[0] > 0
    db.close()

def test_visualization_generation():
    # Test visualization generation
    sample_incidents = [
        ["12/1/2024 8:54", "2024-00001", "1234 Main St", "Traffic Stop", "OK0140200"],
        ["12/1/2024 9:00", "2024-00002", "5678 Oak St", "Welfare Check", "OK0140200"]
    ]
    figs = visualize_data(sample_incidents)
    assert len(figs) == 3  # Should generate 3 visualizations
    assert all(hasattr(fig, 'savefig') for fig in figs)

def test_invalid_url():
    # Test invalid URL handling
    with pytest.raises(Exception):
        fetchincidents("https://invalid-url.com/nonexistent.pdf")

def test_empty_data():
    # Test empty data handling
    incidents = extractincidents("")
    assert len(incidents) == 0

def test_malformed_incident():
    # Test malformed incident data
    malformed_data = "Invalid Data Format"
    incidents = extractincidents(malformed_data)
    assert len(incidents) == 0
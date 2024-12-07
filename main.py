# -*- coding: utf-8 -*-

import argparse
import src.core.project0 as project0
from src.visualization.visualizations import visualize_data

def main(url):
    # Fetch incident data
    incident_data = project0.fetchincidents(url)

    # Extract incidents from the data
    incidents = project0.extractincidents(incident_data)

    # Create the database
    db = project0.createdb()

    # Populate the database with incident data
    project0.populatedb(db, incidents)

    # Generate visualizations
    visualize_data(incidents)

    # Close the database connection
    db.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
#!/usr/bin/env python3
"""Convert the flat jail list to nested structure for data-driven Jails class"""

import json
import re
from pathlib import Path
from collections import defaultdict

def generate_class_name(county_name: str) -> str:
    """Generate a valid Python class name from county name"""
    # Remove special characters and Parish/County suffixes
    clean_name = re.sub(r'\s+(Parish|County)$', '', county_name)
    clean_name = re.sub(r'[^a-zA-Z\s]', '', clean_name)
    # Convert to PascalCase and add County suffix
    words = clean_name.split()
    class_name = ''.join(word.capitalize() for word in words) + 'County'
    return class_name

def main():
    # Load the flat jail data
    data_file = Path('find_zuercher/zuercher_jails_latest.json')
    with data_file.open() as f:
        jails = json.load(f)
    
    # Group by state
    nested_data = defaultdict(dict)
    
    for jail in jails:
        state = jail['state_abbrev']
        county = jail['county']
        class_name = generate_class_name(county)
        
        nested_data[state][class_name] = {
            'jail_id': jail['jail_id'],
            'name': jail['jail_name'],
            'county': county,
            'url': jail['url']
        }
    
    # Write the nested structure
    output_file = Path('jails.json')
    with output_file.open('w') as f:
        json.dump(nested_data, f, indent=2, sort_keys=True)
    
    print(f"Created {output_file} with {len(nested_data)} states")
    for state, counties in nested_data.items():
        print(f"  {state}: {len(counties)} counties")

if __name__ == '__main__':
    main()

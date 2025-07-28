#!/usr/bin/env python3
"""
Script to update the Jails class in zuercherportal_api.py with missing jails from zuercher_jails_latest.json

This script:
1. Reads jail data from zuercher_jails_latest.json
2. Parses existing jails from zuercherportal_api.py
3. Identifies missing jails and generates proper Python class structures
4. Updates the API file with missing jails organized by state
5. Updates the README.md file with a collapsible table of all jails

Usage:
    python update_jails_from_json.py              # Full update (API + README)
    python update_jails_from_json.py --readme-only  # Update only README
"""

import json
import re
from pathlib import Path
from typing import Dict, List


class JailUpdater:
    """Updates the Jails class with missing jails from JSON data"""
    
    # State abbreviation to full name mapping
    STATE_NAMES = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
        'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
        'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
        'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
        'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
        'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
        'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
        'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
        'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
        'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia'
    }
    
    def __init__(self, json_file_path: str, api_file_path: str, readme_file_path: str | None = None):
        self.json_file_path = Path(json_file_path)
        self.api_file_path = Path(api_file_path)
        self.readme_file_path = Path(readme_file_path) if readme_file_path else self.api_file_path.parent / "README.md"
        self.jail_data: List[dict] = []
        self.existing_jails: set[str] = set()
        
    def load_json_data(self) -> None:
        """Load jail data from JSON file"""
        with open(self.json_file_path, 'r', encoding='utf-8') as f:
            self.jail_data = json.load(f)
        print(f"Loaded {len(self.jail_data)} jails from JSON file")
    
    def parse_existing_jails(self) -> None:
        """Parse existing jails from the API file"""
        with open(self.api_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all jail_id assignments in the file
        jail_id_pattern = r'jail_id\s*=\s*["\']([^"\']+)["\']'
        matches = re.findall(jail_id_pattern, content)
        self.existing_jails = set(matches)
        print(f"Found {len(self.existing_jails)} existing jails in API file")
    
    def generate_class_name(self, county: str) -> str:
        """Generate a class name from county name"""
        # Remove special characters and spaces, capitalize words
        clean_name = re.sub(r'[^a-zA-Z\s]', '', county)
        words = clean_name.split()
        class_name = ''.join(word.capitalize() for word in words) + 'County'
        return class_name
    
    def generate_state_class_name(self, state_abbrev: str) -> str:
        """Generate state class name from abbreviation"""
        return state_abbrev.upper()
    
    def organize_jails_by_state(self) -> Dict[str, List[dict]]:
        """Organize jails by state"""
        jails_by_state: Dict[str, List[dict]] = {}
        for jail in self.jail_data:
            state = jail['state_abbrev']
            if state not in jails_by_state:
                jails_by_state[state] = []
            jails_by_state[state].append(jail)
        return jails_by_state
    
    def find_missing_jails(self) -> Dict[str, List[dict]]:
        """Find jails that are missing from the API file"""
        missing_jails: Dict[str, List[dict]] = {}
        jails_by_state = self.organize_jails_by_state()
        
        for state, jails in jails_by_state.items():
            missing_jails[state] = []
            for jail in jails:
                if jail['jail_id'] not in self.existing_jails:
                    missing_jails[state].append(jail)
        
        # Remove states with no missing jails
        missing_jails = {k: v for k, v in missing_jails.items() if v}
        return missing_jails
    
    def generate_jail_class_code(self, jail: dict) -> str:
        """Generate the class code for a single jail"""
        class_name = self.generate_class_name(jail['county'])
        jail_name = jail['jail_name']
        jail_id = jail['jail_id']
        
        return f'''        class {class_name}(Jail):
            """{jail_name}"""

            jail_id = "{jail_id}"
            name = "{jail_name}"'''
    
    def generate_state_class_code(self, state_abbrev: str, jails: List[dict]) -> str:
        """Generate the class code for a state with its jails"""
        state_name = self.STATE_NAMES.get(state_abbrev, state_abbrev)
        class_name = self.generate_state_class_name(state_abbrev)
        
        # Generate jail classes
        jail_classes = []
        for jail in jails:
            jail_classes.append(self.generate_jail_class_code(jail))
        
        # Generate __str__ method
        jail_class_names = [self.generate_class_name(jail['county']) for jail in jails]
        str_method_jails = ', '.join([f'self.{name}.name' for name in jail_class_names])
        
        state_class = f'''    class {class_name}(object):
        """State of {state_name}"""

        name = "State of {state_name}"

{chr(10).join(jail_classes)}

        def __str__(self):
            """Return List of Known Counties"""
            return f"{state_abbrev}({str_method_jails})"'''
        
        return state_class
    
    def read_api_file(self) -> str:
        """Read the current API file content"""
        with open(self.api_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def find_jails_class_end(self, content: str) -> int:
        """Find the end of the Jails class"""
        # Look for the start of the next class (API class)
        api_class_match = re.search(r'^class API:', content, re.MULTILINE)
        if api_class_match:
            return api_class_match.start()
        
        # If API class not found, look for end of file
        return len(content)
    
    def update_api_file(self, missing_jails: Dict[str, List[dict]]) -> None:
        """Update the API file with missing jails"""
        if not missing_jails:
            print("No missing jails found. API file is up to date.")
            return
        
        content = self.read_api_file()
        
        # Find the insertion point (end of Jails class, before API class)
        jails_class_end = self.find_jails_class_end(content)
        
        # Generate new state classes
        new_state_classes = []
        for state_abbrev, jails in sorted(missing_jails.items()):
            state_class_code = self.generate_state_class_code(state_abbrev, jails)
            new_state_classes.append(state_class_code)
        
        # Insert new classes before the API class
        new_content = (
            content[:jails_class_end] + 
            '\n' + 
            '\n\n'.join(new_state_classes) + 
            '\n\n\n' +
            content[jails_class_end:]
        )
        
        # Write updated content
        with open(self.api_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Added {sum(len(jails) for jails in missing_jails.values())} jails across {len(missing_jails)} states")
        for state, jails in missing_jails.items():
            print(f"  {state}: {len(jails)} jails")
    
    def generate_readme_jail_table(self) -> str:
        """Generate the README jail table section"""
        jails_by_state = self.organize_jails_by_state()
        
        readme_content = """## Current Jails in our Database
Below are the jails we currently have in our database. Please feel free to raise issue or pull request to add additional jails.

"""
        
        for state_abbrev in sorted(jails_by_state.keys()):
            jails = sorted(jails_by_state[state_abbrev], key=lambda x: x['county'])
            state_name = self.STATE_NAMES.get(state_abbrev, state_abbrev)
            
            # Create collapsible section for each state
            readme_content += f"""<details>
<summary><strong>{state_name} ({len(jails)} jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
"""
            
            for jail in jails:
                county_class = self.generate_class_name(jail['county'])
                class_access = f"zuercherportal.Jails.{state_abbrev}.{county_class}()"
                readme_content += f"| {jail['county']} | {jail['jail_name']} | `{jail['jail_id']}` | `{class_access}` |\n"
            
            readme_content += "\n</details>\n\n"
        
        return readme_content
    
    def update_readme_file(self) -> None:
        """Update the README file with the current jail list"""
        # Read current README
        with open(self.readme_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the jail database section
        start_marker = "## Current Jails in our Database"
        start_index = content.find(start_marker)
        
        if start_index == -1:
            print("Warning: Could not find jail database section in README")
            return
        
        # Generate new jail table
        new_jail_section = self.generate_readme_jail_table()
        
        # Replace the old section with the new one
        new_content = content[:start_index] + new_jail_section
        
        # Write updated README
        with open(self.readme_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("README file updated with current jail list")
    
    def run(self) -> None:
        """Run the update process"""
        print("Starting jail update process...")
        
        # Load data
        self.load_json_data()
        self.parse_existing_jails()
        
        # Find missing jails
        missing_jails = self.find_missing_jails()
        
        if not missing_jails:
            print("No missing jails found. API file is up to date.")
            return
        
        print(f"\nFound missing jails in {len(missing_jails)} states:")
        for state, jails in missing_jails.items():
            print(f"  {state}: {len(jails)} jails")
        
        # Ask for confirmation
        response = input("\nDo you want to update the API file? (y/n): ")
        if response.lower() in ['y', 'yes']:
            self.update_api_file(missing_jails)
            print("API file updated successfully!")
            
            # Update README regardless of whether there were missing jails
            self.update_readme_file()
        else:
            print("Update cancelled.")
    
    def update_readme_only(self) -> None:
        """Update only the README file with current jail data"""
        print("Updating README file with current jail data...")
        self.load_json_data()
        self.update_readme_file()


def main():
    """Main function"""
    import sys
    
    # Set file paths
    json_file = "zuercher_jails_latest.json"
    api_file = "../zuercherportal_api.py"
    
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--readme-only":
        # Only update README
        updater = JailUpdater(json_file, api_file)
        updater.update_readme_only()
    else:
        # Full update process
        updater = JailUpdater(json_file, api_file)
        updater.run()


if __name__ == "__main__":
    main()

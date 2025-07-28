"""Data-driven Jails implementation to replace the massive class hierarchy"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional


class Jail:
    """Jail class with basic properties"""
    
    def __init__(self, jail_id: str, name: str, county: str = "", url: str = ""):
        self.jail_id = jail_id
        self.name = name
        self.county = county
        self.url = url
        self.system = "zuercherportal"
        self.is_public_api = True
        self.ignore_non_public_api = False
        self.ignore_non_zuercherportal = False

    def __str__(self) -> str:
        return f"{self.jail_id}"


class JailsDataDriven:
    """Data-driven Jails class that loads from JSON"""
    
    _data: Dict = {}
    _loaded = False
    
    @classmethod
    def _load_data(cls):
        """Load jail data from JSON file"""
        if cls._loaded:
            return
            
        data_file = Path(__file__).parent / "jails.json"
        try:
            with data_file.open('r', encoding='utf-8') as f:
                cls._data = json.load(f)
            cls._loaded = True
        except FileNotFoundError:
            print(f"Warning: {data_file} not found. Using empty jail database.")
            cls._data = {}
            cls._loaded = True
    
    @classmethod
    def get_jail(cls, state: str, county_class: str) -> Optional[Jail]:
        """Get a specific jail by state and county class name"""
        cls._load_data()
        
        state_data = cls._data.get(state, {})
        jail_data = state_data.get(county_class)
        
        if jail_data:
            return Jail(
                jail_id=jail_data["jail_id"],
                name=jail_data["name"],
                county=jail_data.get("county", ""),
                url=jail_data.get("url", "")
            )
        return None
    
    @classmethod 
    def get_states(cls) -> List[str]:
        """Get list of all available states"""
        cls._load_data()
        return list(cls._data.keys())
    
    @classmethod
    def get_counties(cls, state: str) -> List[str]:
        """Get list of county class names for a state"""
        cls._load_data()
        return list(cls._data.get(state, {}).keys())
    
    @classmethod
    def get_all_jails(cls) -> List[Jail]:
        """Get all jails as a flat list"""
        cls._load_data()
        jails = []
        
        for state, counties in cls._data.items():
            for county_class, jail_data in counties.items():
                jail = Jail(
                    jail_id=jail_data["jail_id"],
                    name=jail_data["name"], 
                    county=jail_data.get("county", ""),
                    url=jail_data.get("url", "")
                )
                jails.append(jail)
        
        return jails
    
    @classmethod
    def search_by_jail_id(cls, jail_id: str) -> Optional[Jail]:
        """Find a jail by its jail_id"""
        cls._load_data()
        
        for state, counties in cls._data.items():
            for county_class, jail_data in counties.items():
                if jail_data["jail_id"] == jail_id:
                    return Jail(
                        jail_id=jail_data["jail_id"],
                        name=jail_data["name"],
                        county=jail_data.get("county", ""),
                        url=jail_data.get("url", "")
                    )
        return None


def create_backward_compatible_jails():
    """
    Create backward-compatible Jails class that maintains the old API
    while using the data-driven approach under the hood.
    
    This allows existing code like Jails.AR.BentonCounty() to continue working.
    """
    
    # Load the data
    JailsDataDriven._load_data()
    
    # Create the main Jails class
    class Jails:
        """Backward-compatible Jails class with dynamically generated state classes"""
        pass
    
    # State name mapping for documentation
    STATE_NAMES = {
        'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'GA': 'Georgia',
        'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
        'KS': 'Kansas', 'LA': 'Louisiana', 'ME': 'Maine', 'MI': 'Michigan',
        'MN': 'Minnesota', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska',
        'NH': 'New Hampshire', 'NM': 'New Mexico', 'NC': 'North Carolina',
        'OH': 'Ohio', 'ND': 'North Dakota', 'OK': 'Oklahoma', 'OR': 'Oregon',
        'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee',
        'TX': 'Texas', 'VA': 'Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
    }
    
    # Dynamically create state classes
    for state_abbrev, counties in JailsDataDriven._data.items():
        state_name = STATE_NAMES.get(state_abbrev, state_abbrev)
        
        # Create state class with __str__ method
        def make_state_str(state_abbrev, counties):
            def __str__(self):
                county_names = [f"self.{county}" for county in counties.keys()]
                return f"{state_abbrev}({', '.join(county_names)})"
            return __str__
        
        state_attrs = {
            '__doc__': f"State of {state_name}",
            'name': f"State of {state_name}",
            '__str__': make_state_str(state_abbrev, counties)
        }
        
        # Create county classes for this state
        for county_class, jail_data in counties.items():
            jail_attrs = {
                '__doc__': jail_data["name"],
                'jail_id': jail_data["jail_id"],
                'name': jail_data["name"],
                'system': 'zuercherportal',
                'is_public_api': True,
                'ignore_non_public_api': False,
                'ignore_non_zuercherportal': False
            }
            
            # Create the jail class as a subclass of Jail
            jail_class = type(county_class, (Jail,), jail_attrs)
            
            # Override __new__ to return a proper instance
            def make_jail_new(jail_id, name, county, url):
                def __new__(cls):
                    return Jail(jail_id, name, county, url)
                return __new__
            
            jail_class.__new__ = make_jail_new(
                jail_data["jail_id"],
                jail_data["name"], 
                jail_data.get("county", ""),
                jail_data.get("url", "")
            )
            
            state_attrs[county_class] = jail_class
        
        # Create and attach the state class
        state_class = type(state_abbrev, (), state_attrs)
        setattr(Jails, state_abbrev, state_class)
    
    return Jails


# Example usage:
if __name__ == '__main__':
    # Test the simplified API
    print("=== Data-driven API ===")
    states = JailsDataDriven.get_states()
    print(f"Available states: {states[:5]}...")
    
    ar_counties = JailsDataDriven.get_counties('AR')
    print(f"Arkansas counties: {ar_counties}")
    
    benton_jail = JailsDataDriven.get_jail('AR', 'BentonCounty')
    if benton_jail:
        print(f"Benton County Jail: {benton_jail} ({benton_jail.name})")
    
    # Test backward compatibility  
    print("\n=== Backward Compatible API ===")
    Jails = create_backward_compatible_jails()
    
    # This should work exactly like the old API
    benton = Jails.AR.BentonCounty()
    print(f"Jails.AR.BentonCounty(): {benton} ({benton.name})")
    
    print(f"Jails.AR: {Jails.AR()}")

# zuercherportal_api
 
![PyPI - Version](https://img.shields.io/pypi/v/zuercherportal_api) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zuercherportal_api)
![PyPI - License](https://img.shields.io/pypi/l/zuercherportal_api)

## Install
```python

pip install zuercherportal_api

```

## Usage
Manually Supplied Jail Prefix:
```python
import zuercherportal_api as zuercherportal

jail_api = zuercherportal.API(jail_id="benton-so-ar")
inmate_data = jail_api.inmate_search()
```

Using a Jail that is in our Database:
```python
import zuercherportal_api as zuercherportal
jail_api = zuercherportal.API(jail_id=zuercherportal.Jails.AR.BENTON_COUNTY)
inmate_data = jail_api.inmate_search()
```

Filter The Results:
```python
import zuercherportal_api as zuercherportal
jail_api = zuercherportal.API(jail_id=zuercherportal.Jails.AR.BENTON_COUNTY)
inmate_data = jail_api.inmate_search(
    inmate_name="",
    race="all",
    sex="all",
    cell_block="all",
    helf_for_agency="any",
    in_custody_date="",
    records_per_page=50,
    record_start=0,
    sort_by_column="name",
    sort_descending=False,
)
```

## Current Jails in our Database
Below are the jails we currently have in our database. Please feel free to raise issue or pull request to add additional jails.

- State of Arkansas
    - Benton County Jail
    - Pulaski County Jail
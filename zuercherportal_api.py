"""Inmate Search API"""

from dataclasses import dataclass
import sys
import json
import requests
from loguru import logger
from dataclass_wizard import fromdict, asdict


@dataclass
class Inmate:
    """Inmate Data"""
    name: str
    race: str
    sex: str
    cell_block: str
    arrest_date: str
    held_for_agency: str
    mugshot: str
    dob: str
    hold_reasons: str
    is_juvenile: bool
    release_date: str

@dataclass
class ZuercherportalResponse:
    """API Response Data Class"""
    total_record_count: int
    records: list["Inmate"]

class Jails:
    """List of Known Zuercher Portal Jails by State"""

    class AR:
        """State of Arkansas"""

        BENTON_COUNTY = "benton-so-ar"
        PULASKI_COUNTY = "pulaski-so-ar"


class API:
    """Inmate Search API Functions"""

    def __init__(self, jail_id: str, log_level: str = "INFO", return_object: bool = False) -> None:
        self.jail_id = jail_id
        self.api_url = f"https://{jail_id}.zuercherportal.com/api/portal/inmates/load"
        self.log_level = log_level
        self.return_object = return_object
        logger.remove()
        logger.add(sys.stderr, level=log_level)
        logger.info(f"API Initialized with jail_id {jail_id} and log level {log_level}")

    def inmate_search(
        self,
        inmate_name: str = "",
        race: str = "all",
        sex: str = "all",
        cell_block: str = "all",
        helf_for_agency: str = "any",
        in_custody_date: str = "",
        records_per_page: int = 50,
        record_start: int = 0,
        sort_by_column: str = "name",
        sort_descending: bool = False,
    ) -> json:
        """Search Inmates"""
        logger.trace("Start API.search")
        try:
            logger.trace("try")
            response = requests.post(
                url=self.api_url,
                headers={
                    "Content-Type": "application/json; charset=utf-8",
                },
                data=json.dumps(
                    {
                        "cell_block": cell_block,
                        "held_for_agency": helf_for_agency,
                        "in_custody": in_custody_date,
                        "paging": {"count": records_per_page, "start": record_start},
                        "sorting": {
                            "sort_by_column_tag": sort_by_column,
                            "sort_descending": sort_descending,
                        },
                        "sex": sex,
                        "name": inmate_name,
                        "race": race,
                    }
                ),
                timeout=20,
            )
            logger.trace("POST Request Complete")
            logger.debug(f"Response Code: {response.status_code}")
            logger.debug(response.text)
            data = response.json()
            logger.success(f"Total Record Count {data['total_record_count']}")
            logger.trace("Fixing to Return Data")
            if self.return_object:
                data = fromdict(ZuercherportalResponse, data)
            return data
        except requests.exceptions.RequestException:
            logger.trace("Raised Exception")
            logger.exception("Inmate Search Failed")

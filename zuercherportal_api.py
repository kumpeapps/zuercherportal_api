"""Inmate Search API"""

from dataclasses import dataclass
from warnings import warn
import sys
import json
import requests
from loguru import logger


@dataclass
class Inmate(object):
    """Inmate Data"""

    def __init__(
        self,
        name: str,
        race: str,
        sex: str,
        cell_block: str,
        arrest_date: str,
        held_for_agency: str,
        mugshot: str,
        dob: str,
        hold_reasons: str,
        is_juvenile: bool,
        release_date: str,
        jail: str = "",
    ):
        """Initialize New Inmate"""
        self.name = name
        self.race = race
        self.sex = sex
        self.cell_block = cell_block
        self.arrest_date = arrest_date
        self.held_for_agency = held_for_agency
        self.mugshot = mugshot
        self.dob = dob
        self.hold_reasons = hold_reasons
        self.is_juvenile = is_juvenile
        self.release_date = release_date
        self.jail = jail

    def __str__(self):
        """String Value of Inmate"""
        return (
            "Inmate("
            f"name={self.name},"
            f"race={self.race},"
            f"sex={self.sex},"
            f"cell_block={self.cell_block},"
            f"arrest_date={self.arrest_date},"
            f"helf_for_agency={self.held_for_agency},"
            f"mugshot={self.mugshot},"
            f"dob={self.dob},"
            f"hold_reasons={self.dob},"
            f"is_juvenile={self.is_juvenile},"
            f"release_date={self.release_date},"
            f"jail={self.jail}"
            ")"
        )

    @classmethod
    def fromdict(cls, dictionary):
        """Init From Dictionary"""
        return cls(**dictionary)


@dataclass
class Inmates(object):
    """Inmates"""

    def __init__(self, records: list["Inmate"]):
        """Initialize Inmates"""
        if not isinstance(records[0], Inmate):
            formated_records = []
            for record in records:
                formated_records.append(Inmate.fromdict(record))
            self._records = formated_records
        else:
            self._records = records

    @property
    def inmates(self):
        """inmates property"""
        return self._records

    @property
    def inmate_names(self):
        """Return list of only inmate names"""
        return [inmate.name for inmate in self._records]

    def __contains__(self, name: str):
        return name in self.inmate_names

    @inmates.setter
    def inmates(self, inmates: list["Inmate"]):
        """Set Inmates Property"""
        self._records = inmates

    def add_inmates(self, records: list["Inmate"], jail_id: str = ""):
        """Add Inmates"""
        if not isinstance(records[0], Inmate):
            formated_records = []
            for record in records:
                formated_records.append(Inmate.fromdict(record))
        else:
            formated_records = records
        for inmate in formated_records:
            inmate.jail = jail_id
        self._records += records

    def set_jail(self, jail_id: str):
        """Set Jail ID for all records with no jail listed"""
        inmates = self._records
        for inmate in inmates:
            if inmate.jail == "":
                inmate.jail = str(jail_id)
        self._records = inmates

    def update_jail(self, jail_id: str):
        """Set Jail ID for all records"""
        inmates = self._records
        for inmate in inmates:
            inmate.jail = jail_id
        self._records = inmates

    def __len__(self):
        return len(self._records)

    def __iadd__(self, other):
        self._records += other._records

    @classmethod
    def fromdict(cls, inmates):
        """Init from Dict"""
        records = inmates["records"]
        formated_records = []
        for record in records:
            formated_records.append(Inmate.fromdict(record))
        return cls(formated_records)


@dataclass
class ZuercherportalResponse(Inmates):
    """API Response Data Class"""

    def __init__(self, total_record_count: int, records: list["Inmate"]):
        """Init ZuercherportalResponse"""
        super().__init__(records)
        self.records = self._records
        self.total_record_count = total_record_count

    @classmethod
    def fromdict(cls, inmates):
        """Init From Dict"""
        total_record_count = inmates["total_record_count"]
        records = inmates["records"]
        formated_records = []
        for record in records:
            formated_records.append(Inmate.fromdict(record))
        return cls(total_record_count, formated_records)


class Jail(object):
    """Jail"""

    jail_id = ""
    name = jail_id
    system = "zuercherportal"
    is_public_api = True
    ignore_non_public_api = False
    ignore_non_zuercherportal = False

    def __str__(self) -> str:
        if not self.is_public_api and not self.ignore_non_public_api:
            warn(
                (
                    f"{self.name} has been flagged as not a public API"
                    "and may not function properly!"
                ),
                Warning,
            )
        if self.system != "zuercherportal" and not self.ignore_non_zuercherportal:
            warn(
                (
                    f"{self.name} has been flagged as not Zuercher Portal"
                    "and will not work with zuercherportal_api!"
                ),
                Warning,
            )

        return f"{self.jail_id}"


class Jails(object):
    """List of Known Zuercher Portal Jails by State"""

    class AR(object):
        """State of Arkansas"""

        name = "State of Arkansas"

        class BentonCounty(Jail):
            """Benton County Jail"""

            jail_id = "benton-so-ar"
            name = "Benton County Jail"

        class PulaskiCounty(Jail):
            """Pulaski County Jail"""

            jail_id = "pulaski-so-ar"
            name = "Pulaski County Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"AR({self.BentonCounty.name}, {self.PulaskiCounty.name})"


class API:
    """Inmate Search API Functions"""

    def __init__(
        self, jail: Jail | str, log_level: str = "INFO", return_object: bool = True
    ) -> None:
        if isinstance(jail, Jail):
            self.__jail_id = jail.jail_id
            self.__jail = jail
            if self.__jail.system != "zuercherportal":
                raise ConnectionRefusedError(
                    """We show this jail does not use Zuercher Portal 
                    and can not be queried with zuercherportal_api"""
                )
        else:
            self.__jail_id = jail
        self.__api_url = (
            f"https://{self.__jail_id}.zuercherportal.com/api/portal/inmates/load"
        )
        self.__log_level = log_level
        self.return_object = return_object
        logger.remove()
        logger.add(sys.stderr, level=self.__log_level)
        logger.info(
            f"API Initialized with jail_id {self.__jail_id} and log level {self.__log_level}"
        )

    @property
    def log_level(self):
        """log_level property"""
        return self.__log_level

    @log_level.setter
    def log_level(self, level):
        """Update Log Level"""
        self.__log_level = level
        logger.remove()
        logger.add(sys.stderr, level=self.__log_level)
        logger.info(
            f"API Re-Initialized with jail_id {self.__jail_id} and log level {self.__log_level}"
        )

    @property
    def jail(self):
        """Return jail_id"""
        return self.__jail_id

    @jail.setter
    def jail_id(self, jail: Jail | str):
        """Set jail ID and update api_url"""
        if isinstance(jail, Jail):
            self.__jail_id = jail.jail_id
            self.jail = jail
        else:
            self.__jail_id = jail
        self.__api_url = (
            f"https://{self.__jail_id}.zuercherportal.com/api/portal/inmates/load"
        )
        logger.info(
            f"API Re-Initialized with jail_id {self.__jail_id} and log level {self.__log_level}"
        )

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
    ):
        """Search Inmates"""
        logger.trace("Start API.search")
        try:
            logger.trace("try")
            response = requests.post(
                url=self.__api_url,
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
                data = ZuercherportalResponse.fromdict(data)
            return data
        except requests.exceptions.RequestException:
            logger.trace("Raised Exception")
            logger.exception("Inmate Search Failed")

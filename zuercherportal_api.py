"""Inmate Search API"""

import json
import hashlib
from functools import lru_cache
from dataclasses import dataclass
from warnings import warn
import sys
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
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
            f"hold_reasons={self.hold_reasons},"
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
        # Handle empty records list
        if not records:
            self._records = []
        elif not isinstance(records[0], Inmate):
            # Use list comprehension for better performance
            self._records = [Inmate.fromdict(record) for record in records]
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

    def set_inmates(self, inmates: list["Inmate"]):
        """Set Inmates Property"""
        self._records = inmates

    def add_inmates(self, records: list["Inmate"], jail_id: str = ""):
        """Add Inmates"""
        if not records:  # Handle empty records
            return
            
        if not isinstance(records[0], Inmate):
            formated_records = [Inmate.fromdict(record) for record in records]
        else:
            formated_records = records
            
        # Set jail_id for all new inmates
        for inmate in formated_records:
            inmate.jail = jail_id
        self._records.extend(formated_records)  # Use formated_records, not records

    def set_jail(self, jail_id: str):
        """Set Jail ID for all records with no jail listed"""
        for inmate in self._records:
            if inmate.jail == "":
                inmate.jail = str(jail_id)

    def update_jail(self, jail_id: str):
        """Set Jail ID for all records"""
        for inmate in self._records:
            inmate.jail = jail_id

    def __len__(self):
        return len(self._records)

    def __iadd__(self, other):
        self._records.extend(other._records)  # Use extend instead of +=
        return self
        return self

    @classmethod
    def fromdict(cls, inmates):
        """Init from Dict"""
        records = inmates["records"]
        # Use list comprehension for better performance
        formated_records = [Inmate.fromdict(record) for record in records]
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
        # Use list comprehension for better performance
        formated_records = [Inmate.fromdict(record) for record in records]
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



    class CA(object):
        """State of California"""

        name = "State of California"

        class SutterCounty(Jail):
            """Sutter County CA Jail"""

            jail_id = "sutter-so-ca"
            name = "Sutter County CA Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"CA(self.SutterCounty.name)"

    class CO(object):
        """State of Colorado"""

        name = "State of Colorado"

        class GilpinCounty(Jail):
            """Gilpin County CO Jail"""

            jail_id = "gilpin-so-co"
            name = "Gilpin County CO Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"CO(self.GilpinCounty.name)"

    class GA(object):
        """State of Georgia"""

        name = "State of Georgia"

        class CatoosaCounty(Jail):
            """Catoosa County GA Jail"""

            jail_id = "catoosa-so-ga"
            name = "Catoosa County GA Jail"
        class DouglasCounty(Jail):
            """Douglas County GA Jail"""

            jail_id = "douglas-so-ga"
            name = "Douglas County GA Jail"
        class FloydCounty(Jail):
            """Floyd County GA Jail"""

            jail_id = "floyd-so-ga"
            name = "Floyd County GA Jail"
        class HoustonCounty(Jail):
            """Houston County GA Jail"""

            jail_id = "houston-so-ga"
            name = "Houston County GA Jail"
        class LumpkinCounty(Jail):
            """Lumpkin County GA Jail"""

            jail_id = "lumpkin-so-ga"
            name = "Lumpkin County GA Jail"
        class ToombsCounty(Jail):
            """Toombs County GA Jail"""

            jail_id = "toombs-so-ga"
            name = "Toombs County GA Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"GA(self.CatoosaCounty.name, self.DouglasCounty.name, self.FloydCounty.name, self.HoustonCounty.name, self.LumpkinCounty.name, self.ToombsCounty.name)"

    class IA(object):
        """State of Iowa"""

        name = "State of Iowa"

        class ClintonCounty(Jail):
            """Clinton County IA Jail"""

            jail_id = "clinton-so-ia"
            name = "Clinton County IA Jail"
        class MarshallCounty(Jail):
            """Marshall County IA Jail"""

            jail_id = "marshall-so-ia"
            name = "Marshall County IA Jail"
        class PottawattamieCounty(Jail):
            """Pottawattamie County IA Jail"""

            jail_id = "pottawattamie-so-ia"
            name = "Pottawattamie County IA Jail"
        class PoweshiekCounty(Jail):
            """Poweshiek County IA Jail"""

            jail_id = "poweshiek-so-ia"
            name = "Poweshiek County IA Jail"
        class WapelloCounty(Jail):
            """Wapello County IA Jail"""

            jail_id = "wapello-so-ia"
            name = "Wapello County IA Jail"
        class WinneshiekCounty(Jail):
            """Winneshiek County IA Jail"""

            jail_id = "winneshiek-so-ia"
            name = "Winneshiek County IA Jail"
        class WebsterCounty(Jail):
            """Webster County IA Jail"""

            jail_id = "webster-so-ia"
            name = "Webster County IA Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"IA(self.ClintonCounty.name, self.MarshallCounty.name, self.PottawattamieCounty.name, self.PoweshiekCounty.name, self.WapelloCounty.name, self.WinneshiekCounty.name, self.WebsterCounty.name)"

    class ID(object):
        """State of Idaho"""

        name = "State of Idaho"

        class ClearwaterCounty(Jail):
            """Clearwater County ID Jail"""

            jail_id = "clearwater-so-id"
            name = "Clearwater County ID Jail"
        class WashingtonCounty(Jail):
            """Washington County ID Jail"""

            jail_id = "washington-so-id"
            name = "Washington County ID Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"ID(self.ClearwaterCounty.name, self.WashingtonCounty.name)"

    class IL(object):
        """State of Illinois"""

        name = "State of Illinois"

        class IroquoisCounty(Jail):
            """Iroquois County IL Jail"""

            jail_id = "iroquois-so-il"
            name = "Iroquois County IL Jail"
        class OgleCounty(Jail):
            """Ogle County IL Jail"""

            jail_id = "ogle-so-il"
            name = "Ogle County IL Jail"
        class WhitesideCounty(Jail):
            """Whiteside County IL Jail"""

            jail_id = "whiteside-so-il"
            name = "Whiteside County IL Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"IL(self.IroquoisCounty.name, self.OgleCounty.name, self.WhitesideCounty.name)"

    class IN(object):
        """State of Indiana"""

        name = "State of Indiana"

        class MarshallCounty(Jail):
            """Marshall County IN Jail"""

            jail_id = "marshall-so-in"
            name = "Marshall County IN Jail"
        class WayneCounty(Jail):
            """Wayne County IN Jail"""

            jail_id = "wayne-so-in"
            name = "Wayne County IN Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"IN(self.MarshallCounty.name, self.WayneCounty.name)"

    class KS(object):
        """State of Kansas"""

        name = "State of Kansas"

        class AtchisonCounty(Jail):
            """Atchison County KS Jail"""

            jail_id = "atchison-so-ks"
            name = "Atchison County KS Jail"
        class LeavenworthCounty(Jail):
            """Leavenworth County KS Jail"""

            jail_id = "leavenworth-so-ks"
            name = "Leavenworth County KS Jail"
        class LinnCounty(Jail):
            """Linn County KS Jail"""

            jail_id = "linn-so-ks"
            name = "Linn County KS Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"KS(self.AtchisonCounty.name, self.LeavenworthCounty.name, self.LinnCounty.name)"

    class LA(object):
        """State of Louisiana"""

        name = "State of Louisiana"

        class AcadiaParishCounty(Jail):
            """Acadia Parish County LA Jail"""

            jail_id = "acadia-so-la"
            name = "Acadia Parish County LA Jail"
        class AssumptionParishCounty(Jail):
            """Assumption Parish County LA Jail"""

            jail_id = "assumption-so-la"
            name = "Assumption Parish County LA Jail"
        class BienvilleParishCounty(Jail):
            """Bienville Parish County LA Jail"""

            jail_id = "bienville-so-la"
            name = "Bienville Parish County LA Jail"
        class JacksonParishCounty(Jail):
            """Jackson Parish County LA Jail"""

            jail_id = "jackson-so-la"
            name = "Jackson Parish County LA Jail"
        class LafourcheParishCounty(Jail):
            """Lafourche Parish County LA Jail"""

            jail_id = "lafourche-so-la"
            name = "Lafourche Parish County LA Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"LA(self.AcadiaParishCounty.name, self.AssumptionParishCounty.name, self.BienvilleParishCounty.name, self.JacksonParishCounty.name, self.LafourcheParishCounty.name)"

    class ME(object):
        """State of Maine"""

        name = "State of Maine"

        class AndroscogginCounty(Jail):
            """Androscoggin County ME Jail"""

            jail_id = "androscoggin-so-me"
            name = "Androscoggin County ME Jail"
        class FranklinCounty(Jail):
            """Franklin County ME Jail"""

            jail_id = "franklin-so-me"
            name = "Franklin County ME Jail"
        class LincolnCounty(Jail):
            """Lincoln County ME Jail"""

            jail_id = "lincoln-so-me"
            name = "Lincoln County ME Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"ME(self.AndroscogginCounty.name, self.FranklinCounty.name, self.LincolnCounty.name)"

    class MI(object):
        """State of Michigan"""

        name = "State of Michigan"

        class MonroeCounty(Jail):
            """Monroe County MI Jail"""

            jail_id = "monroe-so-mi"
            name = "Monroe County MI Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"MI(self.MonroeCounty.name)"

    class MN(object):
        """State of Minnesota"""

        name = "State of Minnesota"

        class PineCounty(Jail):
            """Pine County MN Jail"""

            jail_id = "pine-so-mn"
            name = "Pine County MN Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"MN(self.PineCounty.name)"

    class MO(object):
        """State of Missouri"""

        name = "State of Missouri"

        class BatesCounty(Jail):
            """Bates County MO Jail"""

            jail_id = "bates-so-mo"
            name = "Bates County MO Jail"
        class JacksonCounty(Jail):
            """Jackson County MO Jail"""

            jail_id = "jackson-so-mo"
            name = "Jackson County MO Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"MO(self.BatesCounty.name, self.JacksonCounty.name)"

    class MT(object):
        """State of Montana"""

        name = "State of Montana"

        class BroadwaterCounty(Jail):
            """Broadwater County MT Jail"""

            jail_id = "broadwater-so-mt"
            name = "Broadwater County MT Jail"
        class ChouteauCounty(Jail):
            """Chouteau County MT Jail"""

            jail_id = "chouteau-so-mt"
            name = "Chouteau County MT Jail"
        class CarbonCounty(Jail):
            """Carbon County MT Jail"""

            jail_id = "carbon-so-mt"
            name = "Carbon County MT Jail"
        class JeffersonCounty(Jail):
            """Jefferson County MT Jail"""

            jail_id = "jefferson-so-mt"
            name = "Jefferson County MT Jail"
        class GallatinCounty(Jail):
            """Gallatin County MT Jail"""

            jail_id = "gallatin-so-mt"
            name = "Gallatin County MT Jail"
        class MadisonCounty(Jail):
            """Madison County MT Jail"""

            jail_id = "madison-so-mt"
            name = "Madison County MT Jail"
        class MeagherCounty(Jail):
            """Meagher County MT Jail"""

            jail_id = "meagher-so-mt"
            name = "Meagher County MT Jail"
        class RosebudCounty(Jail):
            """Rosebud County MT Jail"""

            jail_id = "rosebud-so-mt"
            name = "Rosebud County MT Jail"
        class RooseveltCounty(Jail):
            """Roosevelt County MT Jail"""

            jail_id = "roosevelt-so-mt"
            name = "Roosevelt County MT Jail"
        class RavalliCounty(Jail):
            """Ravalli County MT Jail"""

            jail_id = "ravalli-so-mt"
            name = "Ravalli County MT Jail"
        class ValleyCounty(Jail):
            """Valley County MT Jail"""

            jail_id = "valley-so-mt"
            name = "Valley County MT Jail"
        class StillwaterCounty(Jail):
            """Stillwater County MT Jail"""

            jail_id = "stillwater-so-mt"
            name = "Stillwater County MT Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"MT(self.BroadwaterCounty.name, self.ChouteauCounty.name, self.CarbonCounty.name, self.JeffersonCounty.name, self.GallatinCounty.name, self.MadisonCounty.name, self.MeagherCounty.name, self.RosebudCounty.name, self.RooseveltCounty.name, self.RavalliCounty.name, self.ValleyCounty.name, self.StillwaterCounty.name)"

    class NC(object):
        """State of North Carolina"""

        name = "State of North Carolina"

        class BrunswickCounty(Jail):
            """Brunswick County NC Jail"""

            jail_id = "brunswick-so-nc"
            name = "Brunswick County NC Jail"
        class DavieCounty(Jail):
            """Davie County NC Jail"""

            jail_id = "davie-so-nc"
            name = "Davie County NC Jail"
        class HokeCounty(Jail):
            """Hoke County NC Jail"""

            jail_id = "hoke-so-nc"
            name = "Hoke County NC Jail"
        class PenderCounty(Jail):
            """Pender County NC Jail"""

            jail_id = "pender-so-nc"
            name = "Pender County NC Jail"
        class RutherfordCounty(Jail):
            """Rutherford County NC Jail"""

            jail_id = "rutherford-so-nc"
            name = "Rutherford County NC Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"NC(self.BrunswickCounty.name, self.DavieCounty.name, self.HokeCounty.name, self.PenderCounty.name, self.RutherfordCounty.name)"

    class ND(object):
        """State of North Dakota"""

        name = "State of North Dakota"

        class WilliamsCounty(Jail):
            """Williams County ND Jail"""

            jail_id = "williams-so-nd"
            name = "Williams County ND Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"ND(self.WilliamsCounty.name)"

    class NE(object):
        """State of Nebraska"""

        name = "State of Nebraska"

        class JohnsonCounty(Jail):
            """Johnson County NE Jail"""

            jail_id = "johnson-so-ne"
            name = "Johnson County NE Jail"
        class PerkinsCounty(Jail):
            """Perkins County NE Jail"""

            jail_id = "perkins-so-ne"
            name = "Perkins County NE Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"NE(self.JohnsonCounty.name, self.PerkinsCounty.name)"

    class NH(object):
        """State of New Hampshire"""

        name = "State of New Hampshire"

        class RockinghamCounty(Jail):
            """Rockingham County NH Jail"""

            jail_id = "rockingham-so-nh"
            name = "Rockingham County NH Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"NH(self.RockinghamCounty.name)"

    class NM(object):
        """State of New Mexico"""

        name = "State of New Mexico"

        class HidalgoCounty(Jail):
            """Hidalgo County NM Jail"""

            jail_id = "hidalgo-so-nm"
            name = "Hidalgo County NM Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"NM(self.HidalgoCounty.name)"

    class OH(object):
        """State of Ohio"""

        name = "State of Ohio"

        class AshlandCounty(Jail):
            """Ashland County OH Jail"""

            jail_id = "ashland-so-oh"
            name = "Ashland County OH Jail"
        class AthensCounty(Jail):
            """Athens County OH Jail"""

            jail_id = "athens-so-oh"
            name = "Athens County OH Jail"
        class FayetteCounty(Jail):
            """Fayette County OH Jail"""

            jail_id = "fayette-so-oh"
            name = "Fayette County OH Jail"
        class MarionCounty(Jail):
            """Marion County OH Jail"""

            jail_id = "marion-so-oh"
            name = "Marion County OH Jail"
        class MedinaCounty(Jail):
            """Medina County OH Jail"""

            jail_id = "medina-so-oh"
            name = "Medina County OH Jail"
        class PauldingCounty(Jail):
            """Paulding County OH Jail"""

            jail_id = "paulding-so-oh"
            name = "Paulding County OH Jail"
        class PickawayCounty(Jail):
            """Pickaway County OH Jail"""

            jail_id = "pickaway-so-oh"
            name = "Pickaway County OH Jail"
        class PikeCounty(Jail):
            """Pike County OH Jail"""

            jail_id = "pike-so-oh"
            name = "Pike County OH Jail"
        class PrebleCounty(Jail):
            """Preble County OH Jail"""

            jail_id = "preble-so-oh"
            name = "Preble County OH Jail"
        class RossCounty(Jail):
            """Ross County OH Jail"""

            jail_id = "ross-so-oh"
            name = "Ross County OH Jail"
        class SciotoCounty(Jail):
            """Scioto County OH Jail"""

            jail_id = "scioto-so-oh"
            name = "Scioto County OH Jail"
        class ShelbyCounty(Jail):
            """Shelby County OH Jail"""

            jail_id = "shelby-so-oh"
            name = "Shelby County OH Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"OH(self.AshlandCounty.name, self.AthensCounty.name, self.FayetteCounty.name, self.MarionCounty.name, self.MedinaCounty.name, self.PauldingCounty.name, self.PickawayCounty.name, self.PikeCounty.name, self.PrebleCounty.name, self.RossCounty.name, self.SciotoCounty.name, self.ShelbyCounty.name)"

    class OK(object):
        """State of Oklahoma"""

        name = "State of Oklahoma"

        class ClevelandCounty(Jail):
            """Cleveland County OK Jail"""

            jail_id = "cleveland-so-ok"
            name = "Cleveland County OK Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"OK(self.ClevelandCounty.name)"

    class OR(object):
        """State of Oregon"""

        name = "State of Oregon"

        class ClatsopCounty(Jail):
            """Clatsop County OR Jail"""

            jail_id = "clatsop-so-or"
            name = "Clatsop County OR Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"OR(self.ClatsopCounty.name)"

    class SC(object):
        """State of South Carolina"""

        name = "State of South Carolina"

        class CherokeeCounty(Jail):
            """Cherokee County SC Jail"""

            jail_id = "cherokee-so-sc"
            name = "Cherokee County SC Jail"
        class ColletonCounty(Jail):
            """Colleton County SC Jail"""

            jail_id = "colleton-so-sc"
            name = "Colleton County SC Jail"
        class KershawCounty(Jail):
            """Kershaw County SC Jail"""

            jail_id = "kershaw-so-sc"
            name = "Kershaw County SC Jail"
        class OconeeCounty(Jail):
            """Oconee County SC Jail"""

            jail_id = "oconee-so-sc"
            name = "Oconee County SC Jail"
        class AndersonCounty(Jail):
            """Anderson County SC Jail"""

            jail_id = "anderson-so-sc"
            name = "Anderson County SC Jail"
        class PickensCounty(Jail):
            """Pickens County SC Jail"""

            jail_id = "pickens-so-sc"
            name = "Pickens County SC Jail"
        class UnionCounty(Jail):
            """Union County SC Jail"""

            jail_id = "union-so-sc"
            name = "Union County SC Jail"
        class WilliamsburgCounty(Jail):
            """Williamsburg County SC Jail"""

            jail_id = "williamsburg-so-sc"
            name = "Williamsburg County SC Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"SC(self.CherokeeCounty.name, self.ColletonCounty.name, self.KershawCounty.name, self.OconeeCounty.name, self.AndersonCounty.name, self.PickensCounty.name, self.UnionCounty.name, self.WilliamsburgCounty.name)"

    class SD(object):
        """State of South Dakota"""

        name = "State of South Dakota"

        class BennettCounty(Jail):
            """Bennett County SD Jail"""

            jail_id = "bennett-so-sd"
            name = "Bennett County SD Jail"
        class ClayCounty(Jail):
            """Clay County SD Jail"""

            jail_id = "clay-so-sd"
            name = "Clay County SD Jail"
        class CusterCounty(Jail):
            """Custer County SD Jail"""

            jail_id = "custer-so-sd"
            name = "Custer County SD Jail"
        class DavisonCounty(Jail):
            """Davison County SD Jail"""

            jail_id = "davison-so-sd"
            name = "Davison County SD Jail"
        class LakeCounty(Jail):
            """Lake County SD Jail"""

            jail_id = "lake-so-sd"
            name = "Lake County SD Jail"
        class LincolnCounty(Jail):
            """Lincoln County SD Jail"""

            jail_id = "lincoln-so-sd"
            name = "Lincoln County SD Jail"
        class LawrenceCounty(Jail):
            """Lawrence County SD Jail"""

            jail_id = "lawrence-so-sd"
            name = "Lawrence County SD Jail"
        class MarshallCounty(Jail):
            """Marshall County SD Jail"""

            jail_id = "marshall-so-sd"
            name = "Marshall County SD Jail"
        class LymanCounty(Jail):
            """Lyman County SD Jail"""

            jail_id = "lyman-so-sd"
            name = "Lyman County SD Jail"
        class MeadeCounty(Jail):
            """Meade County SD Jail"""

            jail_id = "meade-so-sd"
            name = "Meade County SD Jail"
        class PenningtonCounty(Jail):
            """Pennington County SD Jail"""

            jail_id = "pennington-so-sd"
            name = "Pennington County SD Jail"
        class RobertsCounty(Jail):
            """Roberts County SD Jail"""

            jail_id = "roberts-so-sd"
            name = "Roberts County SD Jail"
        class UnionCounty(Jail):
            """Union County SD Jail"""

            jail_id = "union-so-sd"
            name = "Union County SD Jail"
        class SullyCounty(Jail):
            """Sully County SD Jail"""

            jail_id = "sully-so-sd"
            name = "Sully County SD Jail"
        class YanktonCounty(Jail):
            """Yankton County SD Jail"""

            jail_id = "yankton-so-sd"
            name = "Yankton County SD Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"SD(self.BennettCounty.name, self.ClayCounty.name, self.CusterCounty.name, self.DavisonCounty.name, self.LakeCounty.name, self.LincolnCounty.name, self.LawrenceCounty.name, self.MarshallCounty.name, self.LymanCounty.name, self.MeadeCounty.name, self.PenningtonCounty.name, self.RobertsCounty.name, self.UnionCounty.name, self.SullyCounty.name, self.YanktonCounty.name)"

    class TN(object):
        """State of Tennessee"""

        name = "State of Tennessee"

        class SullivanCounty(Jail):
            """Sullivan County TN Jail"""

            jail_id = "sullivan-so-tn"
            name = "Sullivan County TN Jail"
        class WashingtonCounty(Jail):
            """Washington County TN Jail"""

            jail_id = "washington-so-tn"
            name = "Washington County TN Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"TN(self.SullivanCounty.name, self.WashingtonCounty.name)"

    class TX(object):
        """State of Texas"""

        name = "State of Texas"

        class BrooksCounty(Jail):
            """Brooks County TX Jail"""

            jail_id = "brooks-so-tx"
            name = "Brooks County TX Jail"
        class PresidioCounty(Jail):
            """Presidio County TX Jail"""

            jail_id = "presidio-so-tx"
            name = "Presidio County TX Jail"
        class UpshurCounty(Jail):
            """Upshur County TX Jail"""

            jail_id = "upshur-so-tx"
            name = "Upshur County TX Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"TX(self.BrooksCounty.name, self.PresidioCounty.name, self.UpshurCounty.name)"

    class VA(object):
        """State of Virginia"""

        name = "State of Virginia"

        class CarolineCounty(Jail):
            """Caroline County VA Jail"""

            jail_id = "caroline-so-va"
            name = "Caroline County VA Jail"
        class NorthumberlandCounty(Jail):
            """Northumberland County VA Jail"""

            jail_id = "northumberland-so-va"
            name = "Northumberland County VA Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"VA(self.CarolineCounty.name, self.NorthumberlandCounty.name)"

    class WI(object):
        """State of Wisconsin"""

        name = "State of Wisconsin"

        class GrantCounty(Jail):
            """Grant County WI Jail"""

            jail_id = "grant-so-wi"
            name = "Grant County WI Jail"
        class DunnCounty(Jail):
            """Dunn County WI Jail"""

            jail_id = "dunn-so-wi"
            name = "Dunn County WI Jail"
        class LincolnCounty(Jail):
            """Lincoln County WI Jail"""

            jail_id = "lincoln-so-wi"
            name = "Lincoln County WI Jail"
        class MonroeCounty(Jail):
            """Monroe County WI Jail"""

            jail_id = "monroe-so-wi"
            name = "Monroe County WI Jail"
        class MenomineeCounty(Jail):
            """Menominee County WI Jail"""

            jail_id = "menominee-so-wi"
            name = "Menominee County WI Jail"
        class WashburnCounty(Jail):
            """Washburn County WI Jail"""

            jail_id = "washburn-so-wi"
            name = "Washburn County WI Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"WI(self.GrantCounty.name, self.DunnCounty.name, self.LincolnCounty.name, self.MonroeCounty.name, self.MenomineeCounty.name, self.WashburnCounty.name)"

    class WY(object):
        """State of Wyoming"""

        name = "State of Wyoming"

        class TetonCounty(Jail):
            """Teton County WY Jail"""

            jail_id = "teton-so-wy"
            name = "Teton County WY Jail"

        def __str__(self):
            """Return List of Known Counties"""
            return f"WY(self.TetonCounty.name)"


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

    def set_jail_id(self, jail: Jail | str):
        """Set jail ID and update api_url"""
        if isinstance(jail, Jail):
            self.__jail_id = jail.jail_id
            self.__jail = jail
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
        
        payload = {
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
        
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "zuercherportal_api/1.1.0",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate"
        }
        
        try:
            logger.trace("Making POST request")
            
            response = requests.post(
                url=self.__api_url,
                json=payload,
                headers=headers,
                timeout=30,  # Increased timeout for CI environments
            )
            
            response.raise_for_status()
            logger.trace("POST Request Complete")
            logger.debug(f"Response Code: {response.status_code}")
            
            data = response.json()
            logger.success(f"Total Record Count {data['total_record_count']}")
            
            if self.return_object:
                logger.trace("Converting to ZuercherportalResponse object")
                data = ZuercherportalResponse.fromdict(data)
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.trace("Request Exception occurred")
            logger.exception(f"Inmate Search Failed: {e}")
            return None

    def load_all_inmates(self):
        """Efficiently load all inmates using pagination"""
        all_inmates = []
        records_per_page = 100  # Use larger page size for efficiency
        current_page = 0
        
        while True:
            # Get page of inmates
            response = self.inmate_search(
                records_per_page=records_per_page,
                record_start=current_page * records_per_page
            )
            
            if not response:
                break
                
            # Add inmates from this page
            if self.return_object:
                inmates_page = response.records
                all_inmates.extend(inmates_page)
                total_records = response.total_record_count
            else:
                inmates_page = response.get('records', [])
                all_inmates.extend(inmates_page)
                total_records = response.get('total_record_count', 0)
            
            # Check if we've got all records
            if len(all_inmates) >= total_records or len(inmates_page) < records_per_page:
                break
                
            current_page += 1
            
        logger.success(f"Loaded {len(all_inmates)} total inmates")
        return all_inmates

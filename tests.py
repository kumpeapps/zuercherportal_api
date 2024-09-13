"""Unit Tests"""
import unittest
import zuercherportal_api as zuercherportal


class LearningCase(unittest.TestCase):
    """Test Cases"""
    def test_benton_county_ar(self):
        """Test Benton County Arkansas"""
        jail_api = zuercherportal.API(zuercherportal.Jails.AR.BENTON_COUNTY)
        inmate_data = jail_api.inmate_search()
        records_count = inmate_data["total_record_count"]
        self.assertGreater(records_count, 0)

    def test_pulaski_county_ar(self):
        """Test Pulaski County Arkansas"""
        jail_api = zuercherportal.API(zuercherportal.Jails.AR.PULASKI_COUNTY)
        inmate_data = jail_api.inmate_search()
        records_count = inmate_data["total_record_count"]
        self.assertGreater(records_count, 0)


def main():
    """Run Tests"""
    unittest.main()


if __name__ == "__main__":
    main()

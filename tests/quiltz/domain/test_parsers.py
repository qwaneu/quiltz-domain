from testing import *
from datetime import date
from quiltz.domain.parsers import date_from_iso, int_from_string
from quiltz.domain.results import  Success, Failure

class TestDateconversion:
    def test_parses_a_date_from_string(self):
        assert_that(date_from_iso.parse_from("2020-10-08"), equal_to(Success(date=date(2020,10,8))))

    def test_can_adjust_the_result_attribute(self):
        assert_that(date_from_iso.parse_from("2020-10-08", success_attribute='some_date'), equal_to(Success(some_date=date(2020,10,8))))

    def test_returns_failure_is_date_is_not_an_iso_string(self):
        assert_that(date_from_iso.parse_from("2020-1008", success_attribute='some_date'), equal_to(Failure(message="some_date: Invalid isoformat string: '2020-1008'")))

    def test_returns_failure_is_date_is_not_present(self):
        assert_that(date_from_iso.parse_from(None, success_attribute='some_date'), equal_to(Failure(message="some_date is missing")))

        
class TestIntFromstring:
    def test_parses_an_int_from_string(self):
        assert_that(int_from_string.parse_from("100"), equal_to(Success(int_val=100)))
    def test_can_have_a_custom_attribute(self):
        assert_that(int_from_string.parse_from("100", success_attribute='count'), equal_to(Success(count=100)))
    def test_accepts_spaces(self):
        assert_that(int_from_string.parse_from("  100  "), equal_to(Success(int_val=100)))
    def test_fails_when_it_has_leading_word_chars(self):
        assert_that(int_from_string.parse_from("W100"), equal_to(Failure(message="'W100' is not a valid integer")))
    def test_fails_when_it_has_trailing_word_chars(self):
        assert_that(int_from_string.parse_from("100W"), equal_to(Failure(message="'100W' is not a valid integer")))

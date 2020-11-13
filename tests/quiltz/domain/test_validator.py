from dataclasses import dataclass
from testing import *
from quiltz.domain.results import Success, Failure
from quiltz.domain.parsers import StringToObjectParser, date_from_iso
from quiltz.domain.validator import validate, conversion_of, presence_of, max_length_of, is_between


class TestValidator_presence_of:
    def test_returns_success_when_value_is_present(self):
        assert_that(validate(presence_of('some_parameter', 'value'))
            .map(lambda p: p.some_parameter),
            equal_to('value'))

    def test_returns_failure_when_value_is_not_present(self):
        assert_that(validate(presence_of('some_parameter', None))
            .map(lambda p: p.some_parameter),
            equal_to(Failure(message='some_parameter is missing')))

class TestValidator_conversion_of:
    def test_validates_a_conversion_that_potentially_returns_failure(self):
        assert_that(validate(conversion_of('language', 'en', StringToObjectParser(lambda lang_string: Success(language='en_lang'))))
            .map(lambda p: p.language),
            equal_to('en_lang'))

    def test_can_fail_a_conversion_that_potentially_returns_failure(self):
        assert_that(validate(conversion_of('language', 'xx', StringToObjectParser(lambda lang_string: Failure(message='uh oh'))))
            .map(lambda p: p.language),
            equal_to(Failure(message='uh oh')))


class TestValidator_conversion_of_other_parameter_support:
    def test_puts_the_parameter_under_that_name_in_valid_parameters(self):
        assert_that(validate(conversion_of('kleur', 'red', Color))
            .map(lambda p: p.kleur),
            equal_to(Color('red')))

@dataclass
class Color:
    color_value: str
    @staticmethod
    def parse_from(color_string, success_attribute):
        return Success(**{success_attribute: Color(color_value=color_string)})

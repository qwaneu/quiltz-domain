from testing import *
from quiltz.domain.results import Success, Failure
from quiltz.domain.parsers import StringToObjectParser
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



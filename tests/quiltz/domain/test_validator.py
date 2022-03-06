from dataclasses import dataclass
from testing import *
from quiltz.domain.results import Success, Failure
from quiltz.domain.validator import validate, conversion_of, presence_of, email_validity_of


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
        assert_that(validate(conversion_of('color', 'red', Color))
            .map(lambda p: p.color),
            equal_to(Color('red')))

    def test_can_fail_a_conversion_that_potentially_returns_failure(self):
        assert_that(validate(conversion_of('color', 'xx', Color))
            .map(lambda p: p.color),
            equal_to(Failure(message='uh oh')))


class TestValidator_conversion_of_other_parameter_support:
    def test_puts_the_parameter_under_that_name_in_valid_parameters(self):
        assert_that(validate(conversion_of('kleur', 'red', ColorWithSuccessAttributeSupport))
            .map(lambda p: p.kleur),
            equal_to(ColorWithSuccessAttributeSupport('red')))


class TestValidator_valid_email_address:
    def validate(self, email):
        return validate(email_validity_of('email_parameter', email)).map(lambda p: p.email_parameter)

    def test_returns_success_for_valid_email_address(self):
        assert_that(self.validate('r@qwan.eu'), equal_to('r@qwan.eu'))

    def test_returns_failure_when_value_is_not_valid(self):
        assert_that(self.validate('bla1234'), equal_to(Failure(message='email_parameter does not contain a valid email address')))
        assert_that(self.validate('.rob@qwan.eu').is_failure(), equal_to(True))

    def test_strips_spaces(self):
        assert_that(self.validate('\u00a0 henk@email.com  \t '), equal_to('henk@email.com'))


@dataclass
class ColorWithSuccessAttributeSupport:
    color_value: str

    @staticmethod
    def parse_from(color_string, success_attribute):
        return Success(**{success_attribute: ColorWithSuccessAttributeSupport(color_value=color_string)})


@dataclass
class Color:
    color_value: str

    @staticmethod
    def parse_from(color_string):
        if color_string == 'red':
            return Success(color=Color(color_value=color_string))
        else:
            return Failure(message='uh oh')

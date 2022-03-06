from testing import *
from quiltz.domain import is_valid_email_address


class TestValidEmailAddresses:
    def test_returns_success_for_valid_email_address(self):
        assert_that(is_valid_email_address('r@qwan.eu'), equal_to(True))
        assert_that(is_valid_email_address('r1@qwan.eu'), equal_to(True))
        assert_that(is_valid_email_address('rob@qwan.qwan.eu'), equal_to(True))
        assert_that(is_valid_email_address('r.o.b@qwan.eu'), equal_to(True))
        assert_that(is_valid_email_address('!#$%&\'*+-/=?^_`.{|}~@qwan.eu'), equal_to(True))
        assert_that(is_valid_email_address('rob@qwan-hq.eu'), equal_to(True))
        assert_that(is_valid_email_address('rob@qwan.bla-eu'), equal_to(True))
        assert_that(is_valid_email_address('rob+xyz@a.com'), equal_to(True))

    def test_returns_failure_when_value_is_not_valid(self):
        assert_that(is_valid_email_address('bla1234'), equal_to(False))
        assert_that(is_valid_email_address('.rob@qwan.eu'), equal_to(False))
        assert_that(is_valid_email_address('@qwan.eu'), equal_to(False))
        assert_that(is_valid_email_address('rob.@qwan.eu'), equal_to(False))
        assert_that(is_valid_email_address('r..ob@qwan.eu'), equal_to(False))
        assert_that(is_valid_email_address('rob@qwan..eu'), equal_to(False))
        assert_that(is_valid_email_address('rob@.qwan.eu'), equal_to(False))

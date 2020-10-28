from testing import *
from quiltz.domain.anonymizer import anonymize

class TestAnonymizer:
    def test_takes_first_letter_and_domain_of_email(self):
        assert_that(anonymize("rob@mailinator.com"), equal_to("r***@mailinator.com"))
        assert_that(anonymize("ro@mailinator.com"), equal_to("r***@mailinator.com"))
        assert_that(anonymize("r@mailinator.com"), equal_to("r***@mailinator.com"))

    def test_returns_the_whole_string_if_mail_is_not_an_email_address(self):
        assert_that(anonymize("robmailinator.com"), equal_to("robmailinator.com"))
        
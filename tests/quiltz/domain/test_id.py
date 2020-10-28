from testing import *
from hamcrest import is_, is_not, starts_with, matches_regexp, instance_of
from uuid import UUID as UUID_IMPL
from quiltz.domain.id import ID, IDGenerator
from quiltz.domain.id.testbuilders import aValidUUID, aValidID

class TestIDCreationFromString:
    def test_creates_an_id_based_on_a_uuid(self):
        assert_that(ID.from_string(str(aValidUUID('34'))), equal_to(ID(aValidUUID('34'))))

    def test_is_valid(self):
        assert_that(ID.from_string(str(aValidUUID('34'))).valid, is_(equal_to(True)))

    def test_creates_an_invalid_id_when_the_string_value_is_not_a_valid_uuid(self):
        assert_that(ID.from_string('34').valid, is_(equal_to(False)))

class TestHashability:
    def test_it_is_hashable_when_valid(self):
        assert_that({ aValidID('34'): 'some_value' }[aValidID('34')], equal_to('some_value'))

    def test_it_is_hashable_when_invalid(self):
        invalid_id = ID.invalid()
        assert_that({ invalid_id: 'some_value' }[invalid_id], equal_to('some_value'))


class TestStringValue:
    def test_is_the_string_value_of_the_uuid(self):
        assert_that(str(ID(aValidUUID('34'))), equal_to(str(aValidUUID('34'))))

    def test_is_invalid_id_when_invalid(self):
        assert_that(str(ID.invalid()), starts_with('invalid_id'))

class TestInvalidId:
    def test_is_unique(self):
        assert_that(ID.invalid(), is_not(equal_to(ID.invalid())))

class TestIdGenerator:
    def test_generate_id_generates_some_uuid(self):
        assert_that(str(IDGenerator().generate_id()), matches_regexp('[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'))

    def test_generate_id_yields_unique_results(self):
        assert_that(IDGenerator().generate_id(), is_not(equal_to(IDGenerator().generate_id())))

    def test_type_is_ID(self):
        assert_that(IDGenerator().generate_id(), is_(instance_of(ID)))
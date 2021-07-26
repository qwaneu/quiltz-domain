from testing import *
from quiltz.domain.results import Success, Failure, PartialSuccess

class ResultContract:
    @pytest.fixture
    def result_class(self):
        raise NotImplementedError('Not Implemented Yet')

    def test_passed_attributes_can_be_obtained_as_attribute(self, result_class):
        assert_that(result_class(some_random_attribute="some_value").some_random_attribute, equal_to("some_value"))

    def test_passed_attributes_end_up_in_the_body(self, result_class):
        assert_that(result_class(some_random_attribute="some_value").body, equal_to(dict(some_random_attribute="some_value")))
    
    def test_can_add_an_attribute(self, result_class):
        assert_that(result_class().with_attributes(some_other_attribute="some_other_value").some_other_attribute, equal_to("some_other_value"))

class SideEffect:
    def __init__(self):
        self.executed = False
    def execute(self):
        self.executed = True

class TestFailure(ResultContract):
    @pytest.fixture
    def result_class(self):
        return Failure

    def test_map_on_failure_returns_same_failure(self):
        result = Failure(message='Fail').map(lambda r: Success(value=10))
        assert_that(result, equal_to(Failure(message='Fail')))

    def test_do_on_failure_is_not_executed(self):
        side_effect = SideEffect()
        result = Failure(message = 'Fail').do(lambda result: side_effect.execute() )
        assert_that(side_effect.executed, is_not(True))
        assert_that(result, equal_to(Failure(message='Fail')))

    def test_or_fail_with_replaces_failure(self):
        result = Failure(message = 'Fail').or_fail_with(value = 0)
        assert_that(result, equal_to(Failure(reason=Failure(message='Fail'), value=0)))
        
class TestSuccess(ResultContract):
    @pytest.fixture
    def result_class(self):
        return Success

    def test_map_on_success_returns_new_result(self):
        result = Success(message = 'Success').map(lambda r: Success(value = 10))
        assert_that(result, equal_to(Success(value=10)))

    def test_do_on_success_is_executed(self):
        side_effect = SideEffect()
        result = Success(message = 'Success').do(lambda result: side_effect.execute() )
        assert_that(side_effect.executed, is_(True))
        assert_that(result, equal_to(Success(message='Success')))

    def test_or_fail_with_does_not_affect_success(self):
        result = Success(message = 'Success').or_fail_with(value = 0)
        assert_that(result, equal_to(Success(message='Success')))

class TestPartialSucces(ResultContract):
    @pytest.fixture
    def result_class(self):
        return PartialSuccess

    def test_is_a_success(self):
        assert_that(PartialSuccess().is_success(), is_(False))

    def test_is_a_failure(self):
        assert_that(PartialSuccess().is_failure(), is_(True))

    def test_map_on_partial_success_merges_success_value(self):
        result = PartialSuccess(message = 'Fail').map(lambda r: Success(value = 10))
        assert_that(result, equal_to(PartialSuccess(message = 'Fail', value=10)))

    def test_do_on_partial_success_is_not_executed(self):
        side_effect = SideEffect()
        result = PartialSuccess(message = 'Fail').do(lambda result: side_effect.execute() )
        assert_that(side_effect.executed, is_(True))
        assert_that(result.message, equal_to('Fail'))

    def test_or_fail_with_does_not_affect_partial_success(self):
        result = PartialSuccess(message = 'Success').or_fail_with(value = 0)
        assert_that(result, equal_to(PartialSuccess(message='Success')))

        

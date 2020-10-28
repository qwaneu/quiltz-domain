from testing import *
from quiltz.domain.results import Success, Failure

class ResultContract:
    @pytest.fixture
    def result_class(self):
        raise NotImplementedError('Not Implemented Yet')

    def test_passed_attributes_can_be_obtained_as_attribute(self, result_class):
        assert result_class(some_random_attribute="some_value").some_random_attribute == "some_value"

    def test_passed_attributes_end_up_in_the_body(self, result_class):
        assert result_class(some_random_attribute="some_value").body == dict(some_random_attribute="some_value")

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
        result = Failure(message = 'Fail').map(lambda r: Success(value = 10))
        assert result.message == 'Fail'

    def test_do_on_failure_is_not_executed(self):
        side_effect = SideEffect()
        result = Failure(message = 'Fail').do(lambda result: side_effect.execute() )
        assert not side_effect.executed
        assert result.message == 'Fail'

    def test_or_fail_with_replaces_failure(self):
        result = Failure(message = 'Fail').or_fail_with(value = 0)
        assert result.value == 0
        
class TestSuccess(ResultContract):
    @pytest.fixture
    def result_class(self):
        return Success

    def test_map_on_success_returns_new_result(self):
        result = Success(message = 'Success').map(lambda r: Success(value = 10))
        assert result.value == 10

    def test_do_on_success_is_executed(self):
        side_effect = SideEffect()
        result = Success(message = 'Success').do(lambda result: side_effect.execute() )
        assert side_effect.executed
        assert result.message == 'Success'

    def test_or_fail_with_does_not_affect_success(self):
        result = Success(message = 'Success').or_fail_with(value = 0)
        assert result.message == 'Success'


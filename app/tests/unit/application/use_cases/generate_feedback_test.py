from faker import Faker
from pytest_mock import MockerFixture


from app.application.use_cases.generate_feedback.generate_feedback import Feedback
from app.domain.models import Person, AIResponse

faker = Faker()


class TestFeedback:
    def test__generate_feedback__returns_feedback__when_(self, mocker: MockerFixture):
        assert True

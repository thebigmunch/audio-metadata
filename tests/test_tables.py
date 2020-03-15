from ward import test

from audio_metadata.formats.tables import (
	_BaseEnum,
	_BaseIntEnum,
)


class TestEnum(_BaseEnum):
	MEMBER = 0


class TestIntEnum(_BaseIntEnum):
	MEMBER = 0


@test(
	"Table enum reprs",
	tags=['unit', 'formats', 'tables'],
)
def _():
	assert repr(TestEnum.MEMBER) == '<TestEnum.MEMBER>'
	assert repr(TestIntEnum.MEMBER) == '<TestIntEnum.MEMBER>'

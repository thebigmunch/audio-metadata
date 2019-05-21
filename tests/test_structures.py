import pytest
from audio_metadata.structures import DictMixin, ListMixin


class DictMixinMissing(DictMixin):
	def __missing__(self, key):
		raise KeyError(key)


def test_DictMixin():
	dict_mixin = DictMixin(key1='value1', key2='value2')

	assert repr(dict_mixin) == "<DictMixin ({'key1': 'value1', 'key2': 'value2'})>"
	assert dict_mixin.__repr__(repr_dict={}) == '<DictMixin ({})>'

	assert list(dict_mixin.items()) == [('key1', 'value1'), ('key2', 'value2')]
	assert list(dict_mixin.keys()) == ['key1', 'key2']
	assert list(dict_mixin.values()) == ['value1', 'value2']

	assert len(dict_mixin) == 2
	assert list(iter(dict_mixin)) == list(iter({'key1': 'value1', 'key2': 'value2'}))

	with pytest.raises(KeyError):
		dict_mixin['test']

	dict_mixin['key3'] = 'value3'
	assert dict_mixin['key3'] == 'value3'

	del dict_mixin['key3']
	assert 'key3' not in dict_mixin

	dict_mixin.key3 = 'value3'
	assert dict_mixin.key3 == 'value3'

	del dict_mixin.key3
	assert not hasattr(dict_mixin, 'key3')

	with pytest.raises(AttributeError):
		dict_mixin.key3

	with pytest.raises(AttributeError):
		del dict_mixin.key3

	dict_mixin_missing = DictMixinMissing()
	with pytest.raises(KeyError):
		dict_mixin_missing['test']


def test_ListMixin():
	list_mixin = ListMixin(['item1', 'item2'])

	assert repr(list_mixin) == '<ListMixin (2 items)>'
	assert list_mixin.items == ['item1', 'item2']

	list_mixin.item_label = 'test items'
	assert repr(list_mixin) == '<ListMixin (2 test items)>'

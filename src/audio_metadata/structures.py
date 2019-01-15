__all__ = ['DictMixin', 'ListMixin']

from collections import UserList
from collections.abc import MutableMapping

import pprintpp


class DictMixin(MutableMapping):
	def __getattr__(self, attr):
		try:
			return self.__getitem__(attr)
		except KeyError:
			raise AttributeError(attr) from None

	def __setattr__(self, attr, value):
		self.__setitem__(attr, value)

	def __delattr__(self, attr):
		try:
			return self.__delitem__(attr)
		except KeyError:
			raise AttributeError(attr) from None

	def __getitem__(self, key):
		return self.__dict__[key]

	def __setitem__(self, key, value):
		self.__dict__[key] = value

	def __delitem__(self, key):
		del(self.__dict__[key])

	def __missing__(self, key):
		return KeyError(key)

	def __iter__(self):
		return iter(self.__dict__)

	def __len__(self):
		return len(self.__dict__)

	def __repr__(self, repr_dict=None):
		repr_dict = repr_dict if repr_dict is not None else self.__dict__
		return f"<{self.__class__.__name__} ({pprintpp.pformat(repr_dict)})>"

	# def __str__(self):
	# 	return pprintpp.pformat({(k, v) for k, v in self.items() if not k.startswith('_')})

	def items(self):
		return self.__dict__.items()

	def keys(self):
		return self.__dict__.keys()

	def values(self):
		return self.__dict__.values()


class ListMixin(UserList):
	item_label = 'items'

	def __repr__(self):
		return f"<{self.__class__.__name__} ({len(self)} {self.item_label})>"

	@property
	def items(self):
		return self.data


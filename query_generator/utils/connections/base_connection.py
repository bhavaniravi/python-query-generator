from abc import ABC, abstractmethod


class BaseConnection(ABC):
	@abstractmethod
	def connect(self):
		pass

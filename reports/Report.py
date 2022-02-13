import abc
import pprint


class Report:

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def generate(self, data):
        pass

    @abc.abstractmethod
    def print(self, data):
        pp = pprint.PrettyPrinter(indent=4)
        for stock in data:
            pp.pprint(stock)

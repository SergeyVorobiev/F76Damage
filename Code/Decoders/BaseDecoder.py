from Code.Decoders.AbstractDecoder import AbstractDecoder

from Code.Decoders.Templates import F76DTemplates


class BaseDecoder(AbstractDecoder):

    def __init__(self, template: F76DTemplates):
        super().__init__(template.value['start_key'],
                         template.value['end_key'],
                         template.value['categories'],
                         template.value['max_unit_length'],
                         template.value['size_func'],
                         template.value['filter_func'])
        self.__count = 0

    def before_start(self):
        pass

    def decoded(self, unit: bytes, result: {}):
        self.__count += 1

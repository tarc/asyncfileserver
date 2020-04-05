from asyncfileserver.model.data_view import DataView


class DataViewFormatter(object):
    def format(self, data):
        return DataView(data)

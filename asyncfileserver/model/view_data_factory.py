from asyncfileserver.model.view_data import ViewData


class ViewDataFactory(object):
    def create(self, data):
        return ViewData(data)

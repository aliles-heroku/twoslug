from werkzeug.routing import BaseConverter


class HexConverter(BaseConverter):

    def to_python(self, value):
        return int(value, 16)

    def to_url(self, value):
        return '%x' % value


class OctConverter(BaseConverter):

    def to_python(self, value):
        return int(value, 8)

    def to_url(self, value):
        return '%o' % value

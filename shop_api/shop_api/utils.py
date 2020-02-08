from json import JSONEncoder
import decimal


class DecimalJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalJSONEncoder, self).default(o)

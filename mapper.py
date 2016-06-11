class Test(object):
    def __init__(self):
        self.A = 1
        self.B = 2
        self.A1 = "a1"
        self.A2 = "a2"

a = {
    "alphabetics": { "A": "A", "B": "B"},
    "numericalphabetics": { "A1": "A1", "A2": "A2" }
}
class Mapper(object):
    def __init__(self, other, _map, raiseKeyError=False):
        print other, _map
        if not isinstance(_map, dict):
            raise TypeError("_map must be a dict. Received type={}".format(type(_map)))
        self._map = _map
        self.other = other
        self.raiseKeyError = raiseKeyError

        def _inspect_items(items, headkey):
            for key, item in items.iteritems():
                # TODO: maybe refactor all isinstance to instead query on ABCs
                if isinstance(item, dict):
                    _inspect_items(item, headkey + "[{}]".format(key))
                elif isinstance(item, str):
                    if raiseKeyError:
                        try:
                            return getattr(self.other, item)
                        except AttributeError:
                            raise ValueError("All strings must correspond to attributes on other when raiseKeyError=False")
                    else:
                        continue
                else:
                    raise TypeError("val={} from _map{} is neither a dict nor str".format(item, headkey + "[{}]".format(key)))

        _inspect_items(self._map, "")
    def __getitem__(self, key):
        item = self._map[key]
        if isinstance(item, dict):
            return Mapper(self.other, item, raiseKeyError=self.raiseKeyError)
        elif isinstance(item, str):
            if self.raiseKeyError:
                return getattr(self.other, item)
            else:
                return getattr(self.other, item, None)
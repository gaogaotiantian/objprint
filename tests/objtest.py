class ObjTest:
    def __init__(self, attrs, function=None):
        for key, value in attrs.items():
            setattr(self, key, value)
        if function is not None:
            self.function = function

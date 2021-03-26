class ObjTest:
    def __init__(self, attrs):
        for key, value in attrs.items():
            setattr(self, key, value)

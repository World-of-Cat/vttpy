def reversible_str_enum(cls):
    cls.__inverse_table__ = {str(v): v for v in cls}
    cls.inverse = classmethod(lambda cls, s: cls.__inverse_table__.get(s, None))
    return cls

def reversible_int_enum(cls):
    cls.__inverse_table__ = {int(v): v for v in cls}
    cls.inverse = classmethod(lambda cls, s: cls.__inverse_table__.get(s, None))
    return cls

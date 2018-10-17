

class UnionizeCase(object):
    __slots__ = (
        'parameters',
        'reader',
        'unionize_class', 
        'postprocessing', 
    )


class TissuecyteClassicUnionizeCase(UnionizeCase):
    def __init__(self):
        self.parameters = 
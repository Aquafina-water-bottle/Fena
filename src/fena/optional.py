
class Optional:
    """
    Used where it might be possible to get an object.

    This is a very simplified version of the Java 8 Optional class
    """

    def __init__(self, item):
        self._item = item
    
    @staticmethod
    def empty():
        """
        Returns itself with None as its item
        """
        return Optional(None)

    def isPresent(self):
        """
        Returns whether an item exists or not
        """
        return self._item is not None

    def get(self):
        return self._item
    
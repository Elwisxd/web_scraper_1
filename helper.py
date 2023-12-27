

class Helper:

    """Helper class is for miscellaneous static helper functions"""
    @staticmethod
    def isfloat(num):
        """
        Returns:
            (bool) - is number float
        """
        try:
            if float(num):
                return True
            if int(num):
                return True
            return False
        except:
            return False

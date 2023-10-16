

class Helper:

    @staticmethod
    def isfloat(num):

        try:
            if float(num):
                return True
            if int(num):
                return True
            return False
        except:
            return False

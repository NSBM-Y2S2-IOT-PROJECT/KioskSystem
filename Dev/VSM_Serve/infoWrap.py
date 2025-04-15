import datetime
class Info:
    def info(self, data):
        # show [INFO] in green color
        print("\033[92m[PROJECT-VISUM-INTERNAL-INFO]\033[0m", data)

    def error(self, data):
        # show [ERROR] in red color
        print("\033[91m[ERROR]\033[0m", data)

    def warning(self, data):
        # show [WARNING] in yellow color
        print("\033[93m[WARNING]\033[0m", data)

    def debug(self, data):
        # show [DEBUG] in cyan color
        print("\033[96m[DEBUG]\033[0m", data)

    def command(self, data):
        print("\033[96m[OVERRIDE]\033[0m", data, ">")

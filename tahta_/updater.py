import github as gtb
class InvalidReleaseVer(Exception):
    message = "APP_VERSION IS BIGGER THAN RELEASE VERSION"
    def __init__(self) -> None:
        super().__init__(self.message)

class VersionChecker:
    def __init__(self,app_ver:float) -> None:
        self.g = gtb.Github()
        self.repo = self.g.get_repo("LothRobotics/tubitak-2204a")
        self.app_ver = app_ver
        
    def check_version(self):
        """Checks and returns if an update is needed or not

        Raises:
            InvalidReleaseVer: If the app version is negative or higher than the latest version 

        Returns:
            bool: Returns True if an update is needed, False if an update isn't needed.
        """
        rmfile = self.repo.get_readme() #get readme.md
        rmtext = rmfile.decoded_content.decode() #get the str and decode it
        lines = rmtext.splitlines(False) #split the lines
        line = lines[0] #get the first line
        index = line.find("Sürüm") #find which index has "Sürüm" and get the string starting from there

        VER_NUM = float(line[index:].strip("Sürüm").strip()) #get the version_num

        if self.app_ver > VER_NUM:
            raise InvalidReleaseVer
        elif self.app_ver == VER_NUM:
            return False
        elif self.app_ver < VER_NUM:
            return True

if __name__ == '__main__':
    checker = VersionChecker(0.02)
    try: 
        result = checker.check_version()
        print(result)
    except:
        print(InvalidReleaseVer.message)
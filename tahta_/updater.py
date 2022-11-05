import github as gtb
import zipfile
from io import StringIO
import requests
import os
import shutil

class InvalidReleaseVer(Exception):
    def __init__(self,value) -> None:
        if value < 0:
            self.message = "APP_VERSION IS NEGATIVE"
        else:
            self.message = "APP_VERSION IS BIGGER THAN RELEASE VERSION"

        super().__init__(self.message)

class VersionChecker:
    def __init__(self,app_ver:float) -> None:
        
        self.g = gtb.Github()
        try:
            self.repo = self.g.get_repo("LothRobotics/tubitak-2204a")
        except gtb.RateLimitExceededException:
            print("EXCEEDED THE MAX API LIMIT GITHUB")
        self.app_ver = app_ver
        
    def check_version(self):
        """Checks and returns if an update is needed or not

        Raises:
            InvalidReleaseVer: If the app version is negative or higher than the latest version 

        Returns:
            bool: Returns True if an update is needed, False if an update isn't needed.
        """
        try:
            rmfile = self.repo.get_readme() #get readme.md
        except AttributeError:
            print("Couldnt get the repo readme")
            return False
        rmtext = rmfile.decoded_content.decode() #get the str and decode it
        lines = rmtext.splitlines(False) #split the lines
        line = lines[0] #get the first line
        index = line.find("Sürüm") #find which index has "Sürüm" and get the string starting from there

        VER_NUM = float(line[index:].strip("Sürüm").strip()) #get the version_num

        if self.app_ver > VER_NUM or self.app_ver < 0:
            raise InvalidReleaseVer(self.app_ver)
        elif self.app_ver == VER_NUM:
            return False
        elif self.app_ver < VER_NUM:
            return True

    def update(self):
        """Not done yet please dont run this
        """
        try:
            release = self.repo.get_latest_release()
            releasesth = release.get_assets()
            print(release.upload_url)
            print(release.html_url)
            print(release.url)
            print(release.zipball_url)

            
            url = release.zipball_url #"https://api.github.com/repos/LothRobotics/tubitak-2204a/zipball/test"
            #url = 'https://api.github.com/repos/facebook/react/releases'
            response = requests.get(url)
            # Raise an exception if the API call fails.
            response.raise_for_status()
            
            z = zipfile.ZipFile(StringIO(response.content))
            
            
            

            shutil.rmtree()

            z.extractall() # extract the files

        except gtb.RateLimitExceededException:
            print("RATE LIMIT BRUH")

if __name__ == '__main__':
    checker = VersionChecker(0.02)
    #result = checker.check_version()
    #checker.update()

    for directory in os.walk(os.curdir):
        print(str(directory[2]))

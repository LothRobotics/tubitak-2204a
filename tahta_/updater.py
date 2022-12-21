import github as gtb
import zipfile
from io import BytesIO
import requests
import os
import shutil
import json
from PyQt5.QtCore import pyqtSignal,QObject,pyqtBoundSignal

class InvalidReleaseVer(Exception):
    def __init__(self,value) -> None:
        if value < 0:
            self.message = "APP_VERSION IS NEGATIVE"
        else:
            self.message = "APP_VERSION IS BIGGER THAN RELEASE VERSION"

        super().__init__(self.message)

class VersionChecker:
    def __init__(self,app, app_ver:float, logger) -> None:
        self.app = app
        self.logger = logger
        self.g = gtb.Github( #login_or_token="bruh" #TODO: REMOVE MY TOKEN
        )
        
        self.progressignal = pyqtBoundSignal()
        self.progressignal
        
        try:
            self.repo = self.g.get_repo("LothRobotics/tubitak-2204a")
        except gtb.RateLimitExceededException:
            self.logger.error("EXCEEDED THE MAX API LIMIT GITHUB")
        self.app_ver = app_ver
        
        #self.importantfiles = ["data.json","log.log","db_credentials.json"]

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
            self.logger.error("Couldnt get the repo readme")
            return False
        rmtext = rmfile.decoded_content.decode() #get the str and decode it
        lines = rmtext.splitlines(False) #split the lines
        line = lines[0] #get the first line
        index = line.find("Sürüm") #find which index has "Sürüm" and get the string starting from there

        self.VER_NUM = float(line[index:].strip("Sürüm").strip()) #get the version_num

        if self.app_ver > self.VER_NUM or self.app_ver < 0:
            raise InvalidReleaseVer(self.app_ver)
        elif self.app_ver == self.VER_NUM:
            return False
        elif self.app_ver < self.VER_NUM:
            return True

    def update(self):
        """I think its done
        """
        try:
            release = self.repo.get_latest_release()
            releasesth = release.get_assets()
            self.logger.info(f"release upload url: {release.upload_url}\nrelease html url: {release.html_url}\nrelease url :{release.url}\nrelease zipball url: {release.zipball_url}")
            download_url = release.url
            
            # store the URL in url as 
            # username = "N0tn3nl1sh"
            # token = "bruh"

            self.logger.info("DOWNLOADING JSON")
            response = requests.get(download_url,       #auth=(username,token) #TODO: Comment this when releasing app
            ).json()

            self.logger.info("GOT APP ZIP DOWNLOAD URL")
            app_download_url = response["assets"][0]["browser_download_url"]
            self.logger.info(app_download_url)

            self.logger.info("DOWNLOADING THE ACTUAL FILE")
            response = requests.get(app_download_url,   #auth=(username,token) #TODO: Comment this when releasing app
            )

            self.logger.info("MAKING ZIP")
            z = zipfile.ZipFile(BytesIO(response.content))
            self.logger.info("MADE ZIP")

            self.logger.warning("STARTED DELETING FILES")
            self.delete_files()

            self.logger.info("REWRITING THE VERSION.JSON FILE")
            with open("data/version.json","r") as file:
                versiondata = json.load(file)
            versiondata["version"] = self.VER_NUM

            with open("data/version.json","w") as file:
                json.dump(versiondata,file,indent=4,ensure_ascii=False)

            self.logger.info("EXTRACTING THE ZIP")
            # Extract all the contents of zip file in current directory
            with z as zipObj:
                zipObj.extractall()
            self.logger.info("EXTRACTED THE ZIP")

            self.app.signalmanager.updatedone.emit()

        except gtb.RateLimitExceededException:
            self.logger.error("RATE LIMIT EXCEEDED EXCEPTION")

    def delete_files(self):
        tobedeleted = []
        for d in os.walk(os.curdir):
            dirpath = d[0] #current path
            dirname = d[1] #paths that it can go to
            filename = d[2] #files that are currently there
            self.logger.info(f"dirpath: {dirpath} , dirname: {dirname} , filename: {filename}" )
            
            if dirpath == "." : # Files inside root
                self.logger.info(f"WONT BE DELETED {dirpath}")
                for f in filename:
                    self.logger.info(f"REMOVE FILE: {f}")
                    os.remove(f)
                    pass
            elif dirpath == ".\\data": #DATA folder
                self.logger.info("DATA folder so it wont be deleted")
                pass
            else: #Folders in root
                self.logger.info(f"TOBELETED: {dirpath}")
                tobedeleted.append(dirpath)

        self.logger.info(f"THESE WILL BE DELETED: {tobedeleted}")
        for folder in tobedeleted:
            shutil.rmtree(folder)
            pass

if __name__ == '__main__':
    checker = VersionChecker(None,0.02)
    #result = checker.check_version()
    print(f"IS UPDATE NEEDED: {checker.check_version()}")
    #checker.delete_files()
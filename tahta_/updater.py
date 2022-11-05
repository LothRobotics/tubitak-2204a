import github as gtb

g = gtb.Github()
repo = g.get_repo("LothRobotics/tubitak-2204a")
rmfile = repo.get_readme() #get readme.md
rmtext = rmfile.decoded_content.decode() #get the str and decode it
lines = rmtext.splitlines(False) #split the lines
line = lines[0] #get the first line
index = line.find("Sürüm") #find which index has "Sürüm" and get the string starting from there

VER_NUM = float(line[index:].strip("Sürüm").strip()) #get the version_num

print(VER_NUM )


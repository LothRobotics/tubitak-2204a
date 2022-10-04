from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json

# bu kod gidip siteden deprem bilgisini alıp sonra da bunu debuglines.txt'ye kaydediyo

PATH = "chromedriver.exe"

website_url = "http://www.koeri.boun.edu.tr/scripts/lst2.asp"

driver = webdriver.Chrome(PATH)

driver.get(website_url)

element = driver.find_element(By.CSS_SELECTOR, "pre") #neden bilmiyorum ama sadece <pre> ismine sahip olan bu şeyi bile buluyo

formatted_text = element.text

with open("debug.txt","w") as file:
    file.write(formatted_text)

lines = formatted_text.splitlines(True) #False \n olmasın, True \n olsun anlamında

with open("debuglines.txt","w") as file:
    json.dump(lines,file)
    


"""
pos = 0
for char in formatted_text:
    if char == "\n":
        print("aaa: ",pos)
    pos += 1
"""

#element.screenshot("debug.png") # ss alma
driver.close()
print("end")
#result = driver.find_element(By.id) #by.id dedii şey ben id ile arıcam demek


#driver.title

#driver.close() #close the tab
#driver.quit() #close the entire window

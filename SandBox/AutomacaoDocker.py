from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

print("=+=+=+=+=+=+=+= SELECIONE O NAVEGADOR =+=+=+=+=+=+=+=")
print("[01] - CHROME")
print("[02] - FIREFOX")

op = int(input("NAVEGADOR: "))

if op == 1:
    driver = webdriver.Chrome(executable_path='..\drivers\Chrome32Bits.exe')
    '''
    capabilities = {
        "browserName": "chrome",
        "browserVersion": "86.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": False
        }
    }
    '''



if op == 2:
    driver = webdriver.Firefox(executable_path='..\drivers\Firefox.exe')
    '''
    capabilities = {
        "browserName": "firefox",
        "browserVersion": "80.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": False
        }
    }
    
    driver = webdriver.Remote(
    command_executor="http://localhost:4444/wd/hub",
    desired_capabilities=capabilities)
    '''

driver.maximize_window()

driver.get("https://www.google.com/")
driver.find_element_by_name('q').send_keys("Teste Automação" + Keys.ENTER)

#body = driver.find_element_by_tag_name("body")
#body.send_keys(Keys.CONTROL + 't')

#webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("t").perform()

driver.execute_script("window.open('', '_blank')")

#driver.close()

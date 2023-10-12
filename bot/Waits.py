from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
def wait_to_be_located(driver , timeout , elem) :
    wait=WebDriverWait(driver,timeout).until(EC.presence_of_element_located(elem))
    return wait

def wait_to_be_located_and_clickable(driver , timeout , elem) :
    wait=WebDriverWait(driver,timeout).until(EC.presence_of_element_located(elem))
    click=WebDriverWait(driver,timeout).until(EC.element_to_be_clickable(elem))
    return click

def wait_all_to_be_located (driver , timeout , elem)  :
    wait=WebDriverWait(driver,timeout).until(EC.presence_of_all_elements_located(elem))
    return wait

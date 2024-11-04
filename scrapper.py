import connector
from selenium import webdriver
from selenium.webdriver.common.by   import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.safari.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from re import findall
from time import sleep
from datetime import datetime


HTML = "https://campusrec.utah.edu/live-usage/index.php"
connection = connector.connect_to_main()

def find_main_div(driver: webdriver) -> str:
    # Opening the webpage
    driver.get(HTML)    
    sleep(2)
    
    # Finding and moving to correct Iframe
    frame = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
    driver.switch_to.frame(frame)
    
    # Finding the Div that has the info needed
    info_div = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="container"]/div[3]/div/div/div/div[2]/div[1]/center/div[2]')))
    
    percent_div = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="container"]/div[3]/div/div/div/div[2]/div[1]/center/div[1]/div/div/div/span')))
    
    return info_div.text, percent_div.text

def get_usage(info_div: str):
    for string in info_div.split(" "):
        if "Updated" in string:
            return int(findall(r'\d+', string)[0])

def get_date(info_div: str) -> str:
    # Manipulating the string until we get the format "MM/DD/YYYY HH:MM (AM+PM)""
    first_index = info_div[:info_div.rfind(":")]
    time_signature = info_div[first_index.rfind(":")+2:]
    
    # Transforming it to a datetime element
    parsed_datetime = datetime.strptime(time_signature, "%m/%d/%Y %I:%M %p")
    
    # Parsing it to a mySQL-compliant style
    mysql_format_datetime = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")

    return mysql_format_datetime
    
if __name__ == "__main__":
    # options = Options()
    # options.automatic_inspection = False
    # options.automatic_profiling = False
    
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    connection = connector.connect_to_main()
    info_div, percent_div = find_main_div(driver)
    percent = int(percent_div.replace("%", ""))
    usage = get_usage(info_div)
    date = get_date(info_div)
    print(date)
    connector.add_row(connection, date, usage, percent)
    connector.get_all(connection)
    connector.close_connection(connection)
    
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    
    with open("/Users/brunogomespascotto/Documents/AreaAvailabilityAnalyser/Log.txt", 'a') as file:
        file.write(f"Last updated: {dt_string} - {date}, {usage}, {percent}\n")
    
    driver.close()
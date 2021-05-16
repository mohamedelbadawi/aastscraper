from selenium import webdriver
from telebot.types import Message
from webdriver_manager.chrome import ChromeDriverManager
import telebot
import time
from selenium import webdriver
import os
BOT_TOKEN="1774877121:AAGjrkUAmJkzrHmDS-RaEG7rkzdENRX4jLQ"
bot = telebot.TeleBot(token=BOT_TOKEN)

@bot.message_handler(commands=['start'])
def sayWelcome(message):
    bot.send_message(message.chat.id,"Enter your login information with this format 18108564:954564")
    bot.register_next_step_handler(message,getResult)

def getResult(message):
    inputText=message.text
    inputText=inputText.rsplit(":")
    print(inputText)
    if input =="Please send the login information with this format 18108564:954564":
        bot.send_message(message.chat.id,inputText)
        bot.register_next_step_handler(message.chat.id,getResult)
    else:
        ID=inputText[0]
        PIN_CODE=inputText[1]
        sendResult(message,ID,PIN_CODE)

def checkInput(string):
    if string.contains(":"):
        return string.rsplit(":")
    else:
        return "Please send the login information with this format 18108564:954564"


def sendResult(message,ID,PIN_CODE):

    # chromeOptions=webdriver.ChromeOptions()
    # chromeOptions.add_argument("--headless")
    # browser = webdriver.Chrome(ChromeDriverManager().install())
    
    
    # # browser.set_window_position(-10000,0)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
            
        browser.get("https://studentportal.aast.edu/Login")
        browser.find_element_by_css_selector("#page-container > div > div.right-content > div.login-content > form > div:nth-child(7) > input").send_keys(ID)
        browser.find_element_by_css_selector("#page-container > div > div.right-content > div.login-content > form > div:nth-child(8) > input").send_keys(PIN_CODE)
        browser.find_element_by_css_selector("#page-container > div > div.right-content > div.login-content > form > div.login-buttons > div > button").click()
        browser.implicitly_wait(2)
        browser.find_element_by_css_selector("#content > div > div:nth-child(6) > a > div > div > h5").click()
        browser.implicitly_wait(2)
        for i in range(2,8):
            result=browser.find_element_by_xpath(f"//*[@id='content']/div/div[3]/div/table/tbody/tr[{i}]").text
            bot.send_message(message.chat.id,result)
            print(result)
        browser.quit()
while True:
    try:
        bot.polling()
    except:
        time.sleep(5)

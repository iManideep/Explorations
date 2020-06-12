from selenium import webdriver

driver=webdriver.Chrome(r"C:\Users\meda.manideep\Downloads\chromedriver_win32\chromedriver.exe")
driver.get("https://web.whatsapp.com/")
driver.maximize_window()
input("Enter any key after scanning QR Code:")
while True:
    user_name=input("Enter contact name as in Whatsapp:\n")
    message=input("Enter message:\n")
    contact_name=driver.find_element_by_xpath("//span[@title='{}']".format(user_name))
    contact_name.click()
    message_box=driver.find_element_by_xpath('//div[@class="_2S1VP copyable-text selectable-text"][@data-tab="1"][@spellcheck="true"]')
    message_box.send_keys(message)
    send_button=driver.find_element_by_xpath('//span[@data-icon="send"]')
    send_button.click()
    print("Successfully Sent!")
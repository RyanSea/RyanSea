from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time

//uses a webdriver to swap twitter credentials — some of the web driver resorts to clicking at a pixel location and is dependant on a given screen size

handle = 'HandleSwapBot'
seller_password = 'SellerPass41'
#TODO: add hashing algo to create a temporary password & mailinator email 
buyer_password = 'BuyerPass42'
buyer_email = 'some_small_hash@mailinator.com'


#Opens Chrome and logs onto Twitter
browser = webdriver.Chrome()
browser.get('http://twitter.com/login')
time.sleep(1) #waits for page to fully load
handle_box = browser.find_element_by_name('session[username_or_email]')
password_box = browser.find_element_by_name('session[password]')
handle_box.send_keys(handle)
password_box.send_keys(seller_password)
login_button = browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div')
login_button.click()

#Initial authentication
browser.get('https://twitter.com/settings/your_twitter_data/account')
time.sleep(1)
current_password_box = browser.find_element_by_name('current_password')
current_password_box.send_keys(seller_password + Keys.RETURN)

#Swaps passwords
browser.get('https://twitter.com/settings/password')
time.sleep(1)
#actionchains allow for mouse controls & we click pixel of the appropriate input field (thank you Page Ruler Redux!)
ActionChains(browser).move_to_element_with_offset(browser.find_element_by_xpath('//*[@id="react-root"]'),850,90).click().send_keys(seller_password).perform()
ActionChains(browser).move_to_element_with_offset(browser.find_element_by_xpath('//*[@id="react-root"]'),850,200).click().send_keys(buyer_password).perform()
ActionChains(browser).move_to_element_with_offset(browser.find_element_by_xpath('//*[@id="react-root"]'),850,280).click().send_keys(buyer_password).perform()
ActionChains(browser).move_to_element_with_offset(browser.find_element_by_xpath('//*[@id="react-root"]'),1100,380).click().perform()
time.sleep(10)

#Swap emails part 1 - change credentials
browser.get('https://twitter.com/settings/email')
time.sleep(1)
ActionChains(browser).move_to_element_with_offset(browser.find_element_by_xpath('//*[@id="react-root"]'),850,180).click().perform()
time.sleep(1)
ActionChains(browser).move_to_element_with_offset(browser.find_element_by_xpath('//*[@id="layers"]'),500,200).click().send_keys(buyer_password).perform()
time.sleep(1)
ActionChains(browser).move_to_element_with_offset(browser.find_element_by_xpath('//*[@id="layers"]'),850,60).click().perform()
time.sleep(1)
ActionChains(browser).move_to_element_with_offset(browser.find_element_by_xpath('//*[@id="layers"]'),500,250).click().send_keys(buyer_email).perform()
time.sleep(2)
ActionChains(browser).move_to_element_with_offset(browser.find_element_by_xpath('//*[@id="layers"]'),850,60).click().perform()

#Swap emails part 2 - grab verification code
browser.execute_script('window.open('');')
browser.switch_to.window(browser.window_handles[1]) #creates a new tab and goes to that tab
browser.get('https://www.mailinator.com')
time.sleep(8) #we want to ensure mailinator has received the email
email_input = browser.find_element_by_id('addOverlay')
email_input.send_keys(buyer_email)
browser.find_element_by_id('go-to-public').click()
time.sleep(1)
text = browser.find_element_by_tag_name("body").get_attribute("innerText").splitlines() #creates an array of all text, split by new lines
#code is 2 indexes after 'GO', it looks like '\tTwitter\t117513 is your Twitter verification code'
code = text[text.index('GO') + 2].split(' ')[0].split('\t')[2] #so we grab that index, split it to get 'tTwitter\t117513', then split that by \t
browser.switch_to.window(browser.window_handles[0])
ActionChains(browser).move_to_element_with_offset(browser.find_element_by_xpath('//*[@id="layers"]'),500,200).click().send_keys(code).perform()
ActionChains(browser).move_to_element_with_offset(browser.find_element_by_xpath('//*[@id="layers"]'),850,60).click().perform()

#TODO: Create an escrow phone number to receive confirmation codes, otherwise this works
#browser.get('https://twitter.com/i/flow/add_phone')
#time.sleep(5)
#
#password_box = browser.find_element_by_name('password')
#password_box.send_keys(password)
#time.sleep(5)
#ActionChains(browser).move_to_element_with_offset(browser.find_element_by_xpath('//*[@id="react-root"]'),850,60).click().perform()
#time.sleep(5)
#
#password_box = browser.find_element_by_name('phone_number')
#password_box.send_keys('')
#time.sleep(5)
#ActionChains(browser).move_to_element_with_offset(browser.find_element_by_xpath('//*[@id="layers"]'),850,60).click().perform()
#time.sleep(5)
#ActionChains(browser).move_to_element_with_offset(browser.find_element_by_xpath('//*[@id="layers"]'),660,375).click().perform()

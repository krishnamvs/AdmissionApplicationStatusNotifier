from selenium import webdriver
import smtplib
import time
import DataOfUser
# Create the ChromeDriver Object
driver = webdriver.Chrome()
# Initialize the Message that you want to send
MailMessage = ''
# Dictionaries to hold various tag info based on the University
UniversityNameToUsernameTag={'Northeastern Univeristy':'ay-login',
              'Purdue University':'email',
              'Georgia Tech':'j_username',
              'North Carolina State University':'email'}
UniversityNameToPasswordTag={'Northeastern Univeristy':'ay-password',
              'Purdue University':'password',
              'Georgia Tech':'j_password',
              'North Carolina State University':'password'}
UniversityNameToButtonTag = {'Northeastern Univeristy':'ay-loginSubmit',
              'Purdue University':'//*[@id="content"]/form/table/tbody/tr/td[1]/div/button',
              'Georgia Tech':'_eventId_proceed',
              'North Carolina State University':'//*[@id="content"]/form/table/tbody/tr/td[1]/div/button'}
UniversityNameToUniversityURL = {'Northeastern Univeristy':'https://app.applyyourself.com/AYApplicantLogin/fl_ApplicantConnectLogin.asp?id=neu-grad',
       'Purdue University':'https://gradapply.purdue.edu/account/login?r=https%3a%2f%2fgradapply.purdue.edu%2fapply%2f',
       'Georgia Tech':'https://www.applyweb.com/cgi-bin/ustat',
       'North Carolina State University':'https://applygrad.ncsu.edu/apply/'}
# Get Userdata from DataOfUser.py file
Universities = Data[0::4]
Courses = Data[1::4]
Usernames = Data[2::4]
Passwords = Data[3::4]
# Go to the Univeristy website, login and collect the Admission Status
for Index in range(len(Universities)):
    UniversityURL = UniversityNameToUniversityURL[Universities[Index]]
    University = Universites[Index]
    Course = Courses[Index]
    Username = Usernames[Index]
    Password = Passwords[Index]
    try: 
        driver.get(UniversityURL)
        time.sleep(10)
        MailMessage = MailMessage + University + ' - ' + Course +'\n';
        if 'Carolina' in University:
            driver.find_element_by_id('_pc_1').click()
            time.sleep(10)
            driver.find_element_by_xpath('//*[@id="content"]/table/tbody/tr/td[1]/b/a').click()
            time.sleep(10)
        username_textbox = driver.find_element_by_id(UniversityNameToUsernameTag[University])
        username_textbox.send_keys(Username)
        password_textbox = driver.find_element_by_id(UniversityNameToPasswordTag[University])
        password_textbox.send_keys(Password)
        time.sleep(10)
        driver.find_element_by_id(UniversityNameToButtonTag[University]).click()
        time.sleep(10)
        if 'Northeastern' in University:
            status = driver.find_element_by_xpath('//*[@id="appList"]/li/ul/li[1]/ul/li[2]/h4').text
            driver.find_element_by_xpath('//*[@id="btncontrol"]/ul/a[4]').click()
        elif 'Purdue' in University:
            driver.find_element_by_xpath('//*[@id="content"]/table/tbody/tr/td[1]/div/a').click()
            time.sleep(10)
            driver.find_element_by_xpath('/html/body/div[10]/div/div/form/div[3]/button[1]').click()
            time.sleep(10)
            status = driver.find_element_by_xpath('//*[@id="content"]/p[1]/strong').text
        elif 'Georgia' in University:
            driver.find_element_by_xpath('//*[@id="ufe-content"]/div[1]/div[2]/div[2]/div[5]/div[2]/div/div/a').click()
            time.sleep(10)
            status = driver.find_element_by_xpath('//*[@id="checkListTrigger-82842925"]/div/div/div[2]/fieldset[2]/div[2]/div/dl/dd').text
        elif 'Carolina' in University:
            driver.find_element_by_xpath('//*[@id="content"]/table/tbody/tr/td[1]/div/a').click()
            time.sleep(10)
            driver.find_element_by_xpath('/html/body/div[4]/div/div/form/div[3]/button[1]').click()
            time.sleep(10)
            if 'Status Update' in driver.page_source:
                status = 'Status updated'
            else:
                status = 'Status not updated'
    except:
        status = 'Errored out'
        print(UniversityURL + ' has errored out!')
    MailMessage = MailMessage + status + '\n' + '\n'
driver.close()
driver.quit()
# Mail the Data(MailMessage) collected
mail = smtplib.SMTP('smtp.gmail.com', 587)
mail.starttls()
mail.login(SenderID, SenderPassword)
mail.sendmail(SenderID, ReceiverID, MailMessage)
mail.quit()
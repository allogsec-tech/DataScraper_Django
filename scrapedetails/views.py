from django.shortcuts import render
from django.http import HttpResponse
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from parsel import Selector

client = MongoClient('mongodb://localhost:27017/')
db = client['search_data']
collection = db["data"]
htmldata = {}

data1 = {}

results={}
results["instagram"]=[]

result1={}
result1["quora"]=[]

result2={}
result2["twitter"]=[]

result3={}
result3["wiki"]=[]

result4={}
result4["research_gate"]=[]

result5={}
result5["facebook"]=[]

result6={}
result6["linkedIn"]=[]

driver = webdriver.Chrome(r'C:\Users\Karthik\django-projects\DataScraper\scrapedetails\chromedriver.exe')





# Create your views here.
def start(request):
    return render(request, 'home.html')

def search(request):
    name = request.GET['keyword']
    print(name)
    
    driver.maximize_window()

   
    instagram(name)
    quora(name)
    twitter(name)
    wiki(name)
    facebook(name)
    # research_gate(name)
    linkedIn(name)
    collection.insert_one({"query":name,"data":data1})
    driver.quit()
    obj = collection.find().sort('_id', -1).limit(1)[0]['_id']
    print(obj)
    tmkc = collection.find({'_id':obj},{'_id':0,'data':1})
    for tmk in tmkc:
#         print(tmk)
        insta0 = (tmk['data']['instagram'])
        insta1 = insta0[0]
        print(insta1)
        htmldata['instagram'] = insta1
        quora0 = (tmk['data']['quora'])
        quora1 = quora0[0]
        print(quora1)
        htmldata['quora'] = (quora1)
        twitter0 = (tmk['data']['twitter'])
        twitter1 = twitter0[0]
        print(twitter1)
        htmldata['twitter'] = (twitter1)
        wiki0 = (tmk['data']['wiki'])
        wiki1 = wiki0[0]
        print(wiki1)
        htmldata['wiki'] = (wiki1)
        facebook0 = (tmk['data']['facebook'])
        facebook1 = facebook0[0]
        print(facebook1)
        htmldata['facebook'] = (facebook1)
        linkedIn0 = (tmk['data']['linkedIn'])
        linkedIn1 = linkedIn0[0]
        print(linkedIn1)
        htmldata['linkedin'] = (linkedIn1)
        print(htmldata)

    return render(request, 'home.html', htmldata)


def check_basicinfo(info, basicdata):
    if (info == "Birthday"):
        birthdate = basicdata
    elif (info == "Gender"):
        gender = basicdata
    elif (info == "Interested In"):
        interested = basicdata

def validate_field(field):
    if field:
        pass
    else:
        field = 'No Results'
    return field

def instagram(name):
    
    
    driver.get('https://google.com')
    search_query = driver.find_element_by_name('q')
    search_query.send_keys('site:instagram.com/ AND ' + name)
    search_query.send_keys(Keys.RETURN)
    insta_id = driver.find_elements_by_class_name('iUh30')

    insta_id= [url.text for url in insta_id]
    sleep(0.5)
    print("instagram has started to scrape")
    for ID_link in insta_id:
        driver.get(ID_link)

        sel = Selector(text = driver.page_source)

        user_id = sel.xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/h1/text()').extract_first()
        
        user_name = sel.xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]/h1/text()').extract_first()
        
        bios = ""
        user_bio = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]/span')
        for bio in user_bio:
            bios += bio.text
        

        
        user_id = validate_field(user_id)
        user_name = validate_field(user_name)
    
    
        results["instagram"].append({"Name":user_name,"ID":user_id,"BioData":bios})    
    data1.update(results)

def quora(name):
    
     
    driver.execute_script("window.open('https://www.quora.com/', 'tab2');")
    driver.switch_to.window("tab2")
    
    sleep(2)
    
    email = driver.find_elements_by_xpath("//input[@class='text header_login_text_box ignore_interaction']")[0]
    email.send_keys('')#Enter your email
    sleep(1)
    
    password = driver.find_elements_by_xpath("//input[@class='text header_login_text_box ignore_interaction']")[1]
    password.send_keys('')#Enter your password
    sleep(1)
    
    driver.find_element_by_xpath("//input[@class='submit_button ignore_interaction']").click()
    sleep(2)
    
    for i in name:
        driver.find_element_by_xpath("//input[@class='selector_input text']").send_keys(i)
        sleep(1)
    
    driver.find_element_by_xpath("//input[@class='selector_input text']").send_keys(u'\ue007')
    sleep(5)
    

    quora_urls = driver.find_elements_by_class_name('user')

    quora_urls= [url.get_attribute('href') for url in quora_urls]
    print("QUORA has started to scrape")
    
    for quora_url in quora_urls:
#         print(quora_url)
        try:
            driver.get(quora_url)
        except Exception as e:
            pass

        sel = Selector(text = driver.page_source)

        name_xpath = sel.xpath('//*[@class="ProfileNameAndSig"]//span[@class="user"]/text()').extract_first()
        if name_xpath:
            name_xpath.strip()
        
        description_1_xpath = sel.xpath('//*[@class="ProfileNameAndSig"]/span/span/text()').extract_first()
        description_2_xpath = sel.xpath('//*[@class="ProfileDescription"]//text()').extract_first()
        
        desc = str(description_1_xpath) +","+ str(description_2_xpath)
        
        school_xpath = sel.xpath('//*[contains(@class,"SchoolCredentialListItem")]//span[@class="UserCredential"]/text()').extract_first()
        
        school_passing_date_xpath= sel.xpath('//*[contains(@class,"SchoolCredentialListItem")]//span[@class="detail_text"]/text()').extract_first()
        
        work_xpath = sel.xpath('//*[contains(@class,"WorkCredentialListItem")]//span[@class="UserCredential"]/text()').extract_first()

        work_duration = sel.xpath('//div[contains(@class,"WorkCredentialListItem")]//span[@class="detail_text"]/text()').extract_first()
        
        location_xapth = sel.xpath('//*[contains(@class,"LocationCredentialListItem")]//span[@class="UserCredential"]/text()').extract_first()
        
        knowledge = ""
        sleep(0.5)
        knowledge_about_xpath = driver.find_elements_by_xpath('//div[@class="topic_info"]/a//span[contains(@class,"TopicNameSpan")]')
        for knowledge_about in knowledge_about_xpath:
            knowledge += knowledge_about.text+ "\n"
        
        
        name_xpath = validate_field(name_xpath)
        desc = validate_field(desc)
        school_xpath = validate_field(school_xpath)
        school_passing_date_xpath = validate_field(school_passing_date_xpath)
        work_xpath = validate_field(work_xpath)
        work_duration = validate_field(work_duration)
        location_xapth =validate_field(location_xapth)
        knowledge = validate_field(knowledge)
        
        if(name_xpath != "Karthik Mudaliar"):
        
            result1["quora"].append({"Name":name_xpath,"Description":desc,"School":school_xpath,"SchoolPassingDate":school_passing_date_xpath,"work":work_xpath,"WorkDuration":work_duration,"location":location_xapth,"knowledge":knowledge})    

    data1.update(result1)
    
    
def twitter(name):
    user_links = []
    count = 0
    
    driver.execute_script("window.open('https://twitter.com/', 'tab3');")
    driver.switch_to.window("tab3")
    sleep(4)
    
    username = driver.find_element_by_class_name('js-signin-email')
    username.click()
    username.send_keys('')#Enter your mailid
    sleep(2)
    password = driver.find_element_by_name('session[password]')
    password.click()
    password.send_keys('')#Enter your password
    sleep(2)
    login = driver.find_element_by_class_name('EdgeButton')
    login.click()
    sleep(2)
    searchuser = driver.find_element_by_id('search-query')
    searchuser.click()
    searchuser.send_keys(name)
    sleep(2)
    searchbtn = driver.find_element_by_class_name('search-icon')
    searchbtn.click()
    sleep(2)
    people = driver.find_element_by_css_selector('a[data-nav="search_filter_users"]')
#     print(people.text)
    people.click()
    sleep(2)
    profile = driver.find_elements_by_class_name('ProfileCard-bg')
    for i in profile:
        user_links.append(i.get_attribute("href"))
#     print(user_links)
    print("twitter has started to scrape")
    for j in user_links:
#         print(j)
        driver.get(j)
        sleep(2)
        userid = driver.find_element_by_class_name('ProfileHeaderCard-screennameLink').text
        
        location = driver.find_element_by_class_name('ProfileHeaderCard-locationText').text

        join_date = driver.find_element_by_class_name('ProfileHeaderCard-joinDateText').text

        birthdate = driver.find_element_by_class_name('ProfileHeaderCard-birthdateText').text

        tweet_bio = ""
        user_bio = driver.find_elements_by_xpath('//*[@id="page-container"]/div[2]/div/div/div[1]/div/div/div/div[1]/p')
        for bio in user_bio:
            tweet_bio += bio.text
            
            
        userid = validate_field(userid)
        location = validate_field(location)
        join_date = validate_field(join_date)
        birthdate = validate_field(birthdate)
        tweet_bio = validate_field(tweet_bio)    
            
        result2["twitter"].append({"userid":userid,"location":location,"join_date":join_date,"birthdate":birthdate,"links":j, "Bio":tweet_bio})
    
    data1.update(result2)  
    

    
def wiki(name):
    


    driver.execute_script("window.open('https://www.google.com', 'tab4');")
    driver.switch_to.window("tab4")

    search_query = driver.find_element_by_name('q')

    search_query.send_keys('site:wikipedia.org/ AND ' + name)
    search_query.send_keys(Keys.RETURN)

    Wiki_urls = driver.find_elements_by_xpath('//div[@class="r"]/a[1]')

    Wiki_urls= [url.get_attribute('href') for url in Wiki_urls]
    sleep(0.5)
    print("wiki has started to scrape")

    for Wiki_url in Wiki_urls:
        driver.get(Wiki_url)

        sel = Selector(text = driver.page_source)

        name_xpath = sel.xpath('//*[@id="firstHeading"]/text()').extract_first()
        

        try:
            description = ""
            description_xpath = driver.find_element_by_xpath('//*[@id="mw-content-text"]/div/p[2]')
            
            description = description_xpath.text
        except:
            pass
        
        search_results = ""
        search_string = driver.find_elements_by_xpath('html/body//*[contains(text(),"Shubham")]')
        for search in search_string:
            search_results += search.text + '\n'
        
        
        name_xpath = validate_field(name_xpath)
        description = validate_field(description)
        search_results = validate_field(search_results)
        Wiki_url = validate_field(Wiki_url)
    
    
        result3["wiki"].append({"Name":name_xpath,"Description":description,"SearchData":search_results,"WikiLink":Wiki_url})    
#     collection.insert_one(result3)
    data1.update(result3)
    
    
def facebook(name):
    

    driver.execute_script("window.open('https://mbasic.facebook.com', 'tab6');")
    driver.switch_to.window("tab6")
    sleep(2)
    birthdate = "No Results"
    gender = "No Results"

    


    user_links = []
    
    email = driver.find_element_by_id('m_login_email')
    email.send_keys('')#Enter your email
    password = driver.find_element_by_name('pass')
    password.send_keys('')#Enter your password
    login = driver.find_element_by_name('login')
    login.click()
    ok = driver.find_element_by_class_name('bp')
    ok.click()
    query = driver.find_element_by_name('query')
    query.send_keys(name)
    query.send_keys(u'\ue007');
    moreResults = driver.find_element_by_class_name('cu')
    moreResults.click()
    profile = driver.find_elements_by_xpath('//table/tbody/tr/td[1]/a')
    for i in profile:
        user_links.append(i.get_attribute("href"))
    print("Facebook has started to scrape")
    for j in user_links:
        driver.get(j)
        sleep(0.5)
        data_living = {}
        contact_data = {}
        basic_data = {}

        
        
        try:
            about = driver.find_element_by_xpath('//*[@id="m-timeline-cover-section"]/div[3]/a[1]')
            about.click()
        except NoSuchElementException as e:
            pass
            
        try:
            fbname = driver.find_element_by_xpath('//span/div/span/strong').text
        except NoSuchElementException as e:
            fbname = "No Results"
            
        try:
            edu = driver.find_element_by_xpath('//div/div[1]/div[1]/div/span/a').text
        except NoSuchElementException as e:
            edu = "No Results"

            
        try:
            
            living = driver.find_element_by_id('living')
        
            if (living != None):
                keys = living.find_elements_by_tag_name("span")
                places = living.find_elements_by_tag_name("a")
                keys = [key.text for key in keys]
                i = 1
                for place in places:
                    if (place.text not in keys):
                        data_living.update({keys[i] : place.text})
                        i = i + 1

        except NoSuchElementException as e:
            data_living = "No Results"

            
        try:
            contact1 = driver.find_element_by_xpath('//*[@id="contact-info"]/div/div[2]/div[1]/table/tbody/tr/td[1]/div/span').text
            contact1data = driver.find_element_by_xpath('//*[@id="contact-info"]/div/div[2]/div[1]/table/tbody/tr/td[2]/div').text
            contact_data.update({contact1:contact1data})
        except NoSuchElementException as e:
            pass
        
        try:
            contact2 = driver.find_element_by_xpath('//*[@id="contact-info"]/div/div[2]/div[2]/table/tbody/tr/td[1]/div/span').text
            contact2data = driver.find_element_by_xpath('//*[@id="contact-info"]/div/div[2]/div[2]/table/tbody/tr/td[2]/div').text
            contact_data.update({contact2:contact2data})
        except NoSuchElementException as e:
            pass
            

        try:
            contact3 = driver.find_element_by_xpath('//*[@id="contact-info"]/div/div[2]/div[3]/table/tbody/tr/td[1]/div/span').text
            contact3data = driver.find_element_by_xpath('//*[@id="contact-info"]/div/div[2]/div[3]/table/tbody/tr/td[2]/div').text
            contact_data.update({contact3:contact3data})
        except NoSuchElementException as e:
            pass


        try:
            basicInfo1 = driver.find_element_by_xpath('//*[@id="basic-info"]/div/div[2]/div[1]/table/tbody/tr/td[1]/div/span').text
            basicdata1 = driver.find_element_by_xpath('//*[@id="basic-info"]/div/div[2]/div[1]/table/tbody/tr/td[2]/div').text
            basic_data.update({basicInfo1:basicdata1})                                              
        except NoSuchElementException as e:
            pass
  
              
        try:
            basicInfo2 = driver.find_element_by_xpath('//*[@id="basic-info"]/div/div[2]/div[2]/table/tbody/tr/td[1]/div/span').text
            basicdata2 = driver.find_element_by_xpath('//*[@id="basic-info"]/div/div[2]/div[2]/table/tbody/tr/td[2]/div').text
            basic_data.update({basicInfo2:basicdata2})    
        except NoSuchElementException as e:
            pass
            
#         print(basic_data)
#         print(contact_data)
#         print("==================================================")
            
        if(fbname != "No Results"):
            
            result5["facebook"].append({"Name":fbname,"Education":edu,"Places":data_living,"ContactData":contact_data,"BasicData":basic_data})

    data1.update(result5)
            
        
        
        
def research_gate(name):
    
    
    driver.execute_script("window.open('https://www.google.com', 'tab5');")
    driver.switch_to.window("tab5")

    search_query = driver.find_element_by_name('q')

    search_query.send_keys('site:researchgate.net/ AND ' + name)
    search_query.send_keys(Keys.RETURN)

    research_gate_urls = driver.find_elements_by_xpath('//div[@class="r"]/a')

    research_gate_urls= [url.get_attribute('href') for url in research_gate_urls]
    print("RG has started to scrape")

    for research_gate_url in research_gate_urls:
        driver.get(research_gate_url)

        sel = Selector(text = driver.page_source)

        rgname = sel.xpath('//*[contains(@class,"fn")]/text()').extract_first()
        

        institute_name = sel.xpath('//h1//div[contains(@class,"nova-e-text nova-e-text--size-m nova-e-text--family-sans-serif nova-e-text--spacing")]/span[1]/text()').extract_first()
        

        fos = sel.xpath('//h1//div[contains(@class,"nova-e-text nova-e-text--size-m nova-e-text--family-sans-serif nova-e-text--spacing")]/span[2]/text() | //h1//div[contains(@class,"nova-e-text nova-e-text--size-m nova-e-text--family-sans-serif nova-e-text--spacing")]/text()[2] | //h1//div[contains(@class,"nova-e-text nova-e-text--size-m nova-e-text--family-sans-serif nova-e-text--spacing")]/a[2]/text()').extract_first()
        

        degree = sel.xpath('//*[@class="nova-e-text nova-e-text--size-m nova-e-text--family-sans-serif nova-e-text--spacing-none nova-e-text--color-inherit info-header"]/span/text()[2]').extract_first()
        

        skill_set = ""
        skills = driver.find_elements_by_xpath('//*[(@class="nova-l-flex__item nova-l-flex nova-l-flex--gutter-xxs nova-l-flex--direction-row@s-up nova-l-flex--align-items-stretch@s-up nova-l-flex--justify-content-flex-start@s-up nova-l-flex--wrap-wrap@s-up")]/div/a')
        for skill in skills:
            skill_set += skill.text +(',')
        

        citations = ""
        research_citation = driver.find_elements_by_xpath('//*[@class="nova-v-publication-item__stack nova-v-publication-item__stack--gutter-m"]//a[contains(@class,"nova-e-link nova-e-link--color-inherit nova-e-link--theme-bare")]')
        for research in research_citation:
            citations += research.text +('\n')
        

        citations_links = ""
        research_citation_link = driver.find_elements_by_xpath('//*[@class="nova-v-publication-item__stack nova-v-publication-item__stack--gutter-m"]//a[contains(@class,"nova-e-link nova-e-link--color-inherit nova-e-link--theme-bare")]') 
        for research_cit_link in research_citation_link:
            citations_links += research_cit_link.get_attribute('href')+ "\n"
        
        
        rgname = validate_field(name)
        institute_name = validate_field(institute_name)
        fos = validate_field(fos)
        degree = validate_field(degree)
        skill_set = validate_field(skill_set)
        citations = validate_field(citations)
        research_gate_url = validate_field(research_gate_url)
        
        
        result4["research_gate"].append({"Name":rgname,"Institution":institute_name,"Field of Study":fos,"Education Degree":degree,"Skills":skill_set,"Research Articles":citations,"Profile link":research_gate_url})    
    data1.update(result4)

    
def linkedIn(name):
    driver.execute_script("window.open('https://linkedin.com', 'tab7');")
    driver.switch_to.window("tab7")
    sleep(2)
    
    driver.find_element_by_class_name('nav__button-secondary').click()

    username = driver.find_element_by_id('username')
    username.send_keys('')#Enter your mail
    sleep(0.5)
    
    password = driver.find_element_by_id('password')
    password.send_keys('')#Enter your Password
    sleep(0.5)
    
    log_in_button = driver.find_element_by_class_name('btn__primary--large')
    log_in_button.click()
    sleep(2)
    
#     driver.execute_script("window.open('https:www.google.com', 'tab7');")
#     driver.get('https:www.google.com')
#     
#     search_query = driver.find_element_by_name('q')
#     #provide the required query in ""
#     search_query.send_keys('site:linkedin.com/in/ AND ' + name)
#     search_query.send_keys(Keys.RETURN)
#     sleep(3)
    search = driver.find_element_by_tag_name('input')
    search.click()
    search.send_keys(name)
    sleep(3)
    driver.find_element_by_tag_name('input').send_keys(Keys.ENTER)
    sleep(5)
    
    
    
#     linkedin_urls = driver.find_elements_by_class_name('iUh30')
    linkedin_urls = driver.find_elements_by_class_name('search-result__result-link')
    print("LinkedIn has started to scrape")

    linkedin_urls= [url.get_attribute('href') for url in linkedin_urls]
    linkedin_urls = list(set(linkedin_urls))
#     print(linkedin_urls)
    sleep(0.5)
    
    
    for linkedin_url in linkedin_urls:
#         print(linkedin_url)
        driver.get(linkedin_url)
        
        sleep(5)
    
        sel = Selector(text = driver.page_source)
        
        
        #name
        linkedInname = driver.find_element_by_class_name('inline').text
        
        if linkedInname:
            linkedInname = linkedInname.strip()
            
        #user_description
        user_description = sel.xpath('//*[@id="topcard"]/div[1]/div[2]/div/p/text() | //*[starts-with(@class, "pv-top-card-section__headline")]/text()').extract_first()
        
        if user_description:
            user_description = user_description.strip()
            
        #location
        user_location = sel.xpath('//*[starts-with(@class, "pv-top-card-section__location")]/text()').extract_first()
        if user_location:
            user_location = user_location.strip()
        
        #______________________summary ____________________________________________________________________________________
        
        summary_more_button = sel.xpath('//div[starts-with(@class,"pv-top-card-section__summary")]/button')
    
        summ = ""
        if summary_more_button:
            summary_button = driver.find_element_by_xpath('//div[starts-with(@class,"pv-top-card-section__summary")]/button').click()
            summary_details = driver.find_elements_by_xpath('//p[contains(@class,"pv-top-card-section__summary-text")]/span[contains(@class,"lt-line-clamp__raw-line")]')
        
            for summary in summary_details:
                summ += summary.text
                
        else:
        
            summary_details = driver.find_elements_by_xpath('//p[contains(@class,"pv-top-card-section__summary-text")]/span[contains(@class,"lt-line-clamp__line")]')
            
            for summary in summary_details:
                summ += summary.text
             
        #__________________________comapny and job details___________________________________________________________________
    
        #company current details(1)__________________________________________________________________________________________________________
        
        job_title_current = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][1]//li[contains(@class,"pv-position-entity ember-view")]//div[2]/h3/text()').extract_first()
        
        if job_title_current:
            job_title_current = job_title_current.strip()
        
        
        comapany_name_current = sel.xpath('//*[starts-with(@class, "pv-top-card-v2-section__entity-name pv-top-card-v2-section__company-name")]/text()').extract_first()
        
        if comapany_name_current:
            comapany_name_current = comapany_name_current.strip()
        
    
        job_duration_current = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][1]//li[contains(@class,"pv-position-entity ember-view")]//div[2]/div/h4[1]/span[2]/text()').extract_first()
        
        if job_duration_current:
            job_duration_current = job_duration_current.strip()
        
        
        job_location_current = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][1]//li[contains(@class,"pv-position-entity ember-view")]//div[2]/h4[2]/span[2]/text()').extract_first()
        
        if job_location_current:
            job_location_current = job_location_current.strip()
        
        
        experience_details_button = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][1]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__line")]/span/a')    
        
        exp_details_current = ""
        
        if experience_details_button:
            experience_details_button_click = driver.find_element_by_xpath('//*[contains(@class,"pv-profile-section__list-item")][1]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__line")]/span/*[@class="lt-line-clamp__more"]').click()
            #experience_details_button_click = driver.find_element_by_xpath('//*[contains(@class,"pv-profile-section__list-item")][1]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__line")]/span').click()
            sleep(0.5)
            experience_details = driver.find_elements_by_xpath('//*[contains(@class,"pv-profile-section__list-item")][1]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__raw-line")]')
    
            for details in experience_details:
                exp_details_current += details.text
            #print("in for loop")
        else:
            experience_details = driver.find_elements_by_xpath('//*[contains(@class,"pv-profile-section__list-item")][1]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__line")]')
    
            for details in experience_details:
                exp_details_current += details.text
            
        #last company details(2)_________________________________________________________________
        
        job_title_last = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][2]//li[contains(@class,"pv-position-entity ember-view")]//div[2]/h3/text()').extract_first()
        
        if job_title_last:
            job_title_last = job_title_last.strip()
    
        
        company_name_last = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][2]//li[contains(@class,"pv-position-entity ember-view")]//div[2]/h4[1]/span[2]/text()').extract_first()
        
        if company_name_last:
            company_name_last = company_name_last.strip()
            
    
        job_duration_last = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][2]//li[contains(@class,"pv-position-entity ember-view")]//div[2]/div/h4[1]/span[2]/text()').extract_first()
        
        if job_duration_last:
            job_duration_last = job_duration_last.strip()
        
        
        job_location_last = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][2]//li[contains(@class,"pv-position-entity ember-view")]//div[2]/h4[2]/span[2]/text()').extract_first()
        
        if job_location_last:
            job_location_last = job_location_last.strip()
        
        
        experience_details_button = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][2]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__line")]/span/a')    
        
        exp_details_last = ""
        
        if experience_details_button:
            experience_details_button_click = driver.find_element_by_xpath('//*[contains(@class,"pv-profile-section__list-item")][2]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__line")]/span/*[@class="lt-line-clamp__more"]').click()
            #experience_details_button_click = driver.find_element_by_xpath('//*[contains(@class,"pv-profile-section__list-item")][1]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__line")]/span').click()
            sleep(0.5)
            experience_details = driver.find_elements_by_xpath('//*[contains(@class,"pv-profile-section__list-item")][2]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__raw-line")]')
    
            for details in experience_details:
                exp_details_last += details.text
            #print("in for loop")
        else:
            experience_details = driver.find_elements_by_xpath('//*[contains(@class,"pv-profile-section__list-item")][2]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__line")]')
    
            for details in experience_details:
                exp_details_last += details.text
            
        #2nd last company details________________________________________________________    
            
        job_title_2_last = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][3]//li[contains(@class,"pv-position-entity ember-view")]//div[2]/h3/text()').extract_first()
        
        if job_title_2_last:
            job_title_2_last = job_title_2_last.strip()
        
        
        company_name_2_last = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][3]//li[contains(@class,"pv-position-entity ember-view")]//div[2]/h4[1]/span[2]/text()').extract_first()
        
        if company_name_2_last:
            company_name_2_last = company_name_2_last.strip()    
        
        
        job_duration_2_last = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][3]//li[contains(@class,"pv-position-entity ember-view")]//div[2]/div/h4[1]/span[2]/text()').extract_first()
        
        if job_duration_2_last:
            job_duration_2_last = job_duration_2_last.strip()
        
        
        job_location_2_last = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][3]//li[contains(@class,"pv-position-entity ember-view")]//div[2]/h4[2]/span[2]/text()').extract_first()
        
        if job_location_2_last:
            job_location_2_last = job_location_2_last.strip()
        
        
        experience_details_button = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][3]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__line")]/span/a')    
        
        exp_details_2_last = ""
        
        if experience_details_button:
            experience_details_button_click = driver.find_element_by_xpath('//*[contains(@class,"pv-profile-section__list-item")][3]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__line")]/span/*[@class="lt-line-clamp__more"]').click()
            sleep(0.5)
            experience_details = driver.find_elements_by_xpath('//*[contains(@class,"pv-profile-section__list-item")][3]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__raw-line")]')
    
            for details in experience_details:
                exp_details_2_last += details.text
            
        else:
            experience_details = driver.find_elements_by_xpath('//*[contains(@class,"pv-profile-section__list-item")][3]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__line")]')
    
            for details in experience_details:
                exp_details_2_last += details.text
            
        #3rd last company________________________________________________________________________________
        
        job_title_3_last = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][4]//li[contains(@class,"pv-position-entity ember-view")]//div[2]/h3/text()').extract_first()
        
        if job_title_3_last:
            job_title_3_last = job_title_3_last.strip()
    
        
        company_name_3_last = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][4]//li[contains(@class,"pv-position-entity ember-view")]//div[2]/h4[1]/span[2]/text()').extract_first()
        
        if company_name_3_last:
            company_name_3_last = company_name_3_last.strip()
    
        
        job_duration_3_last = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][4]//li[contains(@class,"pv-position-entity ember-view")]//div[2]/div/h4[1]/span[2]/text()').extract_first()
        
        if job_duration_3_last:
            job_duration_3_last = job_duration_3_last.strip()
            
        
        job_location_3_last = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][4]//li[contains(@class,"pv-position-entity ember-view")]//div[2]/h4[2]/span[2]/text()').extract_first()
        
        if job_location_3_last:
            job_location_3_last = job_location_3_last.strip()
            
    
        experience_details_button = sel.xpath('//*[contains(@class,"pv-profile-section__list-item")][4]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__line")]/span/a')    
        
        exp_details_3_last = ""
        
        if experience_details_button:
            experience_details_button_click = driver.find_element_by_xpath('//*[contains(@class,"pv-profile-section__list-item")][4]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__line")]/span/*[@class="lt-line-clamp__more"]').click()
            #experience_details_button_click = driver.find_element_by_xpath('//*[contains(@class,"pv-profile-section__list-item")][1]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__line")]/span').click()
            sleep(0.5)
            experience_details = driver.find_elements_by_xpath('//*[contains(@class,"pv-profile-section__list-item")][4]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__raw-line")]')
    
            for details in experience_details:
                exp_details_3_last += details.text
            #print("in for loop")
        else:
            experience_details = driver.find_elements_by_xpath('//*[contains(@class,"pv-profile-section__list-item")][4]//li[contains(@class,"pv-position-entity ember-view")]/div/p/span[contains(@class,"lt-line-clamp__line")]')
    
            for details in experience_details:
                exp_details_3_last += details.text
           
        #________________________schools and education_________________________________________________________________________
        try:
            flag = driver.find_element_by_css_selector('.education-section')
            driver.execute_script("arguments[0].scrollIntoView(true);", flag)
        except:
            pass
        sleep(1)
        
        #school(1)  xpath and logic - school name , degree , field of study , grades
        school_1 = sel.xpath('//li[1]//div[contains(@class,"pv-education-entity")][1]//h3[contains(@class,"pv-entity__school-name")]/text()|//li[1][contains(@class,"pv-education-entity")][1]//h3[contains(@class,"pv-entity__school-name")]/text()').extract_first()
    
        if school_1:
            school_1 = school_1.strip()
        
        school_1_degre = sel.xpath('//*[starts-with(@class,"pv-profile-section__section-info")]/li[1]//*[contains(@class,"pv-entity__degree-name")]/span[2]/text()').extract_first()
        
        if school_1_degre:
            school_1_degre = school_1_degre.strip()
    
    
        school_1_field = sel.xpath('//*[starts-with(@class,"pv-profile-section__section-info")]/li[1]//*[contains(@class,"pv-entity__fos")]/span[2]/text()').extract_first()
        
        if school_1_field:
            school_1_field = school_1_field.strip()
    
        school_1_grade = sel.xpath('//*[starts-with(@class,"pv-profile-section__section-info")]/li[1]//*[contains(@class,"pv-entity__grade")]/span[2]/text()').extract_first()
        
        if school_1_grade:
            school_1_grade = school_1_grade.strip()
    
        
        #school (2) xpath and logic - school name , degree , field of study , grades
        school_2 = sel.xpath('//*[starts-with(@class,"pv-profile-section__sortable-item")][2]//h3[contains(@class,"pv-entity__school-name")]/text()').extract_first()    
        
        if school_2:
            school_2 = school_2.strip()
    
        school_2_degre = sel.xpath('//*[starts-with(@class,"pv-profile-section__section-info")]/li[2]//*[contains(@class,"pv-entity__degree-name")]/span[2]/text()').extract_first()
        
        if school_2_degre:
            school_2_degre = school_2_degre.strip()
            
        school_2_field = sel.xpath('//*[starts-with(@class,"pv-profile-section__section-info")]/li[2]//*[contains(@class,"pv-entity__fos")]/span[2]/text()').extract_first()
        
        if school_2_field:
            school_2_field = school_2_field.strip()
    
        school_2_grade = sel.xpath('//*[starts-with(@class,"pv-profile-section__section-info")]/li[2]//*[contains(@class,"pv-entity__grade")]/span[2]/text()').extract_first()
    
        if school_2_grade:
            school_2_grade = school_2_grade.strip()
    
        
        #school (3) xpath and logic - school name , degree , field of study , grades
        school_3 = sel.xpath('//*[starts-with(@class,"pv-profile-section__sortable-item")][3]//h3[contains(@class,"pv-entity__school-name")]/text()').extract_first()
        
        if school_3:
            school_3 = school_3.strip()
    
        school_3_degre = sel.xpath('//*[starts-with(@class,"pv-profile-section__section-info")]/li[3]//*[contains(@class,"pv-entity__degree-name")]/span[2]/text()').extract_first()
        
        if school_3_degre:
            school_3_degre = school_3_degre.strip()
    
        school_3_field = sel.xpath('//*[starts-with(@class,"pv-profile-section__section-info")]/li[3]//*[contains(@class,"pv-entity__fos")]/span[2]/text()').extract_first()
        
        if school_3_field:
            school_3_field = school_3_field.strip()
    
        school_3_grade = sel.xpath('//*[starts-with(@class,"pv-profile-section__section-info")]/li[3]//*[contains(@class,"pv-entity__grade")]/span[2]/text()').extract_first()
        
        if school_3_grade:
            school_3_grade = school_3_grade.strip()
    
        
        #SCHOOL (4) xpath and logic - school name , degree , field of study , grades
        school_4 = sel.xpath('//*[starts-with(@class,"pv-profile-section__sortable-item")][4]//h3[contains(@class,"pv-entity__school-name")]/text()').extract_first()
        
        if school_4:
            school_4 = school_4.strip()
        
        school_4_degre = sel.xpath('//*[starts-with(@class,"pv-profile-section__section-info")]/li[4]//*[contains(@class,"pv-entity__degree-name")]/span[2]/text()').extract_first()
        
        if school_4_degre:
            school_4_degre = school_4_degre.strip()
    
        school_4_field = sel.xpath('//*[starts-with(@class,"pv-profile-section__section-info")]/li[4]//*[contains(@class,"pv-entity__fos")]/span[2]/text()').extract_first()    
        
        if school_4_field:
            school_4_field = school_4_field.strip()
    
        school_4_grade = sel.xpath('//*[starts-with(@class,"pv-profile-section__section-info")]/li[4]//*[contains(@class,"pv-entity__grade")]/span[2]/text()').extract_first()
        
        if school_4_grade:
            school_4_grade = school_4_grade.strip()
        
        
        try:
            flag = driver.find_element_by_css_selector('.volunteering-section')
            driver.execute_script("arguments[0].scrollIntoView(true);", flag)
        except:
            pass   
        #___________________________________skills_______________________________________________________________________
        try:
            flag = driver.find_element_by_css_selector('.pv-skill-categories-section')
            driver.execute_script("arguments[0].scrollIntoView(true);", flag)
        except:
            pass
        sleep(1)
        
        skill=""
        
        skill_more_button = driver.find_elements_by_xpath('//section[contains(@class,"pv-skill-categories-section")]/div/button')
        
        if skill_more_button:
            skill_more_button[0].click()
            skill_sets = driver.find_elements_by_xpath('//*[contains(@class,"pv-skill-category-entity")]//span[contains(@class,"pv-skill-category-entity__name")]')
            sleep(1)
            for skills in skill_sets:
                skill += skills.text + ","
                
        else:
            skill_sets = driver.find_elements_by_xpath('//*[contains(@class,"pv-skill-category-entity")]//span[contains(@class,"pv-skill-category-entity__name")]')
            sleep(1)
            for skills in skill_sets:
                skill += skills.text + ","
        #________________________________________________________________________________________________________________
        
    
        linkedin_url = driver.current_url
        
        # VALIDATION OF FIELDS
        linkedInname = validate_field(linkedInname)
        user_description = validate_field(user_description)
        comapany_name_current = validate_field(comapany_name_current)
        user_location = validate_field(user_location)
        linkedin_url = validate_field(linkedin_url)
        summ = validate_field(summ)
        company_name_last = validate_field(company_name_last)
        company_name_2_last = validate_field(company_name_2_last)
        company_name_3_last = validate_field(company_name_3_last)
        job_duration_current = validate_field(job_duration_current)
        job_duration_last = validate_field(job_duration_last)
        job_duration_2_last = validate_field(job_duration_2_last)
        job_duration_3_last = validate_field(job_duration_3_last)
        job_title_current = validate_field(job_title_current)
        job_title_last = validate_field(job_title_last)
        job_title_2_last = validate_field(job_title_2_last)
        job_title_3_last = validate_field(job_title_3_last)
        job_location_current = validate_field(job_location_current)
        job_location_last = validate_field(job_location_last)
        job_location_2_last = validate_field(job_location_2_last)
        job_location_3_last = validate_field(job_location_3_last)
        exp_details_current = validate_field(exp_details_current)
        exp_details_last = validate_field(exp_details_last)
        exp_details_2_last = validate_field(exp_details_2_last)
        exp_details_3_last = validate_field(exp_details_3_last)
        school_1 = validate_field(school_1)
        school_1_degre = validate_field(school_1_degre)
        school_1_field = validate_field(school_1_field)
        school_1_grade = validate_field(school_1_grade)
        school_2 = validate_field(school_2)
        school_2_degre = validate_field(school_2_degre)
        school_2_field = validate_field(school_2_field)
        school_2_grade = validate_field(school_2_grade)
        school_3 = validate_field(school_3)
        school_3_degre = validate_field(school_3_degre)
        school_3_field = validate_field(school_3_field)
        school_3_grade = validate_field(school_3_grade)
        school_4 = validate_field(school_4)
        school_4_degre = validate_field(school_4_degre)
        school_4_field = validate_field(school_4_field)
        school_4_grade = validate_field(school_4_grade)
        skill = validate_field(skill)
    
#         result6["linkedIn"].append({"Name":linkedInname,"User Description":user_description,"User Location":user_location,"Summary":summ,"skill":skill,"Current Job Title":job_title_current,"Current Company":comapany_name_current,"Current Job Location":job_location_current,"Current Job Duration":job_duration_current,"Current Job Details":exp_details_current,"Last Job Title":job_title_last,"Last Company":company_name_last,"Last Job Location":job_location_last,"Last Job Duration":job_duration_last,"Last Job Details":exp_details_last,"2nd Last Job Title":job_title_2_last,"2nd Last Company":company_name_2_last,"2nd Last Job Location":job_location_2_last,"2nd Last Job Duration":job_duration_2_last,"2nd Last Job Details":exp_details_2_last,"3rd Last Job Title":job_title_3_last,"3rd Last Company":company_name_3_last,"3nd Last Job Location":job_location_3_last,"3rd Last Job Duration":job_duration_3_last,"3rd Last Job Details":exp_details_3_last,"School 1":school_1,"School 1 Degree":school_1_degre,"School 1 Fos":school_1_field,"School 1 Grade":school_1_grade,"School 2":school_2,"School 2 Degree":school_2_degre,"School 2 Fos":school_2_field,"School 2 Grade":school_2_grade,"School 3":school_3,"School 3 Degree":school_3_degre,"School 3 Fos":school_3_field,"School 3 Grade":school_3_grade,"School 4":school_4,"School 4 Degree":school_4_degre,"School 4 Fos":school_4_field,"School 4 Grade":school_4_grade,"URL":linkedin_url})
        result6["linkedIn"].append({"Name":linkedInname,"UserDescription":user_description,"UserLocation":user_location,"Summary":summ,"skill":skill,"CurrentJobTitle":job_title_current,"CurrentCompany":comapany_name_current,"CurrentJobLocation":job_location_current,"CurrentJobDuration":job_duration_current,"CurrentJobDetails":exp_details_current,"URL":linkedin_url})    
    data1.update(result6)

        


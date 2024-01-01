from bs4 import BeautifulSoup
import json
import os
import re

class App:
    
    def __init__(self,url):
        self.url = url
            
    def scrapedata(self):
        profile_Data = {}
        profile_url = []
        skills = []
        req = open(self.url, encoding="utf8").read()
        makesoup = BeautifulSoup(req,'lxml')
        try:
            #profile_url
            profile_url.append(self.url)
            for url in makesoup.select('a[data-test-personal-info-profile-link]'):
                profile_Data['profile_url'] = url['href']
        except:
            pass
        try:
            for conect in makesoup.select('div[class="lockup__connections"] span[class="a11y-text"]'):
                profile_Data['Connection'] = conect.text.strip()
        except:
            pass
        try:
            #name
            for add in makesoup.select('head>title'):
                name = add.text.split(' ')
                profile_Data['Full Name'] = add.text
                profile_Data['First Name'] = name[0]
                profile_Data['Last Name'] = name[1]
        except:
            pass
        
        try:
            #Desgination
            for design in makesoup.select('section[class="lockup ember-view"] div[class*="artdeco-entity-lockup__content lockup__content"]>div[class*="artdeco-entity-lockup__subtitle"]'):
                profile_Data['Current Position'] = design.text.strip()
        except:
            pass
        
        try:
            #image

            for img in makesoup.select('section[class="lockup ember-view"] img'):
                profile_Data['photo_url'] = img['src']
        except:
            pass
        
        try:
            #location
            for loc in makesoup.select('section[class="lockup ember-view"] div[class="lockup__details"] div[data-test-row-lockup-location]'):
                profile_Data['Current Location'] = loc.text.strip()
        except:
            pass
        
        try:
            #Summary
            for sumry in makesoup.select('section[class="component-card summary-card"] div[class="ember-view"] span:nth-child(1)'):
                profile_Data['Summary'] = sumry.text.strip()
        except:
            pass
        
        try:
            #experinces
            expDict = {} 
            expDict['Experiences']= self.experincescrapedata(makesoup)
            profile_Data['Experiences'] = expDict
        except:
            pass
        
        try:
            #Education
            eduDict = {}
            eduDict['Educations'] = self.education(makesoup)
            profile_Data['Educations'] = eduDict
        except:
            pass
        
        try:
            #Certification
            certfDict = {}
            certfDict['Certifications'] = self.certificate(makesoup)
            profile_Data['Certifications'] = certfDict
        except:
            pass
        
        try:
            #Skills
            for skill in makesoup.select('ul[class="expandable-list-profile-core__list"]'):
                ulList = skill.find_all('dt')
                for li in ulList:
                    skills.append(li.text.strip())
            skillNames = (', ').join(skills)
            profile_Data['Skills'] = skillNames.strip()
        except:
            pass
        
        return profile_Data
    
    def experincescrapedata(self,makesoup):
        experiences = []
        
        for expul in makesoup.select('ul[class="expandable-list-profile-core__list artdeco-list"]'):
            ulList = expul.find_all('li')
            for li in ulList:
                dataExp = {}
                compnyName = ''
                compnyUrl = ''
                logoUrl = ''
                startDte = ''
                endDte = ''
                #company name
                if(li.select('dd[data-test-position-entity-company-name]')):
                    try:
                        if(li.select('dd[data-test-position-entity-company-name] a')):
                            for compname in li.select('dd[data-test-position-entity-company-name] a'):
                                compnyName = compname.text
                                compnyUrl = compname['href']
                        else:
                            for compname in li.select('dd[data-test-position-entity-company-name]'):
                                compnyName = compname.text
                                compnyUrl = ''
                    except:
                        compnyName = ''
                        compnyUrl = ''
                    
                    try:
                        for timedur in li.select('dd[class="background-entity__summary-definition--date-duration"]>span[data-test-position-entity-date-range]'):
                            durtime = timedur.text.split('–')
                            startDte = durtime[0]
                            endDte = durtime[1]
 
                    except:
                        startDte = ''
                        endDte = ''

                else:
                    try:
                        if(li.select('a[data-test-grouped-position-entity-company-link]')):
                            for compname in li.select('a[data-test-grouped-position-entity-company-link]'):
                                compnyName = compname.text
                                compnyUrl = compname['href']
                        else:
                            for compname in li.select('strong[data-test-grouped-position-entity-company-name]'):
                                compnyName = compname.text
                                compnyUrl = ''
                    except:
                        compnyName = ''
                        compnyUrl = ''
                    try:
                        count = len(li.select('span[data-test-grouped-position-entity-date-range]'))
                        for timedur,num in zip(li.select('span[data-test-grouped-position-entity-date-range]'),range(count)):
                            durtime = timedur.text.split('–')
                            if(num == 0):
                                endDte = durtime[1]
                            elif((num+1) == count):
                                startDte = durtime[0]
                            
                    except:
                        endDte = ''
                        startDte = ''
                
                try:
                    #logo
                    for logo in li.select('figure[class="logo-container background-entity__logo-container"] img'):
                        if 'http' in logo['src']:
                            logoUrl = logo['src']
                except:
                    logoUrl = ''
                
                
                dataExp['Company Name'] = compnyName.strip()
                dataExp['Company Url'] = compnyUrl.strip()
                dataExp['Logo Url'] = logoUrl.strip()
                dataExp['Start Date'] = startDte.strip()
                dataExp['End Date'] = endDte.strip()
                rolesdict = {}
                rolesdict['roles'] = self.roles(li)
                dataExp['roles'] = rolesdict
                experiences.append(dataExp)
        return experiences
    
    def roles(self,li):
        roles = []
        roleDes = {}
        jobTitle = ''
        startDte = ''
        endDte = ''
        location = ''
        descrpt = ''
        if(li.select('dd[data-test-position-entity-company-name]')):
            try:
                for designat in li.select('h3[class="background-entity__summary-definition--title"]'):
                    jobTitle = designat.text.strip()
            except:
                jobTitle =''
            
            try:
                for timedur in li.select('dd[class="background-entity__summary-definition--date-duration"]>span[data-test-position-entity-date-range]'):
                    durtime = timedur.text.split('–')
                    startDte = durtime[0]
                    endDte = durtime[1]
            except:
                startDte = ''
                endDte = ''
            try:
                for loc in li.select('dd[data-test-position-entity-location]'):
                    location = loc.text
            except:
                location =''
            
            try:
                for desc in li.select('dd[data-test-position-entity-description]'):
                    descrpt = desc.text
            except:
                descrpt =''
            roleDes['Job Title'] = jobTitle
            roleDes['Starting Date'] = startDte.strip()
            roleDes['Ending Date'] = endDte.strip()
            roleDes['Location'] = location.strip()
            roleDes['Description'] = descrpt.strip()
            roles.append(roleDes)
        else:
            if(li.select('span[data-test-grouped-position-entity-date-range]')):
                for designat,timedur,loc in zip(li.select('dd[data-test-grouped-position-entity-title]'),li.select('span[data-test-grouped-position-entity-date-range]'),li.select('dd[data-test-grouped-position-entity-location]')):
                    roleDes = {}
                    jobTitle = ''
                    startDte = ''
                    endDte = ''
                    location = ''
                    descrpt = ''
                    jobTitle= designat.text.strip()
                    durtime = timedur.text.split('–')
                    startDte = durtime[0]
                    endDte = durtime[1]
                    location = loc.text
                    descrpt = ''
                    roleDes['Job Title'] = jobTitle
                    roleDes['Starting Date'] = startDte.strip()
                    roleDes['Ending Date'] = endDte.strip()
                    roleDes['Location'] = location.strip()
                    roleDes['Description'] = descrpt
                    roles.append(roleDes)   
            else:
                for designat,loc in zip(li.select('dd[data-test-grouped-position-entity-title]'),li.select('dd[data-test-grouped-position-entity-location]')):
                    roleDes = {}
                    jobTitle = ''
                    startDte = ''
                    endDte = ''
                    location = ''
                    descrpt = ''
                    jobTitle= designat.text.strip()
                    location = loc.text
                    descrpt = ''
                    roleDes['Job Title'] = jobTitle
                    roleDes['Starting Date'] = ''
                    roleDes['Ending Date'] = ''
                    roleDes['Location'] = location.strip()
                    roleDes['Description'] = descrpt
                    roles.append(roleDes) 
                    
        return roles

            

    def education(self,makesoup):
        educations = []
        
        for edu in makesoup.select('ul[class="background-section__list"]'):
            ulList = edu.find_all('li')
            for li in ulList:
                dataEdu = {}
                eduName = ''
                eduDeg = ''
                eduFoc = ''
                eduStartDte = ''
                eduEndDte = ''
                logoUrl = ''
                #company name
                try:
                    if(li.select('h3[data-test-education-entity-school-name] a')):
                        for eduname in li.select('h3[data-test-education-entity-school-name] a'):
                            eduName = eduname.text
                            logoUrl = eduname['href']
                    else:
                        for eduname in li.select('h3[data-test-education-entity-school-name]'):
                            eduName = eduname.text
                            logoUrl = ''
                except:
                    eduName =''
                    logoUrl = ''

                try:
                    for degname in li.select('span[data-test-education-entity-degree-name]'):
                        eduDeg = degname.text
                except:
                    eduDeg = ''

                try:
                    for edufocus in li.select('span[data-test-education-entity-field-of-study]'):
                        eduFoc = edufocus.text.strip()
                except:
                    eduFoc =''

                try:
                    for timdur in li.select('dd[data-test-education-entity-dates]'):
                        durtime = timdur.text.split('–')
                        eduStartDte = durtime[0]
                        eduEndDte = durtime[1]
                except:
                    eduStartDte =''
                    eduEndDte = ''

                dataEdu['Education Name'] = eduName.strip()
                dataEdu['Education Degree'] = eduDeg.strip()
                dataEdu['Education Focus'] = eduFoc.strip()
                dataEdu['Education Start Year'] = eduStartDte.strip()
                dataEdu['Education End Year'] = eduEndDte.strip()
                dataEdu['Logo Url'] = logoUrl
                educations.append(dataEdu)
        return educations


    def certificate(self,makesoup):
        certificates = []
        
        for certi in makesoup.select('li[class="accomplishments-base-entity certification-entity ember-view"]'):
            ulList = certi.findAll("div",{"class":"accomplishments-base-entity ember-view"})
            for li in ulList:
                datacerticate = {}
                cerName = ''
                cerStartDte = ''
                cerEndDte = ''
                #certificate name
                try:
                    for cername in li.select('h3[data-test-accomplishments-base-entity-title]'):
                        cerName = cername.text
                except:
                    cerName = ''

                try:
                    for timdur in li.select('div[class="accomplishments-base-entity__date"]'):
                        durtime = timdur.text.split('–')
                        cerStartDte = durtime[0]
                        cerEndDte = durtime[1]
                except:
                    cerStartDte = ''
                    cerEndDte = ''

                datacerticate['Certificate Name'] = cerName.strip()
                datacerticate['Certificate Start Year'] = cerStartDte.strip()
                datacerticate['Certificate End Year'] = cerEndDte.strip()
                certificates.append(datacerticate)
        return certificates

if __name__ == '__main__':
    folderName = 'C:/Users/313/Desktop/LinkldIn_MAli'
    directoryName = ['Most Recent Job ending Present','Most Recent Job ending 2022','Most Recent Job ending 2021','Most Recent Job ending 2020','Most Recent Job ending all other years']
    def open_files_in_browser(folder_name):
        urls = []
        fileName = []
        for filename in os.listdir(folder_name):
            if filename.endswith(".html") or filename.endswith(".htm"):
                urls.append(os.path.join(folder_name, filename))
                fileName.append(filename)
        return [urls,fileName]
    [urls,fileName] = open_files_in_browser(f'{folderName}/Cache3/')
    for index in range(len(urls)):
        print(urls[index])
        app = App(urls[index])
        df = app.scrapedata()
        output = {}
        value = []
        value.append(df)
        output['profile_Data'] = value
        dictValue = output['profile_Data'][0]
        print(dictValue)
        if 'profile_url' in dictValue.keys():
            regex = r"\b(/d+)\b"
            s = output['profile_Data'][0]['Connection']
            conn_num = re.findall("\d+", s)
            conn_num = int(conn_num[0])
            try:
                exper_status = output['profile_Data'][0]['Experiences']['Experiences'][0]['End Date']
                print(exper_status)
                if exper_status == '':
                    exper_status = 'Other'
                else:
                    exper_status = exper_status
            except:
                exper_status = 'Other'
            if(exper_status == 'Present'):
                exper_status = 'Present'
            elif(exper_status == 'Other'):
                exper_status = 'Other'
            else:
                exper_status = re.findall("\d+", exper_status)
                exper_status = exper_status[0]
            if(conn_num >= 500):
                newpath = f'{folderName}/output/json/Greater than 500 connections' 
                for dirname in directoryName:
                    mkdirName = f'{newpath}/{dirname}'
                    if not os.path.exists(mkdirName):
                        os.makedirs(mkdirName)
                if(exper_status == 'Present'):
                    with open(f'{newpath}/Most Recent Job ending Present/{fileName[index]}.json', "w") as outfile:
                        json.dump(output, outfile, indent=4)
                elif(exper_status == '2022'):
                    with open(f'{newpath}/Most Recent Job ending 2022/{fileName[index]}.json', "w") as outfile:
                        json.dump(output, outfile, indent=4)
                elif(exper_status == '2021'):
                    with open(f'{newpath}/Most Recent Job ending 2021/{fileName[index]}.json', "w") as outfile:
                        json.dump(output, outfile, indent=4)
                elif(exper_status == '2020'):
                    with open(f'{newpath}/Most Recent Job ending 2020/{fileName[index]}.json', "w") as outfile:
                        json.dump(output, outfile, indent=4)
                else:
                    with open(f'{newpath}/Most Recent Job ending all other years/{fileName[index]}.json', "w") as outfile:
                        json.dump(output, outfile, indent=4)
            else:
                newpath = f'{folderName}/output/json/Fewer than 500 connections' 
                for dirname in directoryName:
                    mkdirName = f'{newpath}/{dirname}'
                    if not os.path.exists(mkdirName):
                        os.makedirs(mkdirName)
                if(exper_status == 'Present'):
                    with open(f'{newpath}/Most Recent Job ending Present/{fileName[index]}.json', "w") as outfile:
                        json.dump(output, outfile, indent=4)
                elif(exper_status == '2022'):
                    with open(f'{newpath}/Most Recent Job ending 2022/{fileName[index]}.json', "w") as outfile:
                        json.dump(output, outfile, indent=4)
                elif(exper_status == '2021'):
                    with open(f'{newpath}/Most Recent Job ending 2021/{fileName[index]}.json', "w") as outfile:
                        json.dump(output, outfile, indent=4)
                elif(exper_status == '2020'):
                    with open(f'{newpath}/Most Recent Job ending 2020/{fileName[index]}.json', "w") as outfile:
                        json.dump(output, outfile, indent=4)
                else:
                    with open(f'{newpath}/Most Recent Job ending all other years/{fileName[index]}.json', "w") as outfile:
                        json.dump(output, outfile, indent=4)
        else:
            print('Issue in Html file')

    print("Complete Now Thanks You")
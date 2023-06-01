import os
import asyncio
import concurrent.futures
import time
import sys

from urllib.parse import urlparse
from requests_html import AsyncHTMLSession

############################################################################################

BASE_FOLDER_PATH = './'
INPUT_DATA_FOLDER_PATH = os.path.join(BASE_FOLDER_PATH,'InputData')
OUTPUT_DATA_FOLDER_PATH = os.path.join(BASE_FOLDER_PATH,'OutputData')
COMPANY_DATA_FILE_PATH = os.path.join(INPUT_DATA_FOLDER_PATH,'companyWebsites.csv')

COMPANY_NAME_COL_NUM = 1
COMPANY_URL_COL_NUM = 6

MAX_CRAWL_DEPTH = 10000
MAX_CRAWL_LIST = 100
MAX_RENDER_TIME_OUT = 60
WAIT_TIME = 3
GET_TIME_OUT = 30

############################################################################################
def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

############################################################################################
def IsPDF(url):
    isPDF = False
    
    if '.pdf' in url: 
        isPDF = True
    
    return isPDF

############################################################################################
# This function reads all the companies and their URLs into a dict (name:url)
def GetCompanyDict(dataFileName = COMPANY_DATA_FILE_PATH):
 
    # Store the company names (key) and urls (values) in a dictionary
    companyDict = {}

    companyDataFile = open(dataFileName, 'r')
    lines = companyDataFile.readlines()

    for line in lines:
        lineSplit = line.split('^')
                
        if len(lineSplit) > COMPANY_URL_COL_NUM:
            companyName = lineSplit[COMPANY_NAME_COL_NUM]
            companyURL = lineSplit[COMPANY_URL_COL_NUM]
        
            companyDict[companyName] = companyURL
    
    return companyDict

############################################################################################
# This function scrapes all the links on the page which are in the same domain has the url
def ScrapeLocalLinks(webPageResponse, url):
    
    localLinkList = []
    
    if IsPDF(url):
            return localLinkList
    
    try:
        allLinkList = webPageResponse.html.absolute_links
        baseURLDomain = urlparse(webPageResponse.html.base_url).netloc
        
        localLinkList = []

        for link in allLinkList:
            if  urlparse(link).netloc == baseURLDomain:
                if is_valid(link):
                    localLinkList.append(link)
    except:
        return localLinkList
        
    return localLinkList
    
############################################################################################

async def Get(asyncSession, url, VERVOSE = False):         
    try:
        response  = await asyncSession.get(url, timeout = GET_TIME_OUT)

    except:
        response = None
    
    
    return response
    
def TaskFunctionGetResponses(asyncSession, urlsToGet):
    tasks = []
    
    for url in urlsToGet:
        tasks.append(Get(asyncSession, url))
        
    return tasks

############################################################################################

async def TaskManager(linksToCrawl):
    
    # initialize an HTTP session
    session = AsyncHTMLSession()
    
    getTasks = TaskFunctionGetResponses(session, linksToCrawl)   
    responses = await asyncio.gather(*getTasks)

    await session.close()
    
    return responses

############################################################################################
   
def CrawlDomain(company, domainURL):
     
    logFilePath =  os.path.join(OUTPUT_DATA_FOLDER_PATH, (company+'.dat').replace(' ', '_'))
    logFile = open(logFilePath,'w+')
 
    logFile.write('Crawling: '+ domainURL +'\n')
    
    crawledLinks = []
    linksToCrawl = [domainURL]    

    crawlCounter = 0
    failedURL = 0
        
    while len(linksToCrawl) > 0:       
        # Create a list of up 100 links to crawl
        nLinksCrawled = 0
        crawlList = []
        
        while len(crawlList) <= MAX_CRAWL_LIST and len(linksToCrawl) > 0:
            crawlList.append(linksToCrawl.pop())
            nLinksCrawled += 1
        
        # send the list of links to crawl to the TaskManager function
        results = asyncio.run(TaskManager(crawlList))

        # create a list of links and text found by the Tasks
        listOfFoundLinks = []
        for r in results:
            if r != None:
                listOfFoundLinks = listOfFoundLinks + ScrapeLocalLinks(r, r.url)
            else:
                failedURL += 1
        
        # update the list of links that have been crawled
        for link in crawlList:
            crawledLinks.append(link) 
        
        # add the new found links only if they are not in the list AND not already visited
        for newLink in listOfFoundLinks:
            if newLink not in crawledLinks and newLink not in linksToCrawl:
                linksToCrawl.append(newLink)
                                             
        
        # Update the depth of the crawl and end the search if MAX_CRAWL_DEPTH has been reached
        crawlCounter += nLinksCrawled

        logFile.write(str(crawlCounter)+','+str(nLinksCrawled)+','+str(len(linksToCrawl))+'\n')

        if crawlCounter >= MAX_CRAWL_DEPTH:
            break
     
    logFile.close()
    
    print('Done: ', company, flush=True)

############################################################################################
def Demo(companyDict):
         
    for company in companyDict.keys():    
        crawledLinks = CrawlDomain(company, companyDict[company])   
        
############################################################################################

def SubmitJobs(companyDict):

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for company in companyDict.keys():           
            domainURL = companyDict[company]
            executor.submit(CrawlDomain, company, domainURL)
            
        executor.shutdown(wait=False)
        
############################################################################################

if __name__ == '__main__':
    
    if len(sys.argv) == 2:
        companyDict = GetCompanyDict(COMPANY_DATA_FILE_PATH)
    
        if sys.argv[1] == 'multi':    
            print('Start submitting jobs')
            SubmitJobs(companyDict)
            print('Done submitting jobs') 
        elif sys.argv[1] == 'single':
            Demo(companyDict)
        else:
            print('[ERROR] Unknown command line args: ', sys.argv)
    else:
            print('[ERROR] Unknown # of command line args: ', len(sys.argv))  
            

        
        
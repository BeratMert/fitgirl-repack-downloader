from urllib.request import URLopener
from requests import get
from bs4 import BeautifulSoup
from pathlib import Path

class FitGirlRepacksScraper:
    def __init__(self, link):
        self.welcomeText = "asdas"
        self.link = link
        self.downloadLinks = []
    
    def checkLink(self):
        if "https://fitgirl-repacks.site/" not in self.link:
            print("Invalid link format. Example format: https://fitgirl-repacks.site/marvels-spider-man-remastered/")
            return

        self.getLinks()

    def getLinks(self):
        try:
            website = get(self.link)

            if website.status_code != 200:
                print(f"Failed to retrieve content from {self.link}. Status code: {website.status_code}")
                return

            soup = BeautifulSoup(website.content, 'html.parser')

            table = soup.find_all('div', class_='su-spoiler-content su-u-clearfix su-u-trim')

            for row in table:
                links = table[1].find_all("a", href=True)
                for link in links:
                    self.downloadLinks.append(link["href"])
            
            self.startDownload()

        except Exception as e:
            print(f"Error: {e}")
            return

    def startDownload(self):
        if not self.downloadLinks:
            print("No download links found.")
            return
        
        opener = URLopener()
        opener.addheader('User-Agent', 'whatever')

        for dLink in self.downloadLinks:
            try:

                website = get(dLink)

                if website.status_code != 200:
                    print(f"Failed to download from {dLink}. Status code: {website.status_code}")
                    continue

                soup = BeautifulSoup(website.content, 'html.parser')
                scripts = soup.find_all("script")

                # Find and process JavaScript code in <script> tags
                for script in scripts: 
                    js_code = script.get_text()
                    
                    #Check if a specific URL is present in the JavaScript code
                    if "https://fuckingfast.co/" in js_code:
                        start_index = js_code.find("https://fuckingfast.co/")
                        end_index = js_code.find('")', start_index)

                        if start_index != -1 and end_index != -1:
                            downlink = js_code[start_index:end_index]

                            dLink = dLink.split("#")
                            if len(dLink) > 1:
                                dLink = dLink[1]

                                p = Path(dLink)
                                if p.exists():
                                    print("All files are downloaded!")
                                    exit()
                                else:
                                    opener.retrieve(downlink, dLink)

                                print("Downloaded: ", dLink)

            except Exception as e:
                print(f"Error downloading : {e}")
                continue


if __name__ == "__main__":
    testLink = "https://fitgirl-repacks.site/marvels-spider-man-remastered/"
    print("Print game link what you download like this -> ", testLink)
    link = str(input("Paste Game Link: "))
    scraper = FitGirlRepacksScraper(link)
    scraper.checkLink()
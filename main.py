from urllib.request import URLopener
from requests import get
from bs4 import BeautifulSoup

class FitGirlRepacksScraper:
    def __init__(self, link):
        self.welcomeText = "asdas"
        self.link = link
        self.downloadLinks = []
    
    def checkLink(self):
        if "https://fitgirl-repacks.site/" in self.link:

            self.getLinks()

        else:
            print("You need to paste a link like this -> https://fitgirl-repacks.site/marvels-spider-man-remastered/")

    def getLinks(self):
        try:
            website = get(self.link)

            soup = BeautifulSoup(website.content, 'html.parser')

            table = soup.find_all('div', attrs = {'su-spoiler-content su-u-clearfix su-u-trim'})

            for row in table[1].find_all("a", href=True):
                self.downloadLinks.append(row["href"])
            
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
                soup = BeautifulSoup(website.content, 'html.parser')

                # Find and process JavaScript code in <script> tags
                for script in soup.find_all("script"): 
                    js_code = script.get_text()
                    
                    #Check if a specific URL is present in the JavaScript code
                    if "https://fuckingfast.co/" in js_code:
                        test = js_code.split('https://fuckingfast.co/')
                        test = test[1].split('")')

                        downlink = "https://fuckingfast.co/" + test[0]

                        dLink = dLink.split("#")
                        dLink = dLink[1]

                        opener.retrieve(downlink, dLink)

                        print("Downloaded: ", dLink)

            except Exception as e:
                print(f"Error downloading : {e}")
                return


if __name__ == "__main__":
    # link = "https://fitgirl-repacks.site/marvels-spider-man-remastered/"
    link = str(input("Paste link: "))
    scraper = FitGirlRepacksScraper(link)
    scraper.checkLink()
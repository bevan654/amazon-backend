import requests
from utility import *
import random
import threading
proxies = Data().loadProxies('proxies.txt')



affliate = {
    'B08HLWDMFQ':'https://amzn.to/35tqSUy',
    'B08HHV8945':'https://amzn.to/3sr5dFJ'
}

class Task:
    def __init__(self,asin):

        self.lastRequest = None

        self.availability = 'OUT_OF_STOCK'

        self.asin = asin
        self.data = {
            "requestContext": {
                "obfuscatedMarketplaceId": "A39IBJ37TRP1C6",
                "obfuscatedMerchantId": "A39IBJ37TRP1C6",
                "language": "en-US",
                "sessionId": "",
                "currency": "AUD",
                "amazonApiAjaxEndpoint": "data.amazon.com.au"
            },
            "content": {
                "includeOutOfStock": True
            },
            "includeOutOfStock": True,
            "endpoint": "ajax-data",
            "ASINList": [
                self.asin
            ]
        }

        try:

            self.affiliate_link = affliate[asin]
        except:
            self.affiliate_link = 'https://www.amazon.com.au/-/dp/'+asin+'/'

        self.start()

    def LOG(self,text):
        print(f'[{self.asin}] :: {text}')

    def sendWebhook(self,title,image):
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/944541621884682291/oYE7wPvm52hR4hoX8uzEonxAoy-Sd0hVQ9imhwWS97-Y3LQDGG9niGDUOeVRoyCYy5kJ')

        embed = DiscordEmbed(title=title, color=15158332,url=self.affiliate_link)

        embed.set_author(name='https://www.amazon.com.au')


        embed.set_thumbnail(url=image)

        embed.set_footer(text='Powered By Genesis', icon_url='https://media.discordapp.net/attachments/904022469512396861/904022677109497907/Genesis_AIO_logo_black.png?width=1026&height=1026')

        embed.set_timestamp()

        embed.add_embed_field(name='ASIN', value=self.asin,inline=False)

        embed.add_embed_field(name='STATUS', value=str(self.availability),inline=False)
        embed.add_embed_field(name='LINKS', value=f'**[Product Link]({self.affiliate_link}) | [Cart](https://www.amazon.com.au/gp/cart/view.html)**',inline=False)

        webhook.add_embed(embed)

        response = webhook.execute()

    def start(self):
        self.cycle = 0
        while True:
            self.cycle += 1
            if(self.cycle == 1 or self.cycle == 2 or self.cycle % 500 == 0):
                self.LOG("Checking")
            try:
                response = requests.post('https://www.amazon.com.au/juvec',json=self.data,proxies=random.choice(proxies))
            except:
                self.LOG("Request Error")
                self.lastRequest = 'Request Error'
                continue

            if response.status_code == 200:
                if self.lastRequest == 'Request Error':
                    self.LOG('Checking')
                    self.lastRequest = None
                response = response.json()
                if(response['products'][0]['buyingOptions'][0]['availability']['type'] != self.availability):
                    self.LOG(self.availability + ' --> ' + response['products'][0]['buyingOptions'][0]['availability']['type'])
                    self.availability = response['products'][0]['buyingOptions'][0]['availability']['type']


                    
                    image = response['products'][0]['productImages']['images'][0]['lowRes']['url']
                    title =response['products'][0]['productImages']['altText']
                    
                    self.sendWebhook(title,image)
            else:
                self.LOG("Bad Response Status "+str(response.status_code))
                continue


                

        

for i in affliate:
    threading.Thread(target=Task,args=(i,)).start()




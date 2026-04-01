import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

base_URL = 'https://decklog-en.bushiroad.com/view/'
base_logs_path = './target/decklogs.txt'
base_save_path = './lists/'

def main():
    decklogs = readlogs()
    print("Retrieving decklists: "+str(len(decklogs)))
    URLS = [base_URL+x for x in decklogs]
    decklists = []

    for i, url in enumerate(URLS):
        total = len(URLS)
        print(f"\rProgress: {i}/{total}", end="", flush=True)
        html = asyncio.run(ripdeck(url))
        decklists.append(html2deck(html))
        print(f"\rProgress: {i+1}/{total}", end="", flush=True)

    print_decklists(decklists, decklogs)

def readlogs():
    logs_from_txt = []
    with open(base_logs_path, 'r') as f:
        for line in f:
            logs_from_txt.append(line.strip())
    return logs_from_txt

async def ripdeck(url):
    async with async_playwright() as playw:
        browser = await playw.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        html = await page.content()
        return(html)
    
def html2deck(html):
    soup = BeautifulSoup(html, 'html.parser')
    deckview = soup.find_all(class_='card-controller-inner')
    deck_transcribed = []

    for card in deckview:
        card_quantity = card.text
        detail = card.select_one("span.card-detail")
        card_name_code = detail['title'].split(' : ')
        card_code = card_name_code[0]
        card_name = card_name_code[1]
        deck_transcribed.append([card_quantity, card_code, card_name])
    return deck_transcribed

def print_decklists(decklists, decklogs):
    for i, list in enumerate(decklists):
        with open(base_save_path+decklogs[i]+".txt", 'w', encoding="utf-8") as f:
            f.write(decklogs[i])
            f.write("\n")
            for card in list:
                f.write(card[0])
                f.write(" ")
                f.write(card[1])
                f.write(" ")
                f.write(card[2])
                f.write("\n")
        f.close()

main()





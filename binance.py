# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs, BeautifulSoup
# from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
# this is main function
def main():
    service = Service(executable_path="./chromedriver/chromedriver.exe")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    Total_Data = []
    csv_file = 'client_data.csv'
    serial_number = 0
    driver.get('https://www.sodresantoro.com.br/veiculos/v_categoria/carros/')
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    lis = soup.select("ul#paginar_1 li")
    page_number = int(lis[len(lis)-1].text)
    for i in range(1,page_number + 1):
        pagination_url = 'https://www.sodresantoro.com.br/veiculos/ordenacao/data_leilao/tipo-ordenacao/crescente/qtde-itens/15/visualizacao/visual_imagemlista/item-atual/1/pagina/' + str(i) + '/v_categoria/carros/'
        driver.get(pagination_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links = soup.select("ul.tipo-vizualizacao li.visualizacaoDiv-border div.visualizacaoDiv-titulo a.visualizacaoDiv-titulo-lote")
        if len(links) != 0:
            for anchor in links:
                item_link = "https://www.sodresantoro.com.br" + anchor["href"]
                driver.get(item_link)
                face = BeautifulSoup(driver.page_source, 'html.parser')
                serial_number += 1
                scrapedData = {
                    "No": serial_number,
                    "Title": '',
                    "Image URLs" : '',
                    "Current Bid" : '',
                    "Last Bid" : '',
                    "Auction" : '',
                    "Batch": '',
                    "Date" : '',
                    "Categories": '',
                    "Auction Location" : '',
                    "Lot Location" : '',
                    "Internal Code" : '',
                    "Description" : '',
                    "Plate": '',
                    "Color" : '',
                    "KM" : '',
                    "Fuel" : '',
                    "Origin": '',
                    "Chassis Condition" : '',
                    "Exchange": '',
                    "Gas Kit" : '',
                    "Shielding" : '',
                    "Hydraulic/Electrical Steering" : '',
                    "Air Conditioning" : '',
                    "Seller": '',
                }
                Title = face.select("div.online_lance-tit-esq h1")
                Image_URL = face.select("div.slider-for div.slider-for-wrapper div.slider-for-wrapper-items a")
                CurrentBid = face.select("div.online_lance-tit-dir span.valor")
                LastBid = face.select("table#tabela_lances tr.online_blocos-linha")
                Auction = face.select("div.online_desc_lote div.online_desc_coluna1")
                Batch = face.select("div.online_desc_lote div.online_desc_coluna1")
                Date = face.select("div.online_desc_lote div.online_desc_coluna1")
                Categories = face.select("div.online_desc_lote div.online_desc_coluna1")
                AuctionLocation = face.select("div.online_desc_lote div.online_desc_coluna1")
                LotLocation = face.select("div.online_desc_lote div.online_desc_coluna1")
                InternalCode = face.select("div.online_desc_lote div.online_desc_coluna1")
                Description = face.select("div.online_desc_lote p.desc_titulos strong")
                Plate = face.select("div.online_desc_coluna1 ul.divisao li p")
                Seller = face.select("span.titulo_box")

                if Title:
                    scrapedData["Title"] = Title[0].text
                if CurrentBid:
                    scrapedData["Current Bid"] = CurrentBid[0].text
                if LastBid:
                    length = 0
                    length = int(len(LastBid[0].select("td")))
                    scrapedData["Last Bid"] = LastBid[0].select("td")[length-1].text
                if Auction:
                    scrapedData["Auction"] = Auction[0].select("p")[0].select("strong")[0].text
                if Batch:
                    scrapedData["Batch"] = Batch[0].select("p")[1].select("strong")[0].text
                if Date:
                    scrapedData["Date"] = Date[0].select("p")[2].select("b")[0].text
                if Categories:
                    scrapedData["Categories"] = Categories[0].select("p")[3].select("strong")[0].text
                if AuctionLocation:
                    scrapedData["Auction Location"] = AuctionLocation[0].select("p")[4].text.split(": ")[1]
                if LotLocation:
                    scrapedData["Lot Location"] = LotLocation[0].select("p")[5].text.split(": ")[1]
                if InternalCode:
                    scrapedData["Internal Code"] = InternalCode[0].select("p")[6].text.split(": ")[1]
                if Description:
                    scrapedData["Description"] = Description[0].text
                if Seller:
                    for item in Seller:
                        if item.find("Vendedor") != -1:
                            scrapedData["Seller"] = item.find_next("div").text
                if Image_URL:
                    links = ""
                    for j in range(0, 5):
                        links += Image_URL[j]["href"] + ", "
                    scrapedData["Image URLs"] = links
                if Plate: 
                    for item in Plate:
                        if item.text.find("Placa") != -1:
                            scrapedData["Plate"] = item.select("b")[0].text
                        elif item.text.find("KM") != -1:
                            scrapedData["KM"] = item.select("b")[0].text
                        elif item.text.find("Cor") != -1:
                            scrapedData["Color"] = item.select("b")[0].text
                        elif item.text.find("Combustível") != -1:
                            scrapedData["Fuel"] = item.select("b")[0].text
                        elif item.text.find("Origem") != -1:
                            scrapedData["Origin"] = item.select("b")[0].text
                        elif item.text.find("Estado do Chassi") != -1:
                            scrapedData["Chassis Condition"] = item.select("b")[0].text
                        elif item.text.find("Câmbio") != -1:
                            scrapedData["Exchange"] = item.select("b")[0].text
                        elif item.text.find("Kit Gás") != -1:
                            scrapedData["Gas Kit"] = item.select("b")[0].text
                        elif item.text.find("Blindagem") != -1:
                            scrapedData["Shielding"] = item.select("b")[0].text
                        elif item.text.find("Direção Hidráulica/Elétrica") != -1:
                            scrapedData["Hydraulic/Electrical Steering"] = item.select("b")[0].text
                        elif item.text.find("Ar Condicionado") != -1:
                            scrapedData["Air Conditioning"] = item.select("b")[0].text

                Total_Data.append(scrapedData)
                time.sleep(1)
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['No', 'Title', 'Image URLs', 'Current Bid', 'Last Bid', 'Auction', 'Batch', 'Date', 'Categories', 'Auction Location', 'Lot Location', 'Internal Code', 'Description', 'Plate', 'Color', 'KM', 'Fuel', 'Origin', 'Chassis Condition', 'Exchange', 'Gas Kit', 'Shielding', 'Hydraulic/Electrical Steering', 'Air Conditioning', 'Seller']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(Total_Data)

    print("=============end===============")
    time.sleep(1)

if __name__ == '__main__':
    main()

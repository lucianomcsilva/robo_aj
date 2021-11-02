import scrapy
import os
import pathlib
import csv 

class SpiderAj2Spider(scrapy.Spider):
    name = "spider_aj"
    delimiter = ';'
    
    # abre o arquivo local, com todos os links
    start_urls = [f"{pathlib.Path(os.path.abspath('arnaldo_jabor.html')).as_uri()}"]
    
    # Apaga o arquivo caso exista, para evitar sobreposição
    if os.path.exists("artigos_aj.csv"):
        os.remove("artigos_aj.csv")

    # função que interpreta o documento que lista os artigos
    def parse(self, response):       
    # def parse(self, response, row):
        for link in response.css(".item-ultimas").css("h2").css("a::attr(href)").getall():
            text_page = f"https://www.otempo.com.br/{link}"
            yield scrapy.Request(text_page, callback=self.parse_text)

    # função que interpreta os documentos com os textos 
    def parse_text(self, response):
        content = ""   
        for line in response.css('div.texto-artigo p::text').getall() :
            content = content + "".join(line) + "\n"
            
        post = {
            'author': 'Arnaldo Jabor',
            'title': response.css('h1::text').get(),
            'content': content.encode('utf-8')
        }
        
        with open('artigos_aj.csv', 'a', newline='', encoding="utf-8")  as output_file:
             dict_writer = csv.DictWriter(output_file, post.keys())            
             dict_writer.writerows([post])        
        yield post
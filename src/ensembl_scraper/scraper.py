#### Scrapes Ensembl's annotated DNA seqeunce pages

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class EnsemblScraper:
    def __init__(self):
        self.seq_type = 0
        self.sequences = ""
    
    def add_seq(self, seq_list, prev_type, new_type, seq):
        seq = seq.strip()
        
        if seq == "":
            return seq_list, prev_type
        
        if prev_type == new_type:
            seq_list[-1][0] = new_type
            seq_list[-1][1] += seq
            prev_type = new_type
        else:
            seq_list.append([new_type, seq])
            prev_type = new_type
            
        return seq_list, prev_type

    def scrape_seq(self, url, load_page_delay=5):
        self.seq_type = 0
        self.sequences = ""
        
        options = webdriver.ChromeOptions() 
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # Initiates the webdriver.
        # Parameter includes the path of the webdriver
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        
        # Ensures that the page is loaded
        time.sleep(load_page_delay) 
        
        html = driver.page_source
        
        # Apply bs4 to html variable
        soup = BeautifulSoup(html, "html.parser")
        
        # The DNA sequence is found under a span with the '_seq' class
        header = soup.find_all('pre', {'class' : 'text_sequence'})[0].text.split('\n')[0]
        entire_seq = soup.find_all('span', {'class' : '_seq'})
        
        self.sequences += header
        for (idx, line) in enumerate(entire_seq):
            if idx == 0: 
                if header.strip() == line.text.strip():
                    continue
                
            self.sequences += "\n"
            self.sequences += line.text

    def scrape_annotated_seq(self, url, load_page_delay=5):
        self.seq_type = 1
        self.sequences = ""
        
        # Initiates the webdriver.
        # Parameter includes the path of the webdriver
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        
        # Ensures that the page is loaded
        time.sleep(load_page_delay) 
        
        html = driver.page_source
        
        # Apply bs4 to html variable
        soup = BeautifulSoup(html, "html.parser")
        
        # The DNA sequence is found under a span with the '_seq' class
        header = soup.find_all('pre', {'class' : 'text_sequence'})[0].text.split('\n')[0]
        entire_seq = soup.find_all('span', {'class' : '_seq'})

        sequences = []
        prev_type = -1
        seq = ""

        for (idx, line) in enumerate(entire_seq):
            seq += line.text
            if idx == 0:
                sequences.append([0, header])
                continue
            
            # Ensembl has it setup so that exons are usually in another span,
            # requring a loop through more elements
            if len(line.find_all()) > 0:
                for element in entire_seq[idx]:
                    if element.attrs.get('style'):
                        if "#ffebcd" and "#8b0000" in element.attrs.get('style'):
                            sequences, prev_type = self.add_seq(sequences, prev_type, 0, element.text)
                        elif "#ffebcd" in element.attrs.get('style'):
                            sequences, prev_type = self.add_seq(sequences, prev_type, 2, element.text)
                        else:
                            sequences, prev_type = self.add_seq(sequences, prev_type, 1, element.text)
                    else:
                        sequences, prev_type = self.add_seq(sequences, prev_type, 1, element.text)
                        
            else:
                if line.attrs.get('style'):
                    if "#ffebcd" and "#8b0000" in element.attrs.get('style'):
                        sequences, prev_type = self.add_seq(sequences, prev_type, 0, line.text)
                    elif "#ffebcd" in line.attrs.get('style'):
                        sequences, prev_type = self.add_seq(sequences, prev_type, 2, line.text)
                    else:
                        sequences, prev_type = self.add_seq(sequences, prev_type, 1, line.text)
                else:
                    sequences, prev_type = self.add_seq(sequences, prev_type, 1, line.text)

        driver.close() # closing the webdriver
        
        self.sequences = sequences
        
    def save(self, save_file, mode):
        file = open(save_file, mode)
        
        if self.seq_type == 0:
            file.write("{}".format(self.sequences))
        elif self.seq_type == 1:
            for (idx, i) in enumerate(self.sequences):
                if idx == 0:
                    file.write("{}\n".format(i[1]))
                    continue
                
                file.write("{},{}\n".format(i[0], i[1]))
        else:
            pass
            
        file.close()
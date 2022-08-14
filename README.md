# ensembl-scraper
 Get's the DNA sequence from an Ensembl wep page. The ```EnsemblScraper``` object has three main methods that should be used.
 * ```scrape_seq(url, load_page_delay)```: The url parameter should be a string that contains the url to an Ensembl sequence page. The load_page_delay parameter is used as a delay (in seconds) to allow for the Ensembl page to load. The default value of the parameter is 5 and should be any positive number. The method reutrns no value but changes the ```self.sequences``` string variable to be the summary description of the sequence along with the entire DNA sequence.
 * ```scrape_annotated_seq(url, load_page_delay)```: Parameters same as above. The method reutrns no value but changes the ```self.sequences``` string variable to be a 2d list. The first element of the list can either be a 0, 1, or 2. The second element is a corresponding DNA sequence. The meaning of these numbers and what a corresponding DNA sequence is described below. 
   * 0: The sequence to the right of this element are exons that are part of the scraped gene.
   * 1: The sequence to the right of this element are introns.
   * 2: The sequence to the right of this element are exons that are part of the scraped genes region.

 * ```save(save_file, mode)```: The save_file parameter should be a string and is the file name that the scraped sequence will be saved in. The mode parameter is a string and is how you want ot open the save_file. There are six avaliable modes.
   * "r":   Read only
   * "r+":  Read and write
   * "w":   Write only
   * "w+":  Write and read
   * "a"    Append only
   * "a+"   Append and read

# Examples
How to use ```scrape_seq```, using ```scrape__annotated_seq``` is exactly the same.
 ```python
 url = "https://www.ensembl.org/Homo_sapiens/Gene/Sequence?g=ENSG00000175899;r=12:9067664-9116229"

 data = EnsemblScraper()
 data.scrape_seq(url, 5)
 data.save("sequence.csv", "w")
 ```

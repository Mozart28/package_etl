from extraction.webscrapping import ExtractionData 

url = "https://www.w3schools.com/html/html_tables.asp"
colonnes = ["Company", "Contact", "Country"]

df = ExtractionData.extract_webscrapping(url, colonnes, selector="table#customers")
print(df.head())

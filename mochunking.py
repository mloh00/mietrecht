import json
import os

def mochunking(raw_text):
    # Split the text into paragraphs.
    paragraphs = raw_text.split("\n\n")
    # Initialize json list
    json_list = []
    # Iterate over the paragraphs.
    for paragraph in paragraphs:
        # If the paragraph is not empty.
        if paragraph:
            # Get the title of the paragraph.
            title = paragraph.split("\n")[0]
            print(title)
            # Get the text of the paragraph.
            paragraph_text = paragraph.split("\n")[1:]
            # Get the paragraph number
            symbol = "§"
            if symbol in title:
                words_after_symbol = title.split(symbol)[1].split()
                filtered_paragraph_nr = words_after_symbol[0].strip() if words_after_symbol else None
            else: 
                filtered_paragraph_nr = "unknown"
            # Customize the paragraph text.
            paragraph_customized = f"Das ist die Beschreibung zum Paragraphen {title}: " + "".join(paragraph_text)
            # Create a json object and append it to the json list.
            json_list.append({"paragraph": filtered_paragraph_nr, "title": title, "lang": "de", "chunks": [paragraph_customized]})
    
    # Return the json list.
    return json_list  

if __name__ == "__main__":

    with open("Mietrecht_Rohtext.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()

    with open("Mietrecht_chunks.json", "w", encoding="utf-8") as f:
        json.dump(mochunking(raw_text), f, indent=4, ensure_ascii=False)
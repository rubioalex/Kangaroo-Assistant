phrase = "can you please open stack overflow"

if "open" in phrase:
    open_idx = phrase.find('open') + 4
    
    
extracted = phrase[open_idx:].strip().replace(" ", "")
print(extracted)
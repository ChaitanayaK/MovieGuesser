import requests

def encrypt(name: str, guessed: list):
    vowels = ['a', 'e', 'i', 'o', 'u', '/', ',', ':', '"', '?', '-']
    encrypted = []
    name = name.lower()
    shortenedList = guessed.copy()
    for char in guessed:
        if char not in name:
            shortenedList.remove(char)
    vowels.extend(shortenedList)
    for i, char in enumerate (name):
        if char in vowels or char == " ": 
            encrypted.append(name[i])
        else:
            encrypted.append("_") 

    packet = {"movie": " ".join(encrypted), "length": len(guessed)-len(shortenedList), "win": True if "_" not in encrypted else False}

    return packet


def movieData(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except:
        return None

if __name__ == "__main__":
    url = "http://www.omdbapi.com/?t=Cocktail&y=2012"

    print(movieData(url))
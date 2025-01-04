import os
import tempfile
import requests
import urllib.request
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# Loads Personal Unsplash (Stock Photo Library) API key 
load_dotenv()
TOKEN = os.getenv('UNSPLASH_TOKEN')

def obtain_image():
    """Downloads the desired image."""
    URL = f"https://api.unsplash.com/search/photos/?client_id={TOKEN}"
    query = input("Image Type: ")
    PARAMS = {
        "query": query
    }
    response = requests.get(url = URL, params = PARAMS)
    if response.status_code != 200:
        print(f"Error {response.status_code}")
        exit(1)
    
    data = response.json()
    if len(data["results"]) == 0:
        print(f"Error: No result for {query}")
        exit(1)
        
    pic_url = data["results"][0]["links"]["download"]
    if not os.path.exists("images"):
        os.makedirs("images")
    urllib.request.urlretrieve(pic_url, f"images/{PARAMS['query']}.png") 
    return "images/" + PARAMS['query'] + ".png"

def generator(filename):
    """Generates the Text File."""

    # Creates temporary Transposed Grayscaled object 
    img = Image.open(filename) 
    img = img.transpose(Image.TRANSPOSE)
    img = img.convert('L')

    # Scales Image to desired size
    scaling_factor = 0.3
    new_x = int(img.size[0] * scaling_factor)
    new_y = int(img.size[1] * scaling_factor * 2.0)
    newsize = (new_x, new_y) 
    img_resized = img.resize(newsize)
    
    # Creates the temporary Image from object
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, "temp.png")
    img_resized.save(temp_file_path)

    # Goes through each pixel to add a character
    pix = img_resized.load()
    text = ""
    gradient = [' ','.',',',';','!','v','l','L','F','E','$']
    for row in range(img_resized.size[0]):
        for col in range(img_resized.size[1]):
            text += gradient[int((pix[int(row),int(col)]/(255 / (len(gradient)-1))))]
        text+=('\n')
    f = open("output.txt",'w')
    f.write(text[0:len(text)-1])
    image = Image.new("RGB", (int(img.size[1] * scaling_factor * 23.9), int(img.size[0] * scaling_factor * 22.7)), "black")
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size=20)    
    draw.text((0, 0), text, font=font, fill=(255, 255, 255))
    image.save("result.png")

    # Cleansup temporary Files
    os.remove(temp_file_path)

def main():
    """Handles User input."""
    option = input("""\nChoose an Option:\n-----------------\n(1) Search Image\n(2) Select Existing Image\n-----------------\n""")
    while True:
        if option == "1":
            file_name = obtain_image()
            break
        elif option == "2":
            file_name = "images/"+ input("Filename: ") + ".png"
            file_name = os.path.abspath(file_name)
            while not os.path.exists(file_name):
                file_name = "images/"+ input("Filename: ") + r".png"
                file_name = os.path.abspath(file_name)
            break
        option = input("Error Try Again: ")
    generator(file_name)

if __name__ == "__main__":
    main()

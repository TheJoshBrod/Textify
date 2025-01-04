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
    urllib.request.urlretrieve(pic_url, f"input_images/{PARAMS['query']}.png")
    return "input_images/" + PARAMS['query'] + ".png"

def generator(filename, is_image, scaling_factor):
    """Generates the Text File."""

    # Creates temporary Transposed Grayscaled object
    img = Image.open(filename) 
    img = img.transpose(Image.TRANSPOSE)
    img = img.convert('L')

    # Scales Image to desired size
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

    if not is_image:
        with open("output.txt",'w') as f:
            f.write(text[0:len(text)-1])
    else:
        image = Image.new("RGB", (int(img.size[1] * scaling_factor * 23.9), int(img.size[0] * scaling_factor * 22.7)), "black")
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size=20)
        draw.text((0, 0), text, font=font, fill=(255, 255, 255))
        image.save("result.png")

    # Cleansup temporary Files
    os.remove(temp_file_path)

def get_file_name() -> str:
    """Returns file name for image."""
    input_options_txt = "\n"
    input_options_txt += "Choose a Method to Input an Image:\n"
    input_options_txt += "-----------------\n"
    input_options_txt += "(1) Search Image\n"
    input_options_txt += "(2) Select Existing .png Image\n"
    input_options_txt += "-----------------\n"

    option = input(input_options_txt)
    is_valid_image = False
    while True:
        if option == "1":
            file_name = obtain_image()
            break
        elif option == "2":
            while not is_valid_image or not os.path.exists(file_name):
                file_name = "input_images/"+ input("Filename: ")
                file_name = os.path.abspath(file_name)
                try:
                    img = Image.open(file_name)
                    is_valid_image = True
                    img.close()
                except:
                    is_valid_image = False
            break
        option = input("Error Try Again: ")

    return file_name

def get_file_output_mode() -> bool:
    """Returns true if picture mode, false if text mode."""

    output_options_txt = "\n"
    output_options_txt += "Choose a Method to Output an Image:\n"
    output_options_txt += "-----------------\n"
    output_options_txt += "(1) Text file (output.txt)\n"
    output_options_txt += "(2) Image file (result.png)\n"
    output_options_txt += "-----------------\n"

    option = input(output_options_txt)

    while True:
        if option == "1":
            return False
        elif option == "2":
            return True
        option = input("Error Try Again: ")

def get_scaling_factor() -> float:
    """Returns scaling factor of photo."""

    output_options_txt = "\n"
    output_options_txt += "Choose a Scaling Factor\n"
    output_options_txt += "(# chars = scaling_factor * original_height x scaling_factor * original_width)\n"
    output_options_txt += "-----------------\n"

    scaling_factor_input = input(output_options_txt)

    while True:
        try:
            scaling_factor = float(scaling_factor_input)
            return scaling_factor
        except ValueError:
            scaling_factor_input = input("Error Try Again: ")

def main():
    """Handles User input."""
    file_name = get_file_name()
    is_image = get_file_output_mode()
    scaling_factor = get_scaling_factor()

    generator(file_name, is_image, scaling_factor)

if __name__ == "__main__":
    main()

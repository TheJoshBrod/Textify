# Textify

This Python script allows you to generate ASCII art from images. It offers two main functionalities: searching for an image on Unsplash and generating ASCII art from it, or selecting an existing image from your local directory and converting it into ASCII art.

## Prerequisites

Before running the script, ensure you have the following dependencies installed:

- Python >= 3.12.8
- Each of the required libraries (`pip install -r requirments.txt`)

You'll also need a Personal Unsplash API key. You can obtain one by signing up on the [Unsplash website](https://unsplash.com/documentation).

## Usage

1. Clone the repository to your local machine.

2. Create a `.env` file in the project directory and add your Unsplash API key:

    ```
    UNSPLASH_TOKEN=your_api_key_here
    ```

3. Run the script by executing the following command in your terminal:

    ```
    python textify.py
    ```

4. Select an input mode:
   - **Search Image**: Enter the type of image you want to search for on Unsplash. The script will download the first matching image and convert it into ASCII art.
   - **Select Existing Image**: Enter the filename of an existing image in your local directory. The script will convert it into ASCII art.

5. Select an output mode:
   - **Text File**: Outputs ascii picture as text file.
   - **Image File**: Outputs ascii picture as a picture.

6. Select a scaling factor:
   - **Scaling Factor**: Choose number (Recommended Range: `0.005 < scaling factor < 1.0`)
   ***Note**: Very dependent on input image size

## Output

The generated ASCII art will be saved as `output.txt` or `result.png` in the project directory.

## Contributing

Contributions are welcome! If you have ideas for improvement or bug fixes, feel free to fork the repo and submit a pull request.

## Credits

- This script uses the Unsplash API to search for images. Visit [Unsplash](https://unsplash.com/developers) for more information on the API.
- ASCII art generation utilizies the PIL (Python Imaging Library) module.

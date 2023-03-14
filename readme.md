# DuplicateDeleter

DuplicateDeleter is a Python script that helps you find and delete duplicate images in a directory. It works by iterating through a directory (recursively in subdirectories too if wanted) and searching for images with the provided extensions (default to jpg, jpeg, and png). It then compares each image to the other, which yields a score from 0 to 1, where 1 is an exact replica. The user can set a threshold of when to count an image as a duplicate (defaults to 0.8). All duplicate images (that pass the threshold) are then grouped up and shown to the user in a GUI.

## Usage

To use this script, you must first install the requirements by running:

    `pip install -r requirements.txt`

Then, you can run the script by running:

    `python3 -m DuplicateDeleter --directory <path> [--recursive] [--format <format names>] [--no-confirm] [--threshold <amount>] [--verbose] [--version]`


The available flags are (in a table):

| Flag         | Alias | Description                                                                              | Default        |
| ------------ | ----- | ---------------------------------------------------------------------------------------- | -------------- |
| --directory  | -d    | The directory to search for duplicate images in                                          | None           |
| --recursive  | -r    | Whether to search for duplicate images recursively in subdirectories                     | False          |
| --format     | -f    | The image formats to search for (separated by commas)                                    | jpg, jpeg, png |
| --no-confirm | -n    | Whether to skip the confirmation prompt                                                  | False          |
| --threshold  | -t    | The threshold of when to count an image as a duplicate (must be a value between 0 and 1) | 0.8            |
| --verbose    | -v    | Whether to print out the progress of the script                                          | False          |
| --version    | -V    | Whether to print out the version of the script                                           | False          |

The script will start scanning for duplicate images and display the results in a GUI.

## GUI

The GUI consists of a gallery of the images found to be duplicates. Below the gallery, there is a selection box consisting of labels of the images (these labels are provided at the top of every image in the gallery). The user can select multiple options (even all of them) and choose to delete them by clicking the delete button right below. Below the delete button, there are two navigation buttons to proceed to the next/previous duplicate image section and a page counter right in between these two buttons. At the very end of the window, there's a cancel button to close the window.

## Contributing

This script is still in development, and contributions are welcome! If you would like to contribute, please fork the repository and submit a pull request. If you find any bugs or have any suggestions, please open an issue in the repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

from logging import getLogger, basicConfig, INFO, DEBUG, FileHandler, StreamHandler
import random
import argparse
from pathlib import Path
from .src.main import (
    find_all_images,
    find_duplicates,
    delete_all_duplicates,
    verify_directory,
    start_gui,
)

__version__ = "0.1.0"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Path to the directory containing images")
    parser.add_argument(
        "-t", "--threshold", help="Threshold value for similarity", default=0.8, type=float
    )
    parser.add_argument(
        "-f",
        "--formats",
        help="Image formats to search for",
        type=list,
        default=["jpg", "jpeg", "png"],
        nargs="+",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        help="Search for images recursively within sub-directories",
        action="store_true",
    )
    parser.add_argument(
        "-nc",
        "--no-confirm",
        help="Do not ask for confirmation. Use this with caution, it will delete duplicates ramdomly and might delete images you did not expect to tbe deleted.",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Enable verbose logging",
        action="store_true",
    )
    parser.add_argument(
        "--version",
        help="Print the version and exit",
        action="store_true",
    )

    args = parser.parse_args()

    if args.version:
        print(__version__)
        exit()

    basicConfig(
        level=DEBUG if args.verbose else INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            StreamHandler(),
        ],
    )
    log = getLogger(__name__)

    if args.directory is None:
        log.error("Please provide the path to the directory containing images")
        exit()

    if args.threshold < 0 or args.threshold > 1:
        log.error("Threshold value must be between 0 and 1")
        exit()

    directory = Path(args.directory)

    if not verify_directory(directory):
        exit()

    images = find_all_images(directory, args.recursive, args.formats)

    log.info(
        f"Found {len(images)} images in the directory" + (" recursively" if args.recursive else "")
    )

    duplicates = find_duplicates(images, args.threshold)

    if not duplicates or not all(duplicates):
        log.info("No duplicates found. All images are unique.")
        exit()

    log.info(f"Found {sum(map(lambda x: len(x), duplicates))} duplicate images")

    if args.no_confirm:
        # randomize it for shits and giggles :p
        # and then keep only the 1st image in the tuple
        # and delete the rest
        delete_all_duplicates([(random.shuffle(i), i[1:])[1] for i in duplicates])
        log.info("Deleted all duplicate images")
        exit()

    else:
        start_gui(duplicates)

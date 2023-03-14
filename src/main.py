import cv2
import os
import cv2
from skimage.metrics import structural_similarity as compare_ssim
from skimage.transform import resize
from pathlib import Path
from logging import getLogger
from .gui import ImageBrowser

log = getLogger(__name__)


def verify_directory(directory: Path) -> bool:
    """Verify that the given directory exists and is a directory"""
    if not directory.exists():
        log.error("The directory does not exist")
        return False
    if not directory.is_dir():
        log.error("The path provided is not a directory")
        return False
    return True


def find_all_images(
    directory: Path, recursive: bool, formats: list[str] = ["jpg", "jpeg", "png"]
) -> list[Path]:
    """Find all images in the given directory"""
    image_files = []
    log.debug(f"Searching for images in {directory}")
    for item in directory.iterdir():
        if item.is_file() and item.name.lower().endswith(tuple(formats)):
            log.debug(f"Found image: {item}")
            image_files.append(item)
        elif item.is_dir() and recursive:
            image_files.extend(find_all_images(item, recursive, formats))

    return image_files


def find_duplicates(images: list[Path], threshold: float) -> list[list[Path]]:
    """Find duplicate images in the given list of images.
    One image can have multiple duplicates/similar images.
    """
    duplicates = {i: list[Path]() for i in images}
    img_copy = images.copy()
    for i in range(len(images)):
        try:
            im1_path = img_copy[i]
        except IndexError:
            break

        im1 = cv2.imread(str(im1_path))
        iterator = iter(img_copy[i:])
        while True:
            try:
                im2_path = next(iterator)
            except StopIteration:
                break

            else:
                if im1_path == im2_path:
                    continue

            im2 = cv2.imread(str(im2_path))

            log.debug(
                f"Comparing {im1_path} and {im2_path}\n"
                f"Image 1: {im1.shape}\n"
                f"Image 2: {im2.shape}"
            )
            if im1.shape != im2.shape:
                log.debug("Resizing images to match")
                im2 = resize(im2, im1.shape, anti_aliasing=True)
                log.debug(f"Image 2 after resizing: {im2.shape}")
            score, _ = compare_ssim(
                im1,
                im2,
                full=True,
                channel_axis=2,
                data_range=im1.max() - im1.min(),
            )
            log.debug(f"SSIM score: {score}")
            if score > threshold:
                log.debug(f"Found duplicate: {im2_path}")
                duplicates[im1_path].append(im2_path)
                # remove the image from the list of images to avoid duplicates
                img_copy.remove(im2_path)

    log.debug(f"grouping duplicates in sublists")
    return list(map(lambda x: [x[0], *x[1]], filter(lambda x: len(x[1]) > 0, duplicates.items())))


def delete_all_duplicates(duplicates: list[list[Path]]) -> None:
    """Delete all duplicate images in the given dictionary of duplicates"""
    for i in duplicates:
        for j in i:
            os.remove(j)


def start_gui(duplicates: list[list[Path]]):
    # start a gui with tkinter and show each tuple of images one by one in a window
    # give the users an enumerate list of images to choose which they want deleted.
    log.info("Starting GUI")
    ImageBrowser(duplicates)

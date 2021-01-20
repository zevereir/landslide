import numpy as np
from PIL import Image
import imagehash
def calculate_signature(image_file: str, hash_size: int) -> np.ndarray:
    """
    Calculate the dhash signature of a given file

    Args:
        image_file: the image (path as string) to calculate the signature for
        hash_size: hash size to use, signatures will be of length hash_size^2

    Returns:
        Image signature as Numpy n-dimensional array or None if the file is not a PIL recognized image
    """
    try:
        pil_image = Image.open(image_file).convert("L").resize(
            (hash_size + 1, hash_size),
            Image.ANTIALIAS)
        dhash = imagehash.dhash(pil_image, hash_size)
        signature = dhash.hash.flatten()
        pil_image.close()
        return np.packbits(signature)
    except IOError as e:
        raise e


def find_lsh_similarity(img1,img2,  hash_size: int):
    """
    Find near-duplicate images

    Args:
        input_dir: Directory with images to check
        threshold: Images with a similarity ratio >= threshold will be considered near-duplicates
        hash_size: Hash size to use, signatures will be of length hash_size^2
        bands: The number of bands to use in the locality sensitve hashing process

    Returns:
        A list of near-duplicates found. Near duplicates are encoded as a triple: (filename_A, filename_B, similarity)
    """
    signatures = dict()

    signa = calculate_signature(img1,hash_size)
    signb = calculate_signature(img2,hash_size)
    return calc_similary(signa,signb,hash_size)

def calc_similary(a,b,hash_size):
    hd = sum(np.bitwise_xor(
        np.unpackbits(a),
        np.unpackbits(b)
    ))
    similarity = (hash_size ** 2 - hd) / hash_size ** 2
    return similarity



def calc_signature_similarity(img1,img2):
    hash_size = 16
    return find_lsh_similarity(img1,img2, hash_size)

from PIL import Image
import numpy as np

def read_image_filenames(filename):
    """Read image filenames from a text file."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

def stitch_row(image_paths, horizontal_overlap, direction='rtl'):
    """
    Stitch a row of images with given overlap.
    direction: 'rtl' (right to left) or 'ltr' (left to right)
    """
    if direction == 'rtl':
        image_paths = image_paths[::-1]  # Reverse for right to left
    
    # Start with the first image
    result = Image.open(image_paths[0])
    
    for img_path in image_paths[1:]:
        img = Image.open(img_path)
        
        # Calculate dimensions for the merged image
        width1, height1 = result.size
        width2, height2 = img.size
        final_width = width1 + width2 - horizontal_overlap
        final_height = max(height1, height2)
        
        # Create a new blank image
        merged = Image.new('RGB', (final_width, final_height))
        
        # Paste first image
        merged.paste(result, (0, 0))
        
        # Paste the second image with overlap
        merged.paste(img, (width1 - horizontal_overlap, 0))
        
        result = merged
    
    return result

def stitch_images(filename_list_path, rows=13, cols=8, h_overlap=300, v_overlap=400, output_path='stitched_image.jpg'):
    """
    Stitch multiple images in a zigzag pattern with specified overlaps.
    """
    # Read image filenames
    filenames = read_image_filenames(filename_list_path)
    
    if len(filenames) != rows * cols:
        raise ValueError(f"Expected {rows * cols} images, but got {len(filenames)}")
    
    # Reshape filenames into a 2D array
    image_grid = np.array(filenames).reshape(rows, cols)
    
    # Stitch rows first
    stitched_rows = []
    for row_idx, row_images in enumerate(image_grid):
        # Determine a direction based on row index
        direction = 'ltr' if row_idx % 2 else 'rtl'
        stitched_row = stitch_row(row_images, h_overlap, direction)
        stitched_rows.append(stitched_row)
    
    # Start with the first stitched row
    final_result = stitched_rows[0]
    
    # Stitch rows vertically
    for next_row in stitched_rows[1:]:
        # Get dimensions
        width1, height1 = final_result.size
        width2, height2 = next_row.size
        final_width = max(width1, width2)
        final_height = height1 + height2 - v_overlap
        
        # Create a new blank image
        merged = Image.new('RGB', (final_width, final_height))
        
        # Paste first image
        merged.paste(final_result, (0, 0))
        
        # Paste the second image with vertical overlap
        merged.paste(next_row, (0, height1 - v_overlap))
        
        final_result = merged
    
    # Save the final result
    final_result.save(output_path)
    return final_result

# Example usage
if __name__ == "__main__":

    # # # Your text file with image filenames:
    # filename_list_path = "/Users/aavelino/Downloads/BiosoilAI/7_big_insects/A01-B2/images_to_stitich.txt"

    # # Include also the desired output filename and its extension!:
    # output_path = "/Users/aavelino/Downloads/BiosoilAI/7_big_insects//A01-B2//A01-B2_stitched.jpg"


    # # Your text file with image filenames:
    filename_list_path = "/Users/aavelino/Downloads/BiosoilAI/7_big_insects/A02-E/images_to_stitich.txt"

    # Include also the desired output filename and its extension!:
    output_path = "/Users/aavelino/Downloads/BiosoilAI/7_big_insects/A02-E/A02-E_stitched.jpg"
    
    stitched_image = stitch_images(
        filename_list_path,
        rows=12,
        cols=8,
        h_overlap=372,
        v_overlap=422,
        output_path=output_path
    )

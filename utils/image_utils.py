from PIL import Image
import numpy as np
import os

# Configuration
Image.MAX_IMAGE_PIXELS = None
MAX_SIZE = (1024, 1024)  # maximum allowed for testing

def validate_image_size(img, filename):
    """Validate and resize image if needed"""
    if img.size[0] > MAX_SIZE[0] or img.size[1] > MAX_SIZE[1]:
        print(f"⚠️ Image {filename} too large ({img.size}), resizing to {MAX_SIZE}")
        return img.resize(MAX_SIZE)
    return img

def load_images(folder):
    """
    Load and process images from folder
    
    Args:
        folder: Directory containing images
        
    Returns:
        List of processed PIL Images
    """
    images = []
    sizes = []
    
    try:
        # Validate folder exists
        if not os.path.exists(folder):
            print(f"⚠️ Folder {folder} does not exist")
            return []
        
        # Load all grayscale images
        for file in sorted(os.listdir(folder)):
            if file.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                filepath = os.path.join(folder, file)
                img = Image.open(filepath).convert('L')
                
                # Validate and resize if needed
                img = validate_image_size(img, file)
                
                sizes.append(img.size)
                images.append(img)
        
        if len(images) == 0:
            print("⚠️ No images found in", folder)
            return []
        
        # Find minimum width & height across all images
        min_w = min([w for w, h in sizes])
        min_h = min([h for w, h in sizes])
        
        # Resize all images to the same (min_w, min_h)
        images = [img.resize((min_w, min_h)) for img in images]
        
        print(f"All images resized to: {min_w}×{min_h}")
        return images
        
    except Exception as e:
        print(f"❌ Error loading images: {str(e)}")
        return []

def save_images(images, output_folder, prefix):
    """
    Save a list of images to the specified output folder with given prefix
    
    Args:
        images: List of PIL Images or numpy arrays
        output_folder: Directory to save images
        prefix: Prefix for output filenames
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Save each image
        for i, img in enumerate(images):
            # Convert numpy array to PIL Image if needed
            if isinstance(img, np.ndarray):
                img = Image.fromarray(img.astype(np.uint8))
            
            # Generate output filename
            filename = f"{prefix}_{i+1}.png"
            filepath = os.path.join(output_folder, filename)
            
            # Save the image
            img.save(filepath)
            
        print(f"✅ Saved {len(images)} images to {output_folder}/")
            
    except Exception as e:
        print(f"❌ Error saving images: {str(e)}")
        raise

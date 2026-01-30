import io
from PIL import Image


def read_image(contents):

    # 1. Image Processing
    binary_data = None
    
    try:
        # Open with Pillow
        img = Image.open(io.BytesIO(contents))
        
        # Convert to RGB (Crucial for PNGs with transparency)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Resize to 224x224
        img = img.resize((224, 224))
        
        # Save to buffer as JPEG
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        binary_data = buffer.getvalue()
        
    except Exception as e:
        print(f"Error processing image: {e}")
        # You might want to log this or handle it gracefully
        return None

    return binary_data
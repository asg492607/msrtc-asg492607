from PIL import Image

def crop_icons():
    img_path = r"C:\Users\Atharva\.gemini\antigravity\brain\30f0091a-9a0b-4f26-a2e4-8155d055c8bc\media__1783112481620.png"
    img = Image.open(img_path)
    
    # Get dimensions
    width, height = img.size
    
    # Calculate width of each segment (4 icons)
    segment_width = width // 4
    
    # Crop into 4 icons
    for i in range(4):
        # Add a little padding reduction if we want, or just take the exact segment
        left = i * segment_width
        right = (i + 1) * segment_width
        
        # Crop the segment
        cropped = img.crop((left, 0, right, height))
        
        # Optionally, get bounding box to remove extra transparency
        bbox = cropped.getbbox()
        if bbox:
            cropped = cropped.crop(bbox)
            
        cropped.save(f"trust_icon_{i+1}.png")
        print(f"Saved trust_icon_{i+1}.png")

if __name__ == '__main__':
    crop_icons()

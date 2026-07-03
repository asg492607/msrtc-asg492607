from PIL import Image

def extract_badges():
    img_path = r"C:\Users\Atharva\.gemini\antigravity\brain\30f0091a-9a0b-4f26-a2e4-8155d055c8bc\media__1783112269552.png"
    img = Image.open(img_path)
    
    # We will just guess the coordinates of the 4 logos based on the image being a horizontal strip
    # or just use find contours using cv2.
    import cv2
    import numpy as np
    
    # Load image for cv2
    cv_img = cv2.imread(img_path)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    
    # Threshold to find the white rounded boxes
    # The boxes are white (close to 255)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours left to right
    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    
    # Filter boxes that are roughly square and have a reasonable size (e.g. at least 30x30)
    valid_boxes = [b for b in bounding_boxes if b[2] > 30 and b[3] > 30 and 0.8 < b[2]/b[3] < 1.2]
    
    valid_boxes.sort(key=lambda x: x[0])
    
    for i, (x, y, w, h) in enumerate(valid_boxes[:4]):
        # Crop with some padding if needed, or exact box
        cropped = img.crop((x, y, x+w, y+h))
        cropped.save(f"badge_{i+1}.png")
        print(f"Saved badge_{i+1}.png")

if __name__ == '__main__':
    extract_badges()

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    import os
    import random

    # Create directory if it doesn't exist
    os.makedirs("static/images", exist_ok=True)
    
    # Create a placeholder image
    width, height = 1920, 1080
    
    # Create image and drawing context - Gradient background
    img = Image.new('RGB', (width, height), color=(25, 68, 142))
    draw = ImageDraw.Draw(img)
    
    # Create a gradient background (dark blue to black)
    for y in range(height):
        for x in range(width):
            # Calculate gradient color
            r = int(25 - (y / height) * 25)
            g = int(68 - (y / height) * 68)
            b = int(142 - (y / height) * 50)
            draw.point((x, y), fill=(r, g, b))
    
    # Add some random stars
    for _ in range(300):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 3)
        brightness = random.randint(150, 255)
        draw.ellipse((x, y, x+size, y+size), fill=(brightness, brightness, brightness))
    
    # Add a subtle plane silhouette
    try:
        # Draw a simple airplane silhouette
        plane_color = (255, 255, 255, 100)  # Semi-transparent white
        
        # Main body of the plane
        x_center = width // 2
        y_center = height // 3
        
        # Wings
        points = [
            (x_center - 200, y_center),
            (x_center - 100, y_center - 50),
            (x_center + 100, y_center - 50),
            (x_center + 200, y_center),
            (x_center + 100, y_center + 50),
            (x_center - 100, y_center + 50),
        ]
        draw.polygon(points, fill=(255, 255, 255, 30))
        
        # Body
        draw.ellipse((x_center - 30, y_center - 100, x_center + 30, y_center + 100), 
                    fill=(255, 255, 255, 50))
    except Exception as e:
        print(f"Couldn't draw plane: {e}")
    
    # Try to add text
    try:
        # Use default system font or specify a path to a font file
        font_size = 60
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
            smaller_font = ImageFont.truetype("arial.ttf", font_size // 2)
        except:
            font = ImageFont.load_default()
            smaller_font = ImageFont.load_default()
        
        # Add text
        text = "FlightFinder"
        try:
            text_width, text_height = font.getbbox(text)[2:4]  # For newer Pillow versions
        except:
            try:
                text_width, text_height = draw.textsize(text, font=font)  # For older Pillow versions
            except:
                text_width, text_height = 300, 60  # Fallback dimensions
                
        position = ((width - text_width) // 2, (height - text_height) // 2)
        
        # Add a subtle glow effect (multiple layers with increasing transparency)
        for offset in range(10, 0, -2):
            draw.text((position[0] - offset, position[1]), text, fill=(255, 140, 0, 20), font=font)
            draw.text((position[0] + offset, position[1]), text, fill=(255, 140, 0, 20), font=font)
            draw.text((position[0], position[1] - offset), text, fill=(255, 140, 0, 20), font=font)
            draw.text((position[0], position[1] + offset), text, fill=(255, 140, 0, 20), font=font)
            
        # Main text
        draw.text(position, text, fill=(255, 255, 255), font=font)
        
        # Tagline
        tagline = "Find your perfect flight"
        try:
            tagline_width, tagline_height = smaller_font.getbbox(tagline)[2:4]
        except:
            try:
                tagline_width, tagline_height = draw.textsize(tagline, font=smaller_font)
            except:
                tagline_width, tagline_height = 200, 30
                
        tagline_position = ((width - tagline_width) // 2, position[1] + text_height + 20)
        draw.text(tagline_position, tagline, fill=(255, 140, 0), font=smaller_font)
        
    except Exception as e:
        print(f"Couldn't add text: {e}")
    
    # Apply a slight blur for a more professional look
    try:
        img = img.filter(ImageFilter.GaussianBlur(radius=1.5))
    except Exception as e:
        print(f"Couldn't apply blur: {e}")
        
    # Save the image
    img.save("static/images/logon.jpg", quality=95)
    print("Improved background image created at static/images/logon.jpg")
    
except ImportError:
    print("The PIL library is not installed. Please install it:")
    print("Run: pip install Pillow")
    print("Then run this script again.")

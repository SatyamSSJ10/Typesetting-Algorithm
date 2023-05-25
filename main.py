import ast
from PIL import Image, ImageDraw, ImageFont

# Load an image (change the path to an actual image file)
image = Image.open('Screenshot 2023-05-25 131902.jpg')
draw = ImageDraw.Draw(image)

# Set a minimum acceptable font size
min_font_size = 12
line_spacing_multiplier = 1

def split_into_lines(text, font, draw, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        proposed_line = current_line + [word]
        # Check if adding the next word exceeds the max width
        if draw.textsize(' '.join(proposed_line), font=font)[0] <= max_width:
            current_line = proposed_line
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line)) # Add the last line
    return lines

with open('text_boxes.txt', 'r') as f:
    for line in f:
        # Convert the line to a list
        text_list = ast.literal_eval(line.strip())
        
        # Extract text and bounding box
        text, bbox = text_list[0], text_list[1]
        draw.rectangle(bbox, fill="white")
        if len(text.strip()) == 0:
            # If the text is empty or only consists of spaces, skip this line
            continue

        # Create a font
        font = ImageFont.truetype("arial.ttf", min_font_size)
        
        # Increase the width of the bounding box by 20% if needed
        max_width = bbox[2] - bbox[0]
        lines = split_into_lines(text, font, draw, max_width)
        if draw.textsize(max(lines, key=len), font=font)[0] > max_width:
            bbox[2] = int(bbox[2] + 0.2 * (bbox[2] - bbox[0]))
            max_width = bbox[2] - bbox[0]
            lines = split_into_lines(text, font, draw, max_width)

        # Calculate the total text height and the line height
        line_height = draw.textsize('Ay', font=font)[1]
        total_text_height = line_height * len(lines) * line_spacing_multiplier

        # Calculate the y-coordinate of the first line to center the text vertically
        start_y = bbox[1] + (bbox[3] - bbox[1] - total_text_height) / 2

        # Draw the bounding boxes and text
        for i, line in enumerate(lines):
            line_bbox = [bbox[0], start_y + i * line_height, bbox[2], start_y + (i + 1) * line_height]
            draw.rectangle(line_bbox, fill="white")

            # Calculate the centered text position
            text_width, text_height = draw.textsize(line, font)
            text_x = line_bbox[0] + ((line_bbox[2] - line_bbox[0] - text_width) / 2)
            text_y = line_bbox[1] + ((line_bbox[3] - line_bbox[1] - text_height) / 2)

            # Draw the text on the image
            draw.text((text_x, text_y), line, (0, 0, 0), font=font)  # Draw text in black color

# Save the image
image.save("output.jpg")

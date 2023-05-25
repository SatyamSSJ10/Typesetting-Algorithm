import ast
from PIL import Image, ImageDraw, ImageFont

# Load an image (change the path to an actual image file)
image = Image.open('Screenshot 2023-05-25 131902.jpg')
draw = ImageDraw.Draw(image)

# Set a minimum acceptable font size
min_font_size = 10

def split_text(text, max_lines):
    words = text.split()
    if len(words) <= max_lines:
        return words
    lines = []
    for i in range(0, len(words), len(words) // max_lines):
        lines.append(' '.join(words[i:i + len(words) // max_lines]))
    return lines

with open('text_boxes.txt', 'r') as f:
    for line in f:
        # Convert the line to a list
        text_list = ast.literal_eval(line.strip())
        
        # Extract text and bounding box
        text, bbox = text_list[0], text_list[1]

        if len(text.strip()) == 0:
            # If the text is empty or only consists of spaces, skip this line
            continue

        # Calculate the maximum number of lines that can fit in the bounding box
        font = ImageFont.truetype("arial.ttf", min_font_size)
        _, min_font_height = draw.textsize("A", font)  # This gives us the height of a line of text
        max_lines = max(1, (bbox[3] - bbox[1]) // min_font_height)

        # Split the text into the calculated number of lines
        lines = split_text(text, max_lines)
        if len(lines) > max_lines:
            # If the text doesn't fit, increase the bounding box by 20%
            bbox[3] = int(bbox[3] + 0.2 * (bbox[3] - bbox[1]))
            max_lines = len(lines)

        # Adjust the bounding box height for each line of text
        line_height = (bbox[3] - bbox[1]) // len(lines)

        # Draw the bounding boxes and text
        for i, line in enumerate(lines):
            line_bbox = [bbox[0], bbox[1] + i * line_height, bbox[2], bbox[1] + (i + 1) * line_height]
            draw.rectangle(line_bbox, fill="white")

            # Load a font
            font = ImageFont.truetype("arial.ttf", min_font_size)

            # Start with small font size and increment until the text is too big for the box
            text_width, text_height = draw.textsize(line, font)
            while text_width < line_bbox[2] - line_bbox[0] and text_height < line_bbox[3] - line_bbox[1]:
                font = ImageFont.truetype("arial.ttf", font.size + 1)
                text_width, text_height = draw.textsize(line, font)

            # Once the text is too big, decrement the font size to make it fit in the box
            font = ImageFont.truetype("arial.ttf", font.size - 1)
            text_width, text_height = draw.textsize(line, font)

            # Calculate the centered text position
            text_x = line_bbox[0] + ((line_bbox[2] - line_bbox[0] - text_width) / 2)
            text_y = line_bbox[1] + ((line_bbox[3] - line_bbox[1] - text_height) / 2)

            # Draw the text on the image
            draw.text((text_x, text_y), line, (0, 0, 0), font=font)  # Draw text in black color

# Save the image
image.save("output.jpg")

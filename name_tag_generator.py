import os
from PIL import Image, ImageDraw, ImageFont

# Load the template image
template_path = 'assets/background-1.png'
template = Image.open(template_path)

# Define font and text color
font_path = 'assets/MateSC-Regular.ttf'  # Replace with the path to your font file
font_size = 50
font = ImageFont.truetype(font_path, font_size)
text_color = (0, 0, 0)  # White color, you can change this



# List of names
names = []  # Replace this with your list of names
with open('assets/names.txt', 'r') as names_file:
    names = names_file.read().splitlines();

def create_folder_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")
    else:
        print(f"Folder '{folder_name}' already exists.")

create_folder_if_not_exists('output/')

def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

for name in names:
    print(f"Generating for {name} ")
    img_with_text = template.copy()
    draw = ImageDraw.Draw(img_with_text)

    # Split the name into words
    whole_name = name.split()

    # Combine all except the last word with spaces
    first_name = ' '.join(whole_name[:-1])
    last_name = whole_name[-1]

    # Split the name into lines with a maximum width of the image
    max_width = img_with_text.width
    lines = [name]

    # Calculate total text height
    if len(whole_name) == 1:
        total_text_height = get_text_dimensions(whole_name[0], font=font)[1]
    else:
        lines = [first_name, last_name]
        total_text_height = sum(get_text_dimensions(line, font=font)[1] for line in lines)

    # Calculate starting position to center vertically
    y_position = (img_with_text.height - total_text_height) / 2

    # Draw each line of text
    for line in lines:
        text_width, text_height = get_text_dimensions(line, font=font)
        x_position = (img_with_text.width - text_width) / 2
        draw.text((x_position, y_position), line, font=font, fill=text_color)
        y_position += text_height  # Move to the next line

    # Save generated image with the name
    img_with_text.save(f'output/{name.replace(" ", "_")}.png')  # Change 'output_' as needed

# Create images for each name
# for name in names:
#     img_with_text = template.copy()
#     draw = ImageDraw.Draw(img_with_text)

#     # Split the name into words
#     name_parts = name.split()

#     # Combine all except the last word with spaces
#     first_part = ' '.join(name_parts[:-1])

#     # Calculate text size and position
#     text_width, text_height = get_text_dimensions(first_part, font=font)
#     text_position = ((img_with_text.width - text_width) / 2, (img_with_text.height - text_height) / 2)

#     # Add the first part to the image
#     draw.text(text_position, first_part, font=font, fill=text_color)

#     # Calculate text size for the surname
#     last_part_width, last_part_height = get_text_dimensions(name_parts[-1], font=font)
#     last_part_position = ((img_with_text.width - last_part_width) / 2, ((img_with_text.height - text_height) / 2) + text_height)

#     # Add the last part (on a new line) to the image
#     draw.text(last_part_position, name_parts[-1], font=font, fill=text_color)


#     # Save generated image with the name
#     img_with_text.save(f'output/{name.replace(" ", "_")}.png')  # Change 'output_' as needed

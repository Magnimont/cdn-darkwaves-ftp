from PIL import Image, ImageDraw, ImageOps
from easy_pil import Font
from io import BytesIO
from werkzeug.datastructures import FileStorage

def gen_image(title: str, description: str, category: str, author_name: str, uploaded_file: any, output_file_path: str) -> None:
    # Load the uploaded image (author image)
    author_image = Image.open(uploaded_file)

    # Create a new image for the banner
    banner_width = 800
    banner_height = 500
    banner_color = "#E5E5E5"
    banner = Image.new('RGB', (banner_width, banner_height), banner_color)

    # Set up drawing context
    draw = ImageDraw.Draw(banner)

    poppins = Font.poppins(size=40)
    poppins_small = Font.poppins(size=30)

    # Add title
    # Calculate width and height of the text
    def get_text_center(text):
        text_width = draw.textlength(text, font=poppins)
        # Calculate the x position
        x_position = (banner_width - text_width) / 2
        return x_position

    draw.text((get_text_center(title), 20),
              text=title, fill="black", font=poppins)
    # Add description
    max_desc_width = banner_width - 40  # 20px padding on each side
    lines = []
    words = description.split()
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        test_width = draw.textlength(test_line, font=poppins_small)
        if test_width <= max_desc_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + ' '
    lines.append(current_line.strip())
    desc_position = (20, (200 - 60))
    lines_max = 0
    for line in lines:
        draw.text(desc_position, line, fill="black", font=poppins_small)
        desc_position = (desc_position[0], desc_position[1] + 40)
        lines_max = lines_max + 30

    if (lines_max > 130):
        lines_max = 130
    # Add category
    draw.text((20, 200 + lines_max), "Category : "+category,
              fill="black", font=poppins_small)

    # Add author card
    author_card_width = max_desc_width
    author_card_height = 100
    author_card_position = (10, 381)
    author_card_color = "#f0f0f0"
    author_card = Image.new(
        'RGB', (author_card_width, author_card_height),
        author_card_color)
    author_card_draw = ImageDraw.Draw(author_card)
    author_card_draw.text((100, 10), "Author:",
                          fill="black", font=poppins_small)
    author_card_draw.text((100, 50), author_name,
                          fill="black", font=poppins_small)

    # Apply rounded corners to the author card
    border_radius = 20  # Adjust border radius as needed
    rounded_mask = Image.new("L", (author_card_width, author_card_height), 0)
    draw = ImageDraw.Draw(rounded_mask)
    draw.rounded_rectangle((0, 0, author_card_width, author_card_height),
                           radius=border_radius, fill=255)
    author_card_rounded = Image.new(
        "RGB", (author_card_width, author_card_height), banner_color)
    author_card_rounded.paste(author_card, (0, 0), mask=rounded_mask)

    # Paste author image onto author card
    resized_size = (80, 80)
    author_image_resized = author_image.resize(resized_size)
    # Apply rounded corners to the image with a larger radius
    rounded_mask_author = Image.new("L", resized_size, 0)
    draw_author = ImageDraw.Draw(rounded_mask_author)
    draw_author.rounded_rectangle((0, 0, *resized_size),
                                  radius=border_radius * 20, fill=255)
    # Paste the author image with border onto the rounded mask
    author_image_resized_rounded = Image.new(
        "RGB", resized_size, author_card_color)
    author_image_resized_rounded.paste(
        author_image_resized, (0, 0), mask=rounded_mask_author)

    author_card_rounded.paste(author_image_resized_rounded, (13, 10))

    # Paste author card onto banner
    banner.paste(author_card_rounded, author_card_position)

    # Save image
    banner.save(output_file_path)


def gen_ProfilePicture(name: str) -> FileStorage:
    # Extract the first one or two letters of the name
    initials = name[:2].upper()
    print(f"Initials: {initials}")

    # Define the size of the avatar image
    avatar_size = (100, 100)
    background_color = "#3498db"  # A nice blue color
    text_color = "#ffffff"  # White text color

    # Create a new image with the specified background color
    avatar = Image.new('RGB', avatar_size, background_color)

    # Set up drawing context
    draw = ImageDraw.Draw(avatar)

    # Choose a font and size
    poppins = Font.poppins(size=40)

    # Calculate text size and position to center it
    text_width = draw.textlength(initials, font=poppins)
    text_height = 40  # Since we are using a font size of 40
    print(f"Text Width: {text_width}, Text Height: {text_height}")
    text_x = (avatar_size[0] - text_width) // 2
    text_y = (avatar_size[1] - text_height) // 2

    # Draw the text on the image
    draw.text((text_x, text_y), initials, fill=text_color, font=poppins)

    # Save the image to a BytesIO object
    image_stream = BytesIO()
    avatar.save(image_stream, format='PNG')
    image_stream.seek(0)  # Rewind the stream to the beginning

    # Create a FileStorage object
    return FileStorage(stream=image_stream, filename='avatar.png', content_type='image/png')

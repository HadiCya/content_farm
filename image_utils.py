from PIL import Image, ImageDraw, ImageFont
import textwrap


def generate_imessage_style_conversation(messages, file_path):
    # Create a blank image with a white background
    image_width = 800
    # Adjusted height calculation based on message count
    image_height = len(messages) * 150

    # Load a custom font
    font_path = "template/SF-Pro-Text-Semibold.otf"
    font_size = 24
    font = ImageFont.truetype(font_path, font_size)

    # Define colors for iMessage style
    sender_bubble_color = '#1d8bff'
    sender_text_color = '#ffffff'
    receiver_bubble_color = '#3b3b3d'
    receiver_text_color = '#e1e1e1'
    background_color = '#1e1e1e'

    # Set initial positions for the conversation
    padding = 16
    max_width = image_width - 2 * padding
    y = padding
    gap_between_bubbles = 10
    gap_between_senders = 20

    image = Image.new('RGB', (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    # Helper function to draw a tail
    def draw_tail(draw, bubble_x, bubble_y, message_user, bubble_width, bubble_height):
        if message_user == 'sender':
            tail_coordinates = [
                (bubble_x + bubble_width, bubble_y + bubble_height - 16),
                (bubble_x + bubble_width - 8, bubble_y + bubble_height - 8),
                (bubble_x + bubble_width + 8, bubble_y + bubble_height)
            ]
        else:
            tail_coordinates = [
                (bubble_x, bubble_y + bubble_height - 16),
                (bubble_x + 8, bubble_y + bubble_height - 8),
                (bubble_x - 8, bubble_y + bubble_height)
            ]
        draw.polygon(tail_coordinates, fill=(
            sender_bubble_color if message_user == 'sender' else receiver_bubble_color))

    # Draw the conversation on the image
    for index, message in enumerate(messages):
        timestamp = message.get('time', None)
        if timestamp:
            timestamp_font_size = 16
            timestamp_font = ImageFont.truetype(font_path, timestamp_font_size)
            timestamp_width, timestamp_height = draw.textsize(
                timestamp, font=timestamp_font)

            # Center the timestamp
            timestamp_x = (image_width - timestamp_width) / 2
            timestamp_y = y  # Set the y position for the timestamp
            draw.text((timestamp_x, timestamp_y), timestamp,
                      fill='#a1a1a1', font=timestamp_font)

            # Add some space below the timestamp before the next message bubble
            y += timestamp_height + gap_between_bubbles
            continue

        message_text = message.get('text', None)
        message_user = message.get('user', None)
        if not message_text or not message_user:
            continue

        wrapped_message = textwrap.fill(message_text, width=30)
        wrapped_lines = wrapped_message.split('\n')

        # Calculate bubble size
        bubble_width = max(draw.textsize(line, font=font)[
            0] for line in wrapped_lines) + 2 * padding
        bubble_height = sum(draw.textsize(line, font=font)[
            1] for line in wrapped_lines) + padding

        # Ensure bubble dimensions are correct
        bubble_width = min(bubble_width, max_width)
        bubble_height = max(bubble_height, font.getsize(
            message_text)[1] + padding)

        # Ensure that bubble_height is always positive
        if bubble_height <= 0:
            bubble_height = font.getsize(message_text)[1] + padding

        # Draw message bubble
        if message_user == 'sender':
            bubble_x = image_width - bubble_width - padding
        else:
            bubble_x = padding

        bubble_y = y
        bubble_bottom_y = bubble_y + bubble_height

        messages[index]["bubble_y"] = bubble_y
        messages[index]["bubble_bottom_y"] = bubble_bottom_y

        # Draw rounded rectangle for the bubble
        draw.rounded_rectangle(
            [(bubble_x, bubble_y), (bubble_x + bubble_width, bubble_bottom_y)],
            fill=(sender_bubble_color if message_user ==
                  'sender' else receiver_bubble_color),
            radius=20
        )

        # Calculate text position inside the bubble
        text_x = bubble_x + padding
        text_y = bubble_y + padding / 2

        # Draw the text line by line
        for line in wrapped_lines:
            draw.text((text_x, text_y), line, fill=(
                sender_text_color if message_user == 'sender' else receiver_text_color), font=font)
            text_y += draw.textsize(line, font=font)[1]

        # Draw message bubble with a tail if it's the last one from this user
        try:
            is_last_message_from_user = (index == len(
                messages) - 1) or (messages[index + 1]['user'] != message_user)
            if is_last_message_from_user:
                draw_tail(draw, bubble_x, bubble_y, message_user,
                          bubble_width, bubble_height)
        except:
            pass

        subtitle = message.get('subtitle', None)
        if subtitle and message_user == 'sender':
            subtitle_font_size = 14
            subtitle_font = ImageFont.truetype(font_path, subtitle_font_size)
            subtitle_x = bubble_x + bubble_width - \
                draw.textsize(subtitle, font=subtitle_font)[0]
            subtitle_y = bubble_bottom_y + 5  # A small gap below the bubble
            draw.text((subtitle_x, subtitle_y), subtitle,
                      fill=receiver_text_color, font=subtitle_font)
            # Adjust for subtitle height
            y += subtitle_font.getsize(subtitle)[1] + 5

        # Update y for the next message, ensuring space between bubbles
        y = bubble_bottom_y + gap_between_bubbles

        # Add extra gap when switching between senders
        try:
            if messages.index(message) < len(messages) - 1 and message_user != messages[messages.index(message) + 1]['user']:
                y += gap_between_senders
        except:
            pass

    # Save or display the image
    image.save(file_path)
    return messages

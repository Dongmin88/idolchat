import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, LEFT, RIGHT
from toga.colors import rgb, WHITE, BLACK
import json
import os
import asyncio

def create_character_selection_screen(app):
    characters = {
        "Character 1": "character1.png",
        "Character 2": "character2.png",
        "Character 3": "character3.png",
        "Character 4": "character4.png",
        "Character 5": "character5.png",
        "Character 6": "character6.png"
    }

    main_box = toga.Box(style=Pack(direction=COLUMN, padding=20, background_color=WHITE))
    title = toga.Label('Select Your Character', style=Pack(text_align='center', font_size=24, padding=(0, 0, 20, 0), color=rgb(25, 25, 25)))
    main_box.add(title)

    row_box = toga.Box(style=Pack(direction=ROW, padding=10))
    
    for index, (character, image_path) in enumerate(characters.items()):
        character_box = create_character_button(app, character, image_path)
        row_box.add(character_box)

        if (index + 1) % 3 == 0:
            main_box.add(row_box)
            row_box = toga.Box(style=Pack(direction=ROW, padding=10))

    if len(characters) % 3 != 0:
        main_box.add(row_box)
    
    return main_box

def create_character_button(app, character, image_path):
    try:
        character_image = toga.Image(image_path)
        image_view = toga.ImageView(character_image, style=Pack(width=100, height=100))
    except Exception as e:
        print(f"Error loading image for {character}: {e}")
        image_view = toga.Label("이미지 없음", style=Pack(width=100, height=100, background_color=rgb(255, 193, 7)))

    character_label = toga.Label(character, style=Pack(padding_top=5, font_weight='bold', color=rgb(25, 25, 25)))
    button = toga.Button(
        "선택",
        on_press=lambda widget, char=character: show_chat_screen(app, char),
        style=Pack(padding=(10, 5), background_color=rgb(255, 235, 0), color=BLACK)
    )

    character_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER, padding=10, width=120))
    character_box.add(image_view)
    character_box.add(character_label)
    character_box.add(button)
    return character_box

def show_chat_screen(app, character):
    try:
        app.main_window.content = create_chat_screen(app, character)
    except Exception as e:
        print(f"Error creating chat screen: {e}")

def create_chat_screen(app, character):
    main_box = toga.Box(style=Pack(direction=COLUMN, padding=20, background_color=WHITE))

    title = toga.Label(f'Chat with {character}', style=Pack(text_align='center', font_size=24, padding=(0, 0, 20, 0), color=BLACK))
    main_box.add(title)

    message_area = toga.MultilineTextInput(
    readonly=True, 
    style=Pack(flex=1, padding=10, height=400, background_color=rgb(240, 240, 240), color=BLACK)
)

    previous_messages = load_conversation(character)
    message_area.value = previous_messages

    main_box.add(message_area)

    input_box = toga.Box(style=Pack(direction=ROW, padding=10, background_color=WHITE))
    user_input = toga.TextInput(placeholder="메시지를 입력하세요", style=Pack(flex=1, padding=(0, 10, 0, 0), background_color=WHITE, color=BLACK))
    send_button = toga.Button("전송", 
                              on_press=lambda widget: send_message(app, user_input, message_area, character),
                              style=Pack(background_color=rgb(255, 235, 0), color=BLACK, padding=10, width=80, text_align=CENTER))
    input_box.add(user_input)
    input_box.add(send_button)
    
    main_box.add(input_box)
    return main_box




async def scroll_to_bottom(message_area):
    """스크롤을 아래로 이동시키기 위한 비동기 함수"""
    await asyncio.sleep(0.1)  # 살짝 대기 후 스크롤 업데이트
    message_area.selection = (len(message_area.value), len(message_area.value))
    message_area.scroll = len(message_area.value)
    message_area.refresh()

def send_message(app, user_input, message_area, character):
    user_message = user_input.value
    if user_message.strip() == "":
        return

    # Append the user message and bot response
    message_area.value += f"You: {user_message}\n"
    bot_response = bot_reply(user_message, character)
    message_area.value += f"{character}: {bot_response}\n\n"

    # Clear the input field
    user_input.value = ""

    # Scroll to the bottom of the message area
    asyncio.create_task(scroll_to_bottom(message_area))

    # Save the conversation
    save_conversation(character, message_area.value)



def bot_reply(user_message, character):
    responses = {
        "안녕": f"{character}가 인사합니다. 안녕하세요! 어떻게 도와드릴까요?",
        "이름": f"저는 {character}입니다.",
        "잘가": f"{character}가 작별 인사합니다. 다음에 또 봐요!"
    }
    return responses.get(user_message, "죄송합니다, 무슨 말인지 잘 모르겠어요.")

def save_conversation(character, conversation):
    file_path = f"{character}_conversation.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump({"conversation": conversation}, f, ensure_ascii=False, indent=4)

def load_conversation(character):
    file_path = f"{character}_conversation.json"
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(data)
            return data.get("conversation", "")
    return ""

import toga
from toga.style import Pack
from toga.colors import rgb
from .functions import (
    create_character_selection_screen, 
    show_chat_screen
)

class IdolChatApp(toga.App):
    def startup(self):
        self.primary_color = rgb(0, 0, 255)  # Blue
        self.secondary_color = rgb(255, 193, 7)  # Yellow
        self.background_color = rgb(248, 249, 250)  # Light gray/white

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = create_character_selection_screen(self)
        self.main_window.show()

def main():
    return IdolChatApp("Idol Chat", "com.example.idolchat")

if __name__ == '__main__':
    app = main()
    app.main_loop()
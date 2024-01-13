import cv2
import os
import threading
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock
from PIL import Image as PILImage
import pytesseract
from gtts import gTTS

class SpeakTureApp(App):
    def build(self):
        Builder.load_file('project.kv')
        return self.root

class SpeakTureApp(App):
    def build(self):
        self.title = 'SpeakTure'
        self.root = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Title Label
        title_label = Label(text='SPEAKTURE', font_size=20, bold=True, size_hint_y=None, height=50)
        self.root.add_widget(title_label)

        # Image Display
        self.image_display = KivyImage(size=(300, 200))
        self.root.add_widget(self.image_display)

        # Buttons
        button_layout = BoxLayout(spacing=10)

        capture_button = Button(text='Capture', on_press=self.open_camera)
        browse_button = Button(text='Browse', on_press=self.browse_image)

        button_layout.add_widget(capture_button)
        button_layout.add_widget(browse_button)

        self.root.add_widget(button_layout)

        return self.root

    def open_camera(self, instance):
        threading.Thread(target=self.capture_and_ocr).start()

    def browse_image(self, instance):
        file_chooser = FileChooserListView()
        file_chooser.bind(on_submit=self.process_selected_file)

        popup_layout = BoxLayout(orientation='vertical', spacing=10)
        popup_layout.add_widget(file_chooser)

        popup = Popup(title='Choose an Image', content=popup_layout, size_hint=(0.9, 0.9))
        popup.open()

    def process_selected_file(self, instance, value):
        file_path = value[0]
        if file_path:
            image = cv2.imread(file_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            print("Captured Text:", text)
            self.text_to_speech(text)

    def capture_and_ocr(self):
        video = cv2.VideoCapture(1)
        while True:
            _, frame = video.read()
            cv2.imshow("Camera", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                text = pytesseract.image_to_string(gray)
                print("Captured Text:", text)
                self.text_to_speech(text)
        video.release()
        cv2.destroyAllWindows()

    def text_to_speech(self, text):
        if text and text.strip():
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save("output.mp3")
            os.system("start output.mp3")
        else:
            print("No text to speak")

if __name__ == '__main__':
    SpeakTureApp().run()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from plyer import filechooser
import pandas as pd
import re
import pytesseract
from pdf2image import convert_from_path
import numpy as np

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def process_pdf(pdf_path):
    pages = convert_from_path(pdf_path, dpi=200)
    data = []

    for page in pages:
        img = np.array(page)
        text = pytesseract.image_to_string(img, lang='eng')

        ids = re.findall(r'[A-Z]{3}\d{7}', text)

        for i in ids:
            data.append({"Voter ID": i})

    df = pd.DataFrame(data)
    output = "/storage/emulated/0/Download/Voter_App_Output.xlsx"
    df.to_excel(output, index=False)

    return output


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.label = Label(text="📄 Select PDF")
        layout.add_widget(self.label)

        btn1 = Button(text="Select PDF")
        btn1.bind(on_press=self.select_file)
        layout.add_widget(btn1)

        btn2 = Button(text="Process")
        btn2.bind(on_press=self.process)
        layout.add_widget(btn2)

        return layout

    def select_file(self, instance):
        filechooser.open_file(on_selection=self.handle)

    def handle(self, selection):
        if selection:
            self.path = selection[0]
            self.label.text = self.path

    def process(self, instance):
        if not hasattr(self, "path"):
            self.label.text = "❌ Select file first"
            return

        self.label.text = "⏳ Processing..."
        try:
            out = process_pdf(self.path)
            self.label.text = f"✅ Saved:\n{out}"
        except Exception as e:
            self.label.text = str(e)


MyApp().run()

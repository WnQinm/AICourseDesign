import gradio as gr
from src import *


class MyApp:
    def __init__(self):
        self.app = gr.Blocks()
        self.select_model = SelectModel()
        self.tabs = [
            tab1(select_model=self.select_model),
            tab2(select_model=self.select_model),
            tab3(select_model=self.select_model),
        ]

    def launch(self):
        with self.app:
            self.select_model.select_model()
            with gr.Tabs():
                for tab in self.tabs:
                    tab.create_tab()
        self.app.launch()


if __name__ == "__main__":
    app = MyApp()
    app.launch()

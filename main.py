import gradio as gr
from tab1 import TAB as tab1
from tab2 import TAB as tab2
from tab3 import TAB as tab3


class MyApp:
    def __init__(self):
        self.app = gr.Blocks()
        self.tabs = [tab1(), tab2(), tab3()]

    def launch(self):
        with self.app:
            with gr.Tabs():
                for tab in self.tabs:
                    tab.create_tab()
        self.app.launch()


if __name__ == "__main__":
    app = MyApp()
    app.launch()

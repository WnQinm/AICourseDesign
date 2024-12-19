import os
import json
from datetime import datetime
from typing import List, Dict
import gradio as gr
from .utils import BASE_TAB


# 角色扮演+多轮对话
class TAB(BASE_TAB):
    '''
    - 设计一个用于可以与语言模型进行角色扮演游戏的机器人,实现多轮对话互动
    - 与语言模型交互2轮 (提示语不算)
    - 记录并多轮对话的对话历史
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chatbot_prompt = "You are a helpful assistant."

    def submitButtonClick(self, user_input):
        if user_input != "":
            model_output = self.generate(user_input)
        return self.history, ""

    def clear_history(self):
        self.system_prompt = [{"role": "system", "content": self.chatbot_prompt}]
        self.history = []
        return gr.Button(visible=True), gr.File(None, visible=False), gr.Chatbot(label=None, show_label=False)

    def change_memory_size(self, memory_size):
        self.memory_size = memory_size

    def create_history_file(self):
        os.makedirs("./gradioTempFolder", exist_ok=True)
        file_name = "./gradioTempFolder/"+datetime.now().strftime("%y%m%d%H%M%S_summary.json")
        with open(file_name, "w", encoding='utf-8') as f:
            f.write(json.dumps(self.all_history, ensure_ascii=False))
        return gr.Button(visible=False), gr.File(file_name, visible=True)

    def download_history(self):
        return gr.Button(visible=True), gr.File(None, visible=False)

    def example1_click(self):
        self.system_prompt = [{"role": "system", "content": self.chatbot_prompt}]
        self.history = []

        prompt = "我想让你充当 Linux 终端。我将输入命令，您将回复终端应显示的内容。我希望您只在一个唯一的代码块内回复终端输出，而不是其他任何内容。不要写解释。除非我指示您这样做，否则不要键入命令。当我需要用英语告诉你一些事情时，我会把文字放在中括号内[就像这样]。"
        self.system_prompt.append({"role": "system", "content": prompt})

        model_output = self.generate("pwd")
        return gr.Button(visible=True), gr.File(None, visible=False), gr.Chatbot(self.history, label="Linux终端", show_label=True)

    def example2_click(self):
        self.system_prompt = [{"role": "system", "content": self.chatbot_prompt}]
        self.history = []

        prompt = "我想让你扮演一个井字游戏的角色。我负责走棋，你负责更新棋盘以反映我的行动，并决定是否有赢家或平局。用 X 表示我的动作，用 O 表示电脑的动作。除了展示电脑动作之后的棋盘结果和决定游戏结果之外，不要提供任何其他解释或指示。"
        self.system_prompt.append({"role": "system", "content": prompt})

        model_output = self.generate("左上")
        return gr.Button(visible=True), gr.File(None, visible=False), gr.Chatbot(self.history, label="井字棋", show_label=True)

    def example3_click(self):
        self.system_prompt = [{"role": "system", "content": self.chatbot_prompt}]
        self.history = []

        prompt = "我希望你像 Python 解释器一样行事。我会给你 Python 代码，你会执行它。不要提供任何解释。除了代码的输出之外，不要响应任何内容。"
        self.system_prompt.append({"role": "system", "content": prompt})

        model_output = self.generate("print('hello world!')")
        return gr.Button(visible=True), gr.File(None, visible=False), gr.Chatbot(self.history, label="Python解释器", show_label=True)

    def create_tab(self):
        with gr.Tab("2. 角色扮演"):
            with gr.Row():
                with gr.Column(scale=10):
                    chatbot = gr.Chatbot(show_label=False, type="messages")
                    input_box = gr.Textbox(show_label=False, scale=10, submit_btn=True)
                with gr.Column(scale=1):
                    example1_button = gr.Button("实例一 Linux终端")
                    example2_button = gr.Button("实例二 井字棋")
                    example3_button = gr.Button("实例三 Python解释器")
                    memory_size_slider = gr.Slider(minimum=0, maximum=5, step=1, value=self.memory_size, label="记忆长度")
                    download_button = gr.Button("下载对话历史", scale=1)
                    history_file = gr.File(None, visible=False, show_label=False, scale=4)

        input_box.submit(self.submitButtonClick, [input_box], [chatbot, input_box])
        chatbot.clear(self.clear_history, None, [download_button, history_file, chatbot])
        memory_size_slider.change(self.change_memory_size, [memory_size_slider], None)
        download_button.click(self.create_history_file, None, [download_button, history_file])
        history_file.download(self.download_history, None, [download_button, history_file])

        example1_button.click(self.example1_click, None, [download_button, history_file, chatbot])
        example2_button.click(self.example2_click, None, [download_button, history_file, chatbot])
        example3_button.click(self.example3_click, None, [download_button, history_file, chatbot])
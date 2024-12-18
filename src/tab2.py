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
        # TODO 我想让你充当 Linux 终端。我将输入命令，您将回复终端应显示的内容。我希望您只在一个唯一的代码块内回复终端输出，而不是其他任何内容。不要写解释。除非我指示您这样做，否则不要键入命令。当我需要用英语告诉你一些事情时，我会把文字放在中括号内[就像这样]。我的第一个命令是 pwd
        # TODO 我想让你扮演一个井字游戏的角色。我负责走棋，你负责更新棋盘以反映我的行动，并决定是否有赢家或平局。用 X 表示我的动作，用 O 表示电脑的动作。除了更新棋盘和决定游戏结果之外，不要提供任何其他解释或指示。开始时，我将在棋盘的左上角放一个 X，作为第一步棋。
        # TODO 我希望你像 Python 解释器一样行事。我会给你 Python 代码，你会执行它。不要提供任何解释。除了代码的输出之外，不要响应任何内容。第一个代码是：“print('hello world!')”
        self.chatbot_prompt = "You are a helpful assistant."
        self.system_prompt = [{"role": "system", "content": self.chatbot_prompt}]

    def submitButtonClick(self, user_input):
        if user_input != "":
            model_output = self.generate(user_input)
        return self.history, ""

    def clear_history(self):
        self.history = []
        return gr.Button(visible=True), gr.File(None, visible=False)

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

    def create_tab(self):
        with gr.Tab("2. 角色扮演"):
            with gr.Column():
                chatbot = gr.Chatbot(show_label=False, type="messages")
                with gr.Row(equal_height=True):
                    input_box = gr.Textbox(scale=10, show_label=False)
                    submit_button = gr.Button("发送")
            with gr.Row(equal_height=True):
                memory_size_slider = gr.Slider(minimum=0, maximum=5, step=1, value=self.memory_size, label="记忆长度", scale=8)
                download_button = gr.Button("下载对话历史", scale=1)
                history_file = gr.File(None, visible=False, show_label=False, scale=4)

        submit_button.click(self.submitButtonClick, [input_box], [chatbot, input_box])
        chatbot.clear(self.clear_history, None, [download_button, history_file])
        memory_size_slider.change(self.change_memory_size, [memory_size_slider], None)
        download_button.click(self.create_history_file, None, [download_button, history_file])
        history_file.download(self.download_history, None, [download_button, history_file])

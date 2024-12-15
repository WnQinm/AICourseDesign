import gradio as gr
from base_tab import BASE_TAB


# 角色扮演+多轮对话
class TAB(BASE_TAB):
    '''
    - 设计一个用于可以与语言模型进行角色扮演游戏的机器人,实现多轮对话互动
    - 与语言模型交互2轮 (提示语不算)
    - 记录并多轮对话的对话历史
    '''
    def __init__(self):
        super().__init__()

    def create_tab(self):
        with gr.Tab("Tab 2"):
            with gr.Row():
                input2 = gr.Number(label="Number 1")
                input3 = gr.Number(label="Number 2")
                output2 = gr.Textbox(label="Sum", interactive=False)
            button2 = gr.Button("Add Numbers")

            def add_numbers(num1, num2):
                return f"Sum: {num1 + num2}"

            button2.click(add_numbers, inputs=[input2, input3], outputs=[output2])
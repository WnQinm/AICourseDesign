import gradio as gr
from .utils import BASE_TAB


# 自选
class TAB(BASE_TAB):
    '''
    - 自选一个定制服务机器人, 可以设想机器人需要完成的任何任务
    - 提示语：为大语言模型输入一个执行某项"任务"的指令(避免产生超过 1000 个 tokens 的输出)
    - 任务输入：输入"任务"的具体内容
    - 进行单轮或多轮对话均可，不超过 3 轮
    - 导出对话记录
    '''
    def create_tab(self):
        with gr.Tab("3. 定制服务机器人"):
            with gr.Row():
                file_input = gr.File(label="Upload a File")
                file_output = gr.Textbox(label="File Content", interactive=False)
            button3 = gr.Button("Read File")

            def read_file(file):
                if file is not None:
                    with open(file.name, "r") as f:
                        return f.read()
                return "No file uploaded."

            button3.click(read_file, inputs=[file_input], outputs=[file_output])
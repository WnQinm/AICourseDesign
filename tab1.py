import gradio as gr
from base_tab import BASE_TAB


# 文本摘要
class TAB(BASE_TAB):
    '''
    - 创建能够进行文章摘要的机器人
    - 设计提示语，以便让语言模型能够对文章进行总结
    - 保存摘要结果
    '''
    def __init__(self):
        super().__init__()

    def create_tab(self):
        with gr.Tab("Tab 1"):
            with gr.Row():
                input1 = gr.Textbox(label="Input 1")
                output1 = gr.Textbox(label="Output 1", interactive=False)
            button1 = gr.Button("Submit Tab 1")

            def process_tab1(input_text):
                return f"Processed: {input_text}"

            button1.click(process_tab1, inputs=[input1], outputs=[output1])
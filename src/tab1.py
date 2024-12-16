import os
from datetime import datetime
import json
import gradio as gr
from .utils import BASE_TAB


# 文本摘要
class TAB(BASE_TAB):
    '''
    - 创建能够进行文章摘要的机器人
    - 设计提示语，以便让语言模型能够对文章进行总结
    - 保存摘要结果
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._PreSetPrompt("请对冒号之后的文本用尽可能精简的语言进行概括")
        self.max_tokens = 300 * 1.65 + (300 / (1 - 0.11) - 300)

    def WordCntChange(self, slider_value):
        # 通义千问一个汉字平均对应1.5-1.8个token, 日常中文文本的标点符号占比约11%
        self.max_tokens = slider_value * 1.65 + (slider_value / (1 - 0.11) - slider_value)

    def SubmitButtonClick(self, text, word_cnt):
        self._PreSetPrompt(f"请对冒号之后的文本用尽可能精简的语言进行概括,最多{word_cnt}个汉字")
        summary = self.generate(text)

        os.makedirs("./gradioTempFolder", exist_ok=True)
        file_name = "./gradioTempFolder/"+datetime.now().strftime("%y%m%d%H%M%S_summary.txt")
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(json.dumps({
                "context": text,
                "summary": summary
            }))
        return summary, gr.File(file_name, visible=True)

    def create_tab(self):
        with gr.Tab("1. 文本摘要"):
            with gr.Column():
                with gr.Row(equal_height=True):
                    with gr.Column():
                        context = gr.Textbox(label="文章内容", lines=15, max_lines=15)
                        word_cnt = gr.Slider(minimum=10, maximum=1000, value=300, label="摘要字数限制")
                    summary = gr.Textbox(label="摘要", lines=15, max_lines=15)
                with gr.Row(equal_height=True):
                    submitButton = gr.Button("生成摘要")
                    downloadFile = gr.File(None, file_count="single", type="filepath", visible=False)
        word_cnt.change(self.WordCntChange, [word_cnt], None)
        submitButton.click(self.SubmitButtonClick, [context, word_cnt], [summary, downloadFile])

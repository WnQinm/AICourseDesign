import gradio as gr
from abc import ABC, abstractmethod
import requests
from typing import List, Dict


class SelectModel:
    def __init__(self):
        self.model_list:Dict[str, str] = {
                "---": ["---"],
                "qwen": ["qwen-max", "qwen-plus"],
            }
        self.current_model_serie:str = "---"
        self.current_model: str = "---"

    def ChangeModelBySerie(self, model_serie_value):
        return gr.Dropdown(
            choices=self.model_list[model_serie_value],
            value=self.model_list[model_serie_value][0]
        )

    def SubmitButtonClick(self, model_serie_value, model_value):
        self.current_model_serie = model_serie_value
        self.current_model = model_value
        return gr.Textbox(value=f"{self.current_model_serie} / {self.current_model}")

    def select_model(self):
        with gr.Row(equal_height=True):
            ShowCurrentModelTextbox = gr.Textbox(
                label="当前模型",
                value=f"{self.current_model_serie} / {self.current_model}",
                interactive=False,
            )
            ModelSerieSelectDropdown = gr.Dropdown(
                label="模型系列",
                choices=list(self.model_list.keys()),
                multiselect=False,
                value=self.current_model_serie,
            )
            ModelSelectDropdown = gr.Dropdown(
                label="模型名称",
                choices=self.model_list[self.current_model_serie],
                multiselect=False,
                value=self.current_model
            )
            ModelSubmitButton = gr.Button("修改模型")

        ModelSerieSelectDropdown.change(
            self.ChangeModelBySerie,
            [ModelSerieSelectDropdown],
            [ModelSelectDropdown]
        )
        ModelSubmitButton.click(
            self.SubmitButtonClick,
            [ModelSerieSelectDropdown, ModelSelectDropdown],
            [ShowCurrentModelTextbox]
        )


class BASE_TAB(ABC):
    def __init__(self, select_model:SelectModel):
        API_KEY = 0
        self.headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        # 历史对话记录
        self.history:List[Dict[str, str]] = []
        # 对话时模型可见的对话历史
        self.memory_size = 3

        self.max_tokens = 1024
        self.seed = 42

        self.select_model = select_model

    @property
    def current_model(self):
        return self.select_model.current_model

    def _PreSetPrompt(self, prompt):
        self.history = [{"role": "user", "content": prompt}]

    @abstractmethod
    def create_tab(self):
        pass

    def generate(self, prompt):
        if self.current_model == "---":
            return "hello world"
        # TODO
        else:
            return f"{self.current_model} output"

        prompt = {"role": "user", "content": prompt}
        response = requests.post(
            url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            headers=self.headers,
            json={
                "model": self.current_model,
                "messages": self.history + [prompt],
                "max_tokens": self.max_tokens,
                "seed": self.seed,
            },
        )
        if response.status_code != 200:
            pass
        response = response.json()
        self.history.append(prompt)
        self.history.append({"role": "assistant", "content": response["choices"]["message"]["content"]})

        return self.history[-1]["content"]

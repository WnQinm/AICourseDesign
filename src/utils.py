import gradio as gr
from abc import ABC, abstractmethod
import requests
from typing import List, Dict


class SelectModel:
    def __init__(self):
        self.model_list:Dict[str, str] = {
                "---": ["---"],
                "qwen": ["qwen-max", "qwen-plus", "qwen-turbo", "qwq-32b-preview"],
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
        with open("./API_KEY.txt", encoding='utf-8') as f:
            API_KEY = f.read().strip().replace('\n', '')
        self.headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        # 历史对话记录
        self.system_prompt:List[Dict[str, str]] = []
        self.history:List[Dict[str, str]] = []
        # 对话时模型可见的对话历史
        self.memory_size = 3

        self.max_tokens = 100
        self.seed = 42

        self.select_model = select_model

    @property
    def current_model_serie(self):
        return self.select_model.current_model_serie

    @property
    def current_model(self):
        return self.select_model.current_model

    @property
    def _chatbot_history(self):
        if self.memory_size <= 1:
            return self.system_prompt + [self.history[-1]]
        return self.system_prompt + self.history[-self.memory_size:]

    @property
    def all_history(self):
        return self.system_prompt + self.history

    @abstractmethod
    def create_tab(self):
        pass

    def generate(self, prompt):
        prompt = {"role": "user", "content": prompt}
        self.history.append(prompt)

        if self.current_model == "---":
            response = "hello world\n(未选择模型, 默认输出)"
        else:
            response = requests.post(
                url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
                headers=self.headers,
                json={
                    "model": self.current_model,
                    "messages": self._chatbot_history,
                    "max_tokens": self.max_tokens,
                    "seed": self.seed,
                },
            )
            status_code = response.status_code
            response = response.json()
            if status_code != 200:
                response = f"请求失败, status_code: {status_code}\n{response}\n详情见https://help.aliyun.com/zh/model-studio/developer-reference/error-code"
            else:
                response = response["choices"][0]["message"]["content"]

        self.history.append({"role": "assistant", "content": response})
        return self.history[-1]["content"]

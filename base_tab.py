import gradio as gr
from abc import ABC, abstractmethod


class BASE_TAB(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_tab(self):
        pass

    # TODO api调用

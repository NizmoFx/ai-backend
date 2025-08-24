from abc import ABC, abstractmethod
from typing import Optional, Tuple

class AIProvider(ABC):
    @abstractmethod
    def process(self, input_path: str, output_path: str,
                resize: Optional[Tuple[int,int]] = None,
                crop: Optional[Tuple[int,int,int,int]] = None,
                overlay_text: Optional[str] = None) -> str:
        ...

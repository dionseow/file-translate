import os
from typing import Protocol, Union, Callable, Any


class Processor(Protocol):
    def extract_text(
            self,
            file_path: Union[str, os.PathLike],
    ) -> str:
        ...

    def translate_in_place(
            self,
            file_path: Union[str, os.PathLike],
            new_file_path: Union[str, os.PathLike],
            translator: Callable[[str], str],
            **kwargs: Any) -> None:
        ...

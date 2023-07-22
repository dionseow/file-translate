import os
from typing import Protocol, Union, Callable



class FileTranslator(Protocol):
    def translate_in_place(
            self,
            file_path: Union[str, os.PathLike],
            new_file_path: Union[str, os.PathLike],
            translator: Callable[[str], str]) -> None:
        ...

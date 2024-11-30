import abc
from dataclasses import InitVar, dataclass
from pathlib import Path

from aoc.logger import logger


@dataclass
class InputProvider(abc.ABC):
    year: int
    day: int

    @abc.abstractmethod
    def provide_input(self, part: int | None) -> str: ...

    @property
    def _day(self) -> int:
        import __main__

        """Return the day of this challenge based on the module name."""
        if self.__module__ == "__main__":  # challenge is run directly
            return int(Path(__main__.__file__).parent.name.split("_")[1])
        return int(self.__module__.split(".")[-1].split("_")[1])


@dataclass
class SmartFileInputProvider(InputProvider):
    use_test_data: bool = False
    data_dir: InitVar[Path | None] = None

    def __post_init__(self, data_dir: Path | None):
        self._data_dir = data_dir or Path.cwd().joinpath("data")

    def provide_input(self, part: int | None) -> str:
        filename = self.get_input_filename(part)
        print("Using data from", filename)
        return self.get_input_file_path(self.get_input_filename(part)).read_text()

    def get_input_filename(self, part: int | None = None) -> str:
        """Return the input filename for this challenge."""
        base_filename = (
            f"{self.day:02}_test_input"
            if self.use_test_data
            else f"{self.day:02}_input"
        )
        default_filename = f"{base_filename}.txt"
        if part is not None:
            filename = f"{base_filename}_part_{part}.txt"
            if self._data_dir.joinpath(str(self.year), filename).exists():
                return filename
            else:
                logger.info(
                    "File %s does not exist. Using default instead %s",
                    filename,
                    default_filename,
                )
        return default_filename

    def get_input_file_path(self, filename: str) -> Path:
        """Return the input filename for this challenge."""
        return self._data_dir.joinpath(str(self.year), filename)


@dataclass
class SingleFileInputProvider(InputProvider):
    input_path: Path

    def provide_input(self, part: int | None) -> str:
        if not self.input_path.exists():
            raise FileNotFoundError(f"File {self.input_path.resolve()} does not exist.")
        print("Using data from", self.input_path.name)
        return self.input_path.read_text()

from argparse import Action
import os


class AbsolutePathAction(Action):
    @staticmethod
    def get_abs_path(file: str) -> str:
        return file if file[0] == '/' else os.path.abspath(file)

    def __call__(self, parser, namespace, values, option_string, *args, **kwargs):
        setattr(namespace, self.dest, self.get_abs_path(values))

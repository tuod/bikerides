import itertools
import shutil
import sys
from pathlib import Path

import coloredlogs
import logging
import argparse

from argparse_configs import app_config

logger = logging.getLogger(__name__)

coloredlogs.install(
    level='INFO',
    logger=logger,
    fmt="%(asctime)s - [%(levelname)s] - %(name)s - %(filename)s.%(funcName)s(%(lineno)d) - %(message)s",
)


def remove_path_prefix(fullpath, prefix):
    # Ненадежное место. Нужно заменить. Сейчас лень.
    return str(fullpath).replace(f"{prefix}/", "./")


def remove_catalogs_by_name(args, name, exclude=None, dry_run=None, verbose=None):
    project_dir = args["project_dir"]
    project_dir = Path(project_dir).expanduser().resolve()
    goals = list(project_dir.glob(f"**/{name}"))

    if exclude:
        for i, p in enumerate(exclude):
            rel_path = remove_path_prefix(p, project_dir)
            logger.info(f"Exclude path ({i+1}): {rel_path}")

    for goal in goals:
        if list(
                itertools.filterfalse(
                    lambda x: not str(goal).startswith(str(x)),
                    exclude
                )
        ):
            continue

        rel_path = remove_path_prefix(goal, project_dir)
        log_message = f"Recursively removing {rel_path}"
        if args["execute"]:
            logger.warning(log_message) if args["verbose"] else None
            shutil.rmtree(goal)
        else:
            logger.info(f"{log_message}") if args["verbose"] else None
    return goals


class Command:
    def __init__(self):
        self.removed_paths = []
        self.path_map = {
            "/clean/all": self.command_clean_all_handler,
            "/clean/tox": self.command_clean_tox_handler,
            "/clean/pycache": self.command_clean_pycache_handler,
            "/summary": self.command_summary_handler,
        }

    def execute(self, args):
        path = str(args["command"])
        application = args["app"]
        log = logger.info if args["verbose"] else logger.debug
        log(f"Run command {path}")
        try:
            command_func = self.path_map[path]
        except KeyError:
            if application.leaf:
                logger.error(f"This is a leaf command, but there is no handler for it.")
            else:
                application.parser.error(message=application.parser.format_help())
        else:
            project_dir = Path(args["project_dir"]).expanduser().resolve()
            logger.info(f"Project dir is {project_dir}")
            logger.debug(f"Args: {args}")
            command_func(args)
        log(f"Complete command {path}")

    def command_clean_all_handler(self, args):
        logger.info(f"Cleaning all...")
        self.command_clean_tox_handler(args)
        self.command_clean_pycache_handler(args)

    def command_clean_tox_handler(self, args):
        logger.info(f"Cleaning tox...")
        rm_paths = remove_catalogs_by_name(args, ".tox", exclude=self.removed_paths)
        self.removed_paths.extend(rm_paths)

    def command_clean_pycache_handler(self, args):
        logger.info(f"Cleaning pycache...")
        rm_paths = remove_catalogs_by_name(args, "__pycache__", exclude=self.removed_paths)
        self.removed_paths.extend(rm_paths)

    def command_summary_handler(self, args):
        logger.warning(f"Summary: ...")


class App:
    def __init__(self, name, args=None, commands=None, params=None, parent=None):
        self.name = name
        self.params = params
        self.commands = commands
        self.args = args if args else []
        self.parent = parent
        self.children_apps = []
        self.path = ""
        self.parser = None
        self.subparsers = None
        self.leaf = True if not commands else False

        self.register_app()
        self.register_app_args()

        if not commands:
            self.path = self._calc_path()
            logger.debug(f"There is no subcommands in command {self.name}. Command path is {self.path}.")

    def register_app(self):
        if not self.parent:
            logger.debug(f"Add new parser for {self.name} app.")
            self.parser = argparse.ArgumentParser()
        else:
            self.parser = self.parent.subparsers.add_parser(
                self.name,
                **self.params
            )
        self.parser.set_defaults(command=self._calc_path(), app=self)
        subparser_help_message = f"{self.name.capitalize()} help"

        if self.commands:
            self.subparsers = self.parser.add_subparsers(help=subparser_help_message)

        logger.debug(f"Register new app {self.name}. Parent: {self.parent.name if self.parent else '/'}.")

    def register_app_args(self):
        for arg in self.args:
            self.parser.add_argument(
                *arg["named"],
                **arg["key_value"],
            )

    def parse_args(self):
        return self.parser.parse_args()

    def _calc_path(self):
        current_app = self
        path = self.name
        while current_app.parent:
            path = f"{current_app.parent.name}/{path}"
            current_app = current_app.parent
        arr = path.split("/", 1)
        if len(arr) > 1:
            path = arr[1]
        else:
            path = ""
        path = "/" + path
        return path

    @classmethod
    def load_config(cls, input_dict, parent=None):
        application = cls(
            input_dict["name"],
            args=input_dict.get("args", []),
            commands=input_dict.get("commands", []),
            params=input_dict.get("params", {}),
            parent=parent,
        )
        for command in input_dict.get("commands", []):
            child_app = cls.load_config(command, parent=application)
            application.children_apps.append(child_app)

        return application


if __name__ == '__main__':
    app = App.load_config(app_config)
    parsed_args = app.parse_args()
    Command().execute(vars(parsed_args))

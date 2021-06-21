from pathlib import Path


class Args:
    project_dir = {
        "named": [
            "-p",
            "--dir",
            "--project-dir",
        ],
        "key_value": {
            "type": Path,
            "default": Path.cwd(),
            "dest": "project_dir",
            "help": "project root directory",
        },
    }

    execute = {
        "named": [
            "-e",
            "--exec",
            "--execute",
        ],
        "key_value": {
            "action": "store_true",
            "help": "allowing destructive actions",
            "dest": "execute",
        },
    }

    verbose = {
        "named": [
            "-v",
            "--verbose",
        ],
        "key_value": {
            "action": "store_true",
            "help": "verbose output",
            "dest": "verbose",
        },
    }


app_config = {
    "name": "commands",
    "params": {"help": "Root help"},
    "args": [
        Args.verbose,
    ],
    "commands": [
        {
            "name": "clean",
            "params": {"help": "Remove all test and build artifacts"},
            "args": [
                Args.project_dir,
                Args.execute,
            ],
            "commands": [
                {
                    "name": "all",
                    "params": {"help": "Remove all test and build artifacts"},
                },
                {
                    "name": "tox",
                    "params": {
                        "help": "Remove tox cache",
                    },
                },
                {
                    "name": "pycache",
                    "params": {
                        "help": "Remove __pycache__",
                    },
                },
            ],
        },
        {
            "name": "summary",
            "params": {
                "help": "Print summary",
            },
        },
    ],
}

import argparse
import tkinter as tk
from tkinter import scrolledtext
from pathlib import Path


VFS_NAME = "default"


class Config:
    def __init__(self, vfs_path="default.vfs", startup_script=None):
        self.vfs_path = str(vfs_path)
        self.startup_script = str(startup_script) if startup_script else ""

    def dump(self):
        return (
            f"vfs_path={self.vfs_path}",
            f"startup_script={self.startup_script}",
        )


def parse_command(line):
    """Разделяет ввод на команду и аргументы по пробелам."""
    parts = line.split()
    if not parts:
        return "", []
    return parts[0], parts[1:]


def execute_command(line, config=None):
    """Выполняет команды этапов 1-2 и возвращает текстовый результат."""
    config = config or Config()
    command, args = parse_command(line)

    if not command:
        return "error: empty command"

    if command in ("ls", "cd"):
        # На этапе 2 эти команды всё ещё являются заглушками.
        if args:
            return f"{command}: " + " ".join(args)
        return f"{command}:"

    if command == "conf-dump":
        if args:
            return "error: conf-dump does not accept arguments"
        return "\n".join(config.dump())

    if command == "exit":
        if args:
            return "error: exit does not accept arguments"
        return "__EXIT__"

    return f"error: unknown command '{command}'"


def run_startup_script(script_path, config):
    """Выполняет команды стартового скрипта последовательно.

    Ошибка отдельной команды не прерывает выполнение следующих строк.
    """
    path = Path(script_path)
    if not path.is_file():
        return [
            f"error: startup script not found: {path}",
        ]

    output = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return [f"error: cannot read startup script: {exc}"]

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        output.append(f"$ {line}")
        result = execute_command(line, config)
        output.extend(result.splitlines() or [""])

        # exit is an intentional termination command, not an error.
        if result == "__EXIT__":
            output.append("Выход из эмулятора.")
            break

    return output


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="VFS: default")
    parser.add_argument(
        "--vfs", "--vfs-path",
        dest="vfs_path",
        default="default.vfs",
        help="путь к VFS",
    )
    parser.add_argument(
        "--script", "--startup-script",
        dest="startup_script",
        default=None,
        help="путь к стартовому скрипту",
    )
    return parser.parse_args(argv)


class ShellEmulator:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.root.title(f"VFS: {VFS_NAME}")
        self.root.geometry("760x500")
        self.root.minsize(600, 400)
        self.output = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=("Menlo", 13),
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        bottom = tk.Frame(root)
        bottom.pack(fill=tk.X, padx=10, pady=(5, 10))
        self.entry = tk.Entry(bottom, font=("Menlo", 13))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.submit)
        self.entry.focus()

        button = tk.Button(bottom, text="Выполнить", command=self.submit)
        button.pack(side=tk.RIGHT, padx=(8, 0))

        self.write("UNIX-like shell emulator")
        self.write(f"VFS: {VFS_NAME}")
        self.write("Доступные команды: ls, cd, conf-dump, exit")
        self.write(f"VFS path: {self.config.vfs_path}")
        if self.config.startup_script:
            self.write(f"Startup script: {self.config.startup_script}")
            for line in run_startup_script(self.config.startup_script, self.config):
                self.write(line)
        self.write("Введите команду:")

    def write(self, text):
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def submit(self, event=None):
        line = self.entry.get()
        self.entry.delete(0, tk.END)

        self.write(f"$ {line}")
        result = execute_command(line, self.config)
        if result == "__EXIT__":
            self.write("Выход из эмулятора.")
            self.root.after(150, self.root.destroy)
            return

        for result_line in result.splitlines() or [""]:
            self.write(result_line)


def main(argv=None):
    args = parse_args(argv)
    config = Config(args.vfs_path, args.startup_script)
    root = tk.Tk()
    ShellEmulator(root, config)
    root.mainloop()


if __name__ == "__main__":
    main()

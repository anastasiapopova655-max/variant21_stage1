import tkinter as tk
from tkinter import scrolledtext


VFS_NAME = "default"


def parse_command(line):
    """Разделяет ввод на команду и аргументы по пробелам."""
    parts = line.split()
    if not parts:
        return "", []
    return parts[0], parts[1:]


def execute_command(line):
    """Выполняет команды этапа 1 и возвращает текстовый результат."""
    command, args = parse_command(line)

    if not command:
        return "error: empty command"

    if command in ("ls", "cd"):
        if args:
            return f"{command}: " + " ".join(args)
        return f"{command}:"

    if command == "exit":
        return "__EXIT__"

    return f"error: unknown command '{command}'"


class ShellEmulator:
    def __init__(self, root):
        self.root = root
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
        self.write("Доступные команды: ls, cd, exit")
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
        result = execute_command(line)

        if result == "__EXIT__":
            self.write("Выход из эмулятора.")
            self.root.after(150, self.root.destroy)
            return

        self.write(result)


def main():
    root = tk.Tk()
    ShellEmulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()

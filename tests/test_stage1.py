import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import execute_command, parse_command


def test_parser():
    assert parse_command("ls file.txt") == ("ls", ["file.txt"])
    assert parse_command("cd folder one") == ("cd", ["folder", "one"])


def test_ls_and_cd_stubs():
    assert execute_command("ls") == "ls:"
    assert execute_command("ls folder") == "ls: folder"
    assert execute_command("cd home") == "cd: home"


def test_exit():
    assert execute_command("exit") == "__EXIT__"


def test_errors():
    assert execute_command("") == "error: empty command"
    assert execute_command("unknown test") == "error: unknown command 'unknown'"

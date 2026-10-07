import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import Config, execute_command, parse_args, run_startup_script


def test_cli_arguments():
    args = parse_args(["--vfs", "disk.vfs", "--script", "startup.txt"])
    assert args.vfs_path == "disk.vfs"
    assert args.startup_script == "startup.txt"


def test_cli_argument_aliases():
    args = parse_args(["--vfs-path", "disk.vfs", "--startup-script", "startup.txt"])
    assert args.vfs_path == "disk.vfs"
    assert args.startup_script == "startup.txt"


def test_conf_dump():
    config = Config("disk.vfs", "startup.txt")
    assert execute_command("conf-dump", config) == (
        "vfs_path=disk.vfs\nstartup_script=startup.txt"
    )


def test_conf_dump_rejects_arguments():
    config = Config("disk.vfs")
    assert execute_command("conf-dump extra", config) == (
        "error: conf-dump does not accept arguments"
    )


def test_startup_script_continues_after_error(tmp_path):
    script = tmp_path / "startup.txt"
    script.write_text("ls\nunknown\nconf-dump\ncd home\n", encoding="utf-8")
    output = run_startup_script(script, Config("disk.vfs", str(script)))
    assert "$ ls" in output
    assert "error: unknown command 'unknown'" in output
    assert "$ conf-dump" in output
    assert "vfs_path=disk.vfs" in output
    assert "$ cd home" in output


def test_missing_startup_script():
    output = run_startup_script("does-not-exist.txt", Config())
    assert output == ["error: startup script not found: does-not-exist.txt"]

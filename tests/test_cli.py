import pytest

from click.testing import CliRunner
from pathlib import Path

from edges_cal.cli import compare, report, run


def test_run(data_path: Path, tmpdir: Path):
    runner = CliRunner()
    outdir = tmpdir / "cli-out"
    if not outdir.exists():
        outdir.mkdir()
    result = runner.invoke(
        run,
        [
            str(data_path / "settings.yaml"),
            str(data_path / "Receiver01_25C_2019_11_26_040_to_200MHz"),
            "--out",
            str(outdir),
            "--cache-dir",
            str(outdir),
            "--plot",
            "--simulators",
            "AntSim2",
        ],
    )

    assert result.exit_code == 0


def test_report(data_path: Path, tmpdir: Path):
    runner = CliRunner()
    outdir = tmpdir / "cli-out"
    if not outdir.exists():
        outdir.mkdir()

    result = runner.invoke(
        report,
        [
            str(data_path / "Receiver01_25C_2019_11_26_040_to_200MHz"),
            "--config",
            str(data_path / "settings.yaml"),
            "--out",
            str(outdir),
            "--cache-dir",
            str(outdir),
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 0


def test_compare(data_path: Path, tmpdir: Path):
    runner = CliRunner()
    outdir = tmpdir / "cli-out"
    if not outdir.exists():
        outdir.mkdir()

    result = runner.invoke(
        compare,
        [
            str(data_path / "Receiver01_25C_2019_11_26_040_to_200MHz"),
            str(data_path / "Receiver01_25C_2019_11_26_040_to_200MHz"),
            "--config",
            str(data_path / "settings.yaml"),
            "--config-cmp",
            str(data_path / "settings.yaml"),
            "--out",
            str(outdir),
            "--cache-dir",
            str(outdir),
        ],
        catch_exceptions=False,
    )

    if result.exit_code:
        print(result.output)

    assert result.exit_code == 0

import logging
import os
import platform
import sys
import warnings

try:
    # Python 3.8+
    from importlib import metadata as importlib_metadata
except Exception:  # pragma: no cover
    import importlib_metadata  # type: ignore


def _safe_get_version(package_name: str) -> str:
    try:
        return importlib_metadata.version(package_name)
    except Exception:
        return "unknown"


def _log_package_versions() -> None:
    packages_to_check = [
        "pyexiv2",
        "exiftool",
        "pywin32",
        "PySide6",
        "PyQt6",
        "PyQt5",
        "PyInstaller",
    ]
    for pkg in packages_to_check:
        logging.info(f"Package {pkg} version: {_safe_get_version(pkg)}")


def _patch_input_to_log() -> None:
    import builtins  # local import to avoid early binding in some packagers

    original_input = builtins.input

    def logged_input(prompt: str = "") -> str:  # type: ignore[override]
        try:
            logging.warning(f"input() called with prompt: {prompt!r}")
        except Exception:
            # Best-effort; never block the prompt
            pass
        return original_input(prompt)

    builtins.input = logged_input  # type: ignore[assignment]


def _patch_tk_messagebox_logging() -> None:
    try:
        from tkinter import messagebox

        def _wrap(fn_name: str):
            fn = getattr(messagebox, fn_name, None)
            if not callable(fn):
                return

            def wrapper(*args, **kwargs):
                try:
                    logging.warning(
                        f"tkinter.messagebox.{fn_name} called with args={args!r} kwargs={kwargs!r}"
                    )
                except Exception:
                    pass
                return fn(*args, **kwargs)

            setattr(messagebox, fn_name, wrapper)

        for name in [
            "showinfo",
            "showwarning",
            "showerror",
            "askquestion",
            "askokcancel",
            "askyesno",
            "askretrycancel",
        ]:
            _wrap(name)
    except Exception:
        # GUI may not be available; ignore
        pass





def install_diagnostics_logging() -> None:
    """Install environment diagnostics and prompt logging.

    - Logs OS, Python, and key package versions
    - Captures calls to builtins.input (often used by license prompts)
    - Wraps tkinter.messagebox functions to log prompts
    - Captures warnings into logs
    """
    # If logging not configured elsewhere, set a sensible default
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler("app.log")],
        )

    logging.info("Installing diagnostics logging")
    logging.info(f"Platform: {platform.platform()}")
    logging.info(f"Python: {sys.version}")
    logging.info(f"CWD: {os.getcwd()}")

    _log_package_versions()
    _patch_input_to_log()
    _patch_tk_messagebox_logging()

    # Route warnings to logging
    logging.captureWarnings(True)
    warnings.filterwarnings("default")



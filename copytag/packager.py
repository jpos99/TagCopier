import PyInstaller.__main__
import os
import logging

# Configuração do logger para salvar logs em um arquivo e também exibi-los no console
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("packager.log"),
                        logging.StreamHandler()
                    ])

def create_executable():
    try:
        logging.info("Starting the packaging process")

        PyInstaller.__main__.run([
            'frontend.py',
            '--name=TagCopier',
            '--onefile',
            '--windowed',
            '--icon=app_icon.ico',
            '--add-data=requirements.txt;.',
            '--hidden-import=win32api',
            '--hidden-import=win32security',
            '--hidden-import=pyexiv2',
        ])

        logging.info("Packaging process completed successfully")

    except Exception as e:
        logging.error(f"An error occurred during the packaging process: {e}")


if __name__ == '__main__':
    create_executable()

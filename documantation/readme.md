
# Tag Copier

Tag Copier is a program designed to help users manage tags from source files and replicate them to corresponding destination files. This program is composed of a frontend interface built using PySimpleGUI and backend operations supported by the Python standard library and third-party modules like pyexiv2.

## Features:

1. **Source and Destination Directory Selection**: Allows users to select a source directory and a destination directory.
2. **CSV Generation**: Provides an option to generate a CSV file containing information about the source file, its tag, and the corresponding destination file.
3. **Tag Copying**: Enables users to copy tags from the generated CSV to the destination files.
4. **Tabular Display**: Displays the CSV data in a tabular format within the GUI.

## Usage:

To get started, run the `frontend.py` to launch the GUI:

```bash
python frontend.py
```

Once the application is active:

1. Browse and select your desired source directory.
2. Browse and select your desired destination directory.
3. Click on 'Generate CSV' to assemble the CSV file.
4. Click on 'Copy tags' to propagate the tags to the destination files.
5. View the contents of the CSV directly within the GUI.

## Dependencies:

- **PySimpleGUI**: Offers the user-friendly interface.
- **pyexiv2**: Essential for reading and modifying image metadata.
- **Python's CSV module**: Facilitates CSV file generation and reading.
- **OS module**: Handles various filesystem operations.

Ensure these are installed to ensure the smooth running of the application.

## Core Files:

- **frontend.py**: Hosts the graphical user interface and main application logic.
- **backend.py**: Responsible for generating the CSV file and copying tags from the CSV to the destination files.
- **service.py**: Encompasses several utility functions pivotal to the application's operation.

## Future Enhancements:

- Robust error-handling capabilities.
- Incorporation of a progress bar for long-running tasks.
- Enablement of batch processing for large-scale operations.
- Provision of diverse tag operations (e.g., delete, update).

## Contributing:

Your contributions are always welcome! Should you find any issues or have suggestions for improvements, feel free to raise them or submit pull requests to enhance the application.


# Towel Dependency Installer

The **Towel Dependency Installer** is a Python GUI application designed to quickly install or uninstall all the dependencies required for Towel Apps. It provides an easy-to-use interface for managing the necessary Python packages, ensuring that you have all the required components to run Towel applications smoothly.

## Features

- **Easy Installation and Uninstallation**: Install or uninstall all necessary dependencies with just a few clicks.
- **Package Selection**: Select or unselect individual packages as needed.
- **(Un)Select All Button**: Quickly select or unselect all packages.
- **Pip Version Selection**: Choose between `pip` and `pip3` based on your Python environment.
- **Real-Time Terminal Output**: Monitor the installation or uninstallation progress directly within the app.
- **Stop Operation**: Cancel ongoing operations at any time with the **Stop** button.

## Managed Dependencies

The Towel Dependency Installer manages the following Python packages:

- `pynput`
- `setuptools`
- `Flask`
- `pefile`
- `lief`
- `capstone`
- `keystone-engine`
- `pygame`
- `scipy`
- `numpy`
- `pydub`
- `pdfplumber`
- `transformers`
- `tqdm`
- `moviepy`
- `imageio`

## Requirements

- **Python 3.x**
- **Tkinter Library** (usually included with Python installations)
- **pip** or **pip3** installed and available in your system's PATH

## Installation

1. **Download the Script**

   Download the `tdi.py` script from the repository or source where it's provided.

2. **Run the Script**

   Open a terminal or command prompt, navigate to the directory containing the script, and run:

   ```bash
   python tdi.py
   ```

   Or, if using Python 3:

   ```bash
   python3 tdi.py
   ```

## Usage

1. **Select Packages**

   - All packages are selected by default.
   - Use the checkboxes to select or unselect individual packages.
   - Click the **(Un)Select All** button to toggle the selection of all packages.

2. **Choose Pip Version**

   - Select either **pip** or **pip3** depending on your Python environment.

3. **Install or Uninstall Packages**

   - Click the **Install** button to install the selected packages.
   - Click the **Uninstall** button to remove the selected packages.

4. **Monitor Progress**

   - The terminal output area displays real-time progress and messages from the `pip` commands.
   - Scroll through the output to monitor the installation or uninstallation process.

5. **Stop an Ongoing Operation**

   - Click the **Stop** button to cancel the ongoing installation or uninstallation.
   - This will terminate the current `pip` process.

## Screenshots

*(Screenshots can be added here to illustrate the application's interface and features.)*

## Notes

- **Permissions**: Ensure you have the necessary permissions to install or uninstall packages on your system.
- **Process Termination**: Using the **Stop** button may leave packages in an inconsistent state. Use it only when necessary.
- **Platform Compatibility**: The application handles process termination differently on Windows and Unix-like systems due to system limitations.

## Troubleshooting

- **pip Not Found**: If the application cannot find `pip` or `pip3`, ensure they are installed and added to your system's PATH.
- **Permission Errors**: Run the application with administrator or root privileges if you encounter permission issues.
- **Failed Installations**: The terminal output area will display any errors during the installation or uninstallation process.

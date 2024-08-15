# ZeeWoo
**ZeeWoo: Privacy services with AI-based file deletion and Artifact removal solutions**

**지우개: AI 기반 파일 삭제 및 Artifact 제거 솔루션을 통한 개인정보 보호 서비스**

# 🧹 ZeeWoo Eraser Software (Beta)

🚧 **Currently in Beta**: ZeeWoo Eraser is in its testing phase with basic file deletion functionality. Future updates will bring more features and improvements! Stay tuned for enhanced capabilities.


# 🧹 ZeeWoo Eraser Software

ZeeWoo is a powerful file deletion tool designed to securely delete office document files (Excel, PPT, Hangul HWP, Word) along with **Windows artifacts (MFT, INDX, $UsnJournal, $LogFile, $Recycle.Bin, LNK files)** associated with them. This tool is designed to work on Windows 11 environments.

## 📋 Features

1. **File Deletion**: Completely deletes the selected office and other files.
2. **Artifact Removal**: Safely removes system artifacts related to the deleted files, such as MFT, $I30, $UsnJournal, $LogFile, $Recycle.Bin, and LNK files.
3. **Logging**: Keeps a log of deleted files and artifacts in `logs/deletion_log.txt`.
4. **$UsnJournal Exception**: Optionally, you can keep $UsnJournal for forensic purposes or decide not to delete it.

## 🚀 Key Artifact Details

- **MFT**: Master File Table in NTFS that stores metadata for files and directories.
- **INDX ($I30)**: Artifact that stores directory file listings in NTFS.
- **$UsnJournal**: Journal that logs changes to the file system, essential for forensic analysis.
- **$LogFile**: NTFS transaction log file that tracks changes to the file system.
- **$Recycle.Bin**: Directory where deleted files are stored temporarily in the Recycle Bin.
- **LNK files**: Shortcut files that retain metadata about deleted files.

## 🛠️ How to Use

1. **File Selection**: Click the "Browse" button in the program to select the file you want to delete.
2. **File Deletion**: Once the file path is displayed, click the "Delete" button to delete the file and its related artifacts.
3. **Confirmation**: A success message will appear upon completion, and the action will be logged in the `logs/deletion_log.txt` file.

### 💻 Code Structure

- **`main.py`**: Handles the GUI and provides file selection and deletion functionalities.
- **`file_manager.py`**: Manages the deletion of files and artifacts.
- **`artifact_parser.py`**: Identifies and finds the related Windows artifacts for a given file.
- **`utils.py`**: Utility functions for checking file extensions and fetching the user’s SID.

## 📂 Key Files

```
📦 core
 ┣ 📜 artifact_parser.py  # Artifact parsing class
 ┣ 📜 file_manager.py     # File and artifact deletion manager
 ┣ 📜 utils.py            # Utility function collection
 ┗ 📜 main.py             # Main GUI application


📦 Installation & Execution

Clone the Repository
git clone https://github.com/Gyuwon-Yonsei-CPSS/ZeeWoo.git

Install Dependencies
pip install -r requirements.txt

Run the Program
python main.py
or
dist/지우개.exe
```

## ⚠️ Notes
If you wish to preserve the $UsnJournal, you can modify the logic in artifact_parser.py to exclude the $UsnJournal from deletion.
Be aware that once files and artifacts are deleted, they may not be recoverable.


## 📧 Contact
For any questions or bug reports, feel free to reach out via email.

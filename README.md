# 🚀 **ZeeWoo Software**

ZeeWoo is an advanced eraser software that supports various file formats and specializes in detecting and securely deleting sensitive data. It ensures that deleted files cannot be recovered, providing a strong solution for managing sensitive information on your computer.

---

## ✨ **Key Features**

- **💼 Secure File Deletion**  
  - Completely deletes files in a way that makes them unrecoverable, protecting sensitive information.

- **🔍 YOLO-based Image Detection**  
  - Utilizes the latest YOLO model to detect sensitive information in images and prompt the user to confirm whether or not to delete them.

- **⏰ Automatic Scheduling**  
  - Provides an automatic file deletion feature. Users can set a schedule (daily, weekly, monthly) to have files deleted automatically at their chosen intervals.

- **📂 Supports Multiple File Formats**  
  - Detects and deletes various file types, including PDFs, images (JPEG, PNG), and documents (Word, Excel, etc.).

- **🎨 Intuitive User Interface**  
  - A user-friendly UI that makes it easy for anyone to use, allowing users to review and delete detected files with ease.

---

## 🛠 **How to Use**

1. **Detect and Delete Files**  
   - Select the file path, and ZeeWoo Software will detect files and prompt the user for deletion. Once deleted, the files cannot be recovered.

2. **Set Up Scheduling**  
   - Set up a schedule for regular file deletion. Choose the date, time, and frequency of deletion, and ZeeWoo will handle the rest.

3. **Review Detected Files**  
   - The detected files are displayed on the screen, allowing the user to confirm the deletion.

---

## 💼 **Use Cases**

- **Data Privacy Protection**: Safely delete files containing sensitive customer or personal data to prevent information leakage.
- **File Cleanup**: Regularly clean up unnecessary files to optimize storage space.
- **Security Enhancement**: Ensure deleted files cannot be recovered, reducing security risks.

---

## 🛠 **Installation & Execution**

### 1. **Clone the repository**
```
git clone https://github.com/Gyuwon-Yonsei-CPSS/ZeeWoo.git
```

2. Install necessary packages
```
pip install -r requirements.txt
```

3. Run the application
```
python main.py
or
zeewoo.exe
```

📂 Project Structure
```
ZeeWoo/
│
├── data/                # Data-related files
├── ui/                  # UI resources
├── yolov8/              # YOLOv8 model and related code
├── main.py              # Main execution file
└── README.md            # Project documentation
```

📝 Notes
ZeeWoo is a critical solution for sensitive data protection, and users can automate file management using its scheduling feature.
Further updates regarding image detection and data models are planned.


🔗 Key Files
yolov8.pt: Pre-trained YOLOv8 model file
schedule.py: Code for the automatic file deletion scheduling feature
ui/: User interface components and design files

# Python 3.12 Installation and Usage Guide

## Installation Status ✅

Python 3.12.10 has been successfully installed on your Windows system.

**Location:** `C:\Users\raycs\AppData\Local\Programs\Python\Python312\`

## How to Use Python 3.12

### Method 1: Full Path (Recommended)
```powershell
& "C:\Users\raycs\AppData\Local\Programs\Python\Python312\python.exe" --version
& "C:\Users\raycs\AppData\Local\Programs\Python\Python312\python.exe" your_script.py
```

### Method 2: Virtual Environment (Best Practice)
```powershell
# Activate virtual environment
venv312\Scripts\activate.bat

# Now you can use python directly
python --version
python your_script.py

# Deactivate when done
deactivate
```

### Method 3: Add to PATH (Optional)
If you want to use `python` command directly, you can add Python 3.12 to your PATH:

1. Open System Properties → Advanced → Environment Variables
2. Edit the PATH variable
3. Add: `C:\Users\raycs\AppData\Local\Programs\Python\Python312\`
4. Add: `C:\Users\raycs\AppData\Local\Programs\Python\Python312\Scripts\`

## Package Installation

### Using Full Path
```powershell
& "C:\Users\raycs\AppData\Local\Programs\Python\Python312\python.exe" -m pip install package_name
```

### Using Virtual Environment
```powershell
venv312\Scripts\activate.bat
pip install package_name
```

## Known Issues and Solutions

### Issue: chroma-hnswlib Build Error
**Error:** `Microsoft Visual C++ 14.0 or greater is required`

**Solution:** 
1. Visual Studio Build Tools have been installed
2. For now, you can install packages individually:
   ```powershell
   & "C:\Users\raycs\AppData\Local\Programs\Python\Python312\python.exe" -m pip install streamlit langchain-openai
   ```

### Issue: Python not found in PATH
**Solution:** Use the full path or virtual environment method above.

## Testing Your Installation

Run the test script:
```powershell
& "C:\Users\raycs\AppData\Local\Programs\Python\Python312\python.exe" test_python.py
```

## Next Steps

1. **Set up virtual environment** (recommended):
   ```powershell
   .\setup_env.bat
   ```

2. **Install project dependencies**:
   ```powershell
   venv312\Scripts\activate.bat
   pip install -r requirements_minimal.txt
   ```

3. **Test the brand identity workflow**:
   ```powershell
   python app.py
   ```

## Troubleshooting

- If you get permission errors, run PowerShell as Administrator
- If packages fail to install, try using the virtual environment
- For chromadb issues, consider using alternative vector databases or wait for pre-compiled wheels

## Python 3.12 Features

Python 3.12 includes:
- Improved error messages
- Better performance
- Enhanced type system
- New syntax features
- Better compatibility with modern packages 
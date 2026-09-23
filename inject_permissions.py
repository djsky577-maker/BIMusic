import re

file_path = 'android/app/src/main/AndroidManifest.xml'

try:
    with open(file_path, 'r') as f:
        content = f.read()

    # Check if permissions are already there
    if 'FOREGROUND_SERVICE' in content:
        print("✅ Permissions already exist!")
    else:
        # Find the <application tag and insert permissions right before it
        permissions = """    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />
    
    <application"""
        
        content = content.replace('<application', permissions, 1)
        
        with open(file_path, 'w') as f:
            f.write(content)
        print("✅ Permissions injected successfully!")
except Exception as e:
    print(f"❌ Error: {e}")

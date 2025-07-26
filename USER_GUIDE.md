# MSG to EML Converter - User Guide

## For Your Dad 👨‍💻

This is a simple app to convert MSG email files to EML format, so they can be opened in any email program like Mail, Outlook, or Thunderbird.

### How to Use the App

1. **Open the App**: Double-click on "MSG to EML Converter.app"

2. **Convert a Single File**:

   - Click "Browse" next to "MSG File" and select your .msg file
   - Click "Browse" next to "Output EML" to choose where to save the converted file
   - Click "Convert File"

3. **Convert Multiple Files (Batch)**:

   - Click "Browse" next to "Input Folder" and select the folder containing your .msg files
   - Click "Browse" next to "Output Folder" to choose where to save all converted files
   - **Check "Search subfolders recursively"** if you want to find MSG files in subfolders too
   - Click "Convert All Files"

4. **Watch the Progress**: The app will show you what it's doing in the status area at the bottom

### What You Get

- Each .msg file becomes a .eml file
- The .eml files can be opened in any email program
- All email content, attachments, and information is preserved
- **Non-MSG files are ignored** (you'll see a warning about how many were skipped)
- **Subdirectories are searched** when recursive mode is enabled

### If Something Goes Wrong

- Make sure the .msg files aren't corrupted
- Check that you have permission to write to the output folder
- The status area will show any error messages
- **Don't worry about warnings** - they just tell you about non-MSG files that were ignored

### Example

If you have:

```
Downloads/
  email1.msg
  email2.msg
  Old_Emails/
    important.msg
    archive.msg
  Documents/
    report.pdf (ignored)
    meeting.msg
```

After conversion with recursive mode enabled you'll have:

```
Downloads_EML/
  email1.eml
  email2.eml
  Old_Emails/
    important.eml
    archive.eml
  Documents/
    meeting.eml
```

**Note**: The report.pdf file was ignored (you'll see "⚠️ 1 non-MSG files ignored" in the status)

---

**Technical Note**: This entire app was created by AI (GitHub Copilot) to help convert MSG files to the more universal EML format.

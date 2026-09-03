# MSG to EML Converter - User Guide

*Created by Carlo*

## Getting Started

This application converts Microsoft Outlook MSG email files to the standard EML format, making them compatible with any email program like Mail, Outlook, or Thunderbird.

### Usage Instructions

1. **Launch the Application**: Start the MSG to EML Converter application

2. **Single File Conversion**:

   - Click "Browse" next to "MSG File" and select your .msg file
   - Click "Browse" next to "Output EML" to choose where to save the converted file
   - Click "Convert File"

3. **Batch Conversion**:

   - Click "Browse" next to "Input Folder" and select the folder containing your .msg files
   - Click "Browse" next to "Output Folder" to choose where to save all converted files
   - **Check "Search subfolders recursively"** if you want to include MSG files in subfolders
   - Click "Convert All Files"

4. **Monitor Progress**: The application displays conversion status in the status area

### Conversion Results

- Each .msg file is converted to a .eml file
- .eml files are compatible with all standard email programs
- All email content, attachments, and metadata are preserved
- **Non-MSG files are automatically ignored** (the application will report how many were skipped)
- **Subdirectories are processed** when recursive mode is enabled

### Troubleshooting

- Ensure .msg files are not corrupted or password-protected
- Verify you have write permissions to the output folder
- Check the status area for detailed error messages
- **Warnings about ignored files are normal** - they indicate non-MSG files that were skipped

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

**Note**: The report.pdf file was ignored (the application reports "⚠️ 1 non-MSG files ignored" in the status)

---

**About**: This application provides a reliable solution for converting Microsoft Outlook MSG files to the universal EML email format.

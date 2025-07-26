#!/bin/bash
# Package the MSG to EML Converter for delivery

echo "📦 Packaging MSG to EML Converter for your dad..."

# Create a delivery folder
mkdir -p "MSG_to_EML_for_Dad"

# Copy the app
cp -r "dist/MSG to EML Converter.app" "MSG_to_EML_for_Dad/"

# Copy the user guide
cp "USER_GUIDE.md" "MSG_to_EML_for_Dad/"

# Create a simple README for the package
cat > "MSG_to_EML_for_Dad/README.txt" << 'EOF'
MSG to EML Converter
===================

Hi! This app converts MSG email files to EML format.

To use:
1. Double-click "MSG to EML Converter.app"
2. Follow the simple interface
3. Read "USER_GUIDE.md" for detailed instructions

The app was completely created by AI to help you convert old MSG files!

Enjoy!
EOF

echo "✅ Package ready in: MSG_to_EML_for_Dad/"
echo "📱 App: MSG_to_EML_for_Dad/MSG to EML Converter.app"
echo "📖 Guide: MSG_to_EML_for_Dad/USER_GUIDE.md"
echo ""
echo "🎁 Ready to share with your dad!"
echo "   You can zip this folder and send it to him."

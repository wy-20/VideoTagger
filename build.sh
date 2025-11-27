#!/bin/bash
# build.sh - Video Tagger packaging script for Ubuntu 20.04

set -e

APP_NAME="video-tagger"
VERSION="1.0.0"
OUTPUT_DIR="dist"

echo "=== Video Tagger Packaging Script ==="
echo "Version: $VERSION"
echo "Target platform: Ubuntu 20.04"
echo ""

# Check virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Please activate the virtual environment first"
    echo "   source venv/bin/activate"
    exit 1
fi

# Install/update packaging tools
echo "📦 Installing packaging dependencies..."
pip install --upgrade pyinstaller

# Clean old build files
echo "🧹 Cleaning old builds..."
[ -d build ] && rm -rf build/
[ -d dist ] && rm -rf dist/

# Execute packaging using spec file
echo "🔨 Starting packaging..."
pyinstaller video_tagger.spec --clean

# Create release package
echo "📁 Creating release package..."
RELEASE_DIR="$OUTPUT_DIR/${APP_NAME}-${VERSION}-ubuntu20.04"
mkdir -p "$RELEASE_DIR"

# Copy executable
cp "$OUTPUT_DIR/$APP_NAME" "$RELEASE_DIR/"

# Create launcher script
cat > "$RELEASE_DIR/run.sh" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec "$SCRIPT_DIR/video-tagger" "$@"
EOF
chmod +x "$RELEASE_DIR/run.sh"

# Create README
cat > "$RELEASE_DIR/README.txt" << EOF
Video Tagger v$VERSION
========================

Run:
  ./video-tagger

Or via the launcher script:
  ./run.sh

System requirements:
  - Ubuntu 20.04 or later
  - GStreamer plugins (for video playback)

If video playback fails, install:
  sudo apt install gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \\
      gstreamer1.0-plugins-ugly gstreamer1.0-libav
EOF

# Compress release package
echo "📦 Compressing release package..."
cd "$OUTPUT_DIR"
tar -czvf "${APP_NAME}-${VERSION}-ubuntu20.04.tar.gz" "${APP_NAME}-${VERSION}-ubuntu20.04"

echo ""
echo "✅ Packaging complete!"
echo "📍 Output location: $OUTPUT_DIR/${APP_NAME}-${VERSION}-ubuntu20.04.tar.gz"
echo "📏 File size: $(du -h "${APP_NAME}-${VERSION}-ubuntu20.04.tar.gz" | cut -f1)"

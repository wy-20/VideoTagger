#!/bin/bash
# Build script for VideoTagger AppImage
# This script creates an AppImage for Ubuntu 22.04 x64
#
# Usage: ./build_appimage.sh
#
# Requirements:
#   - Ubuntu 22.04 x64 (or compatible)
#   - Python 3.10+
#   - pip
#   - wget or curl
#   - fuse (for running AppImage)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
BUILD_DIR="${PROJECT_ROOT}/build"
APPDIR="${BUILD_DIR}/AppDir"
APP_NAME="VideoTagger"
APP_VERSION="${APP_VERSION:-1.0.0}"

echo "========================================"
echo "Building ${APP_NAME} AppImage v${APP_VERSION}"
echo "========================================"

# Create build directory
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"
cd "${BUILD_DIR}"

echo ""
echo "Step 1: Setting up Python virtual environment..."
echo "----------------------------------------"
python3 -m venv venv
source venv/bin/activate

echo ""
echo "Step 2: Installing Python dependencies..."
echo "----------------------------------------"
pip install --upgrade pip
pip install -r "${PROJECT_ROOT}/requirements.txt"
pip install pyinstaller

echo ""
echo "Step 3: Building with PyInstaller..."
echo "----------------------------------------"
cd "${PROJECT_ROOT}"
pyinstaller --clean --noconfirm "${SCRIPT_DIR}/VideoTagger.spec"

echo ""
echo "Step 4: Creating AppDir structure..."
echo "----------------------------------------"
mkdir -p "${APPDIR}/usr/bin"
mkdir -p "${APPDIR}/usr/lib"
mkdir -p "${APPDIR}/usr/share/applications"
mkdir -p "${APPDIR}/usr/share/icons/hicolor/scalable/apps"
mkdir -p "${APPDIR}/usr/share/icons/hicolor/256x256/apps"
mkdir -p "${APPDIR}/usr/share/metainfo"

# Copy PyInstaller output
cp -r "${PROJECT_ROOT}/dist/VideoTagger/"* "${APPDIR}/usr/bin/"

# Copy desktop file
cp "${SCRIPT_DIR}/VideoTagger.desktop" "${APPDIR}/"
cp "${SCRIPT_DIR}/VideoTagger.desktop" "${APPDIR}/usr/share/applications/"

# Copy icon
cp "${SCRIPT_DIR}/VideoTagger.svg" "${APPDIR}/VideoTagger.svg"
cp "${SCRIPT_DIR}/VideoTagger.svg" "${APPDIR}/usr/share/icons/hicolor/scalable/apps/"
cp "${SCRIPT_DIR}/VideoTagger.svg" "${APPDIR}/.DirIcon"

# Create PNG icon from SVG (if rsvg-convert is available)
if command -v rsvg-convert &> /dev/null; then
    rsvg-convert -w 256 -h 256 "${SCRIPT_DIR}/VideoTagger.svg" > "${APPDIR}/usr/share/icons/hicolor/256x256/apps/VideoTagger.png"
fi

# Copy AppRun script
cp "${SCRIPT_DIR}/AppRun" "${APPDIR}/"
chmod +x "${APPDIR}/AppRun"

echo ""
echo "Step 5: Bundling GStreamer plugins..."
echo "----------------------------------------"
# Bundle GStreamer plugins for video playback
GSTREAMER_DIR="/usr/lib/x86_64-linux-gnu/gstreamer-1.0"
if [ -d "$GSTREAMER_DIR" ]; then
    mkdir -p "${APPDIR}/usr/lib/x86_64-linux-gnu/gstreamer-1.0"
    
    # Copy essential GStreamer plugins for video playback
    GSTREAMER_PLUGINS=(
        "libgstcoreelements.so"
        "libgstplayback.so"
        "libgstvideoconvertscale.so"
        "libgstautodetect.so"
        "libgstvideoparsersbad.so"
        "libgstlibav.so"
        "libgstmatroska.so"
        "libgstisomp4.so"
        "libgstavi.so"
        "libgstaudioparsers.so"
        "libgstaudioconvert.so"
        "libgstaudioresample.so"
        "libgstvolume.so"
        "libgstalsa.so"
        "libgstpulseaudio.so"
        "libgstvideorate.so"
        "libgstdeinterlace.so"
        "libgstx264.so"
        "libgstvpx.so"
        "libgstflv.so"
        "libgstasf.so"
    )
    
    for plugin in "${GSTREAMER_PLUGINS[@]}"; do
        if [ -f "${GSTREAMER_DIR}/${plugin}" ]; then
            cp "${GSTREAMER_DIR}/${plugin}" "${APPDIR}/usr/lib/x86_64-linux-gnu/gstreamer-1.0/"
        fi
    done
    
    # Copy GStreamer plugin scanner
    if [ -f "/usr/libexec/gstreamer-1.0/gst-plugin-scanner" ]; then
        mkdir -p "${APPDIR}/usr/libexec/gstreamer-1.0"
        cp "/usr/libexec/gstreamer-1.0/gst-plugin-scanner" "${APPDIR}/usr/libexec/gstreamer-1.0/"
    fi
fi

echo ""
echo "Step 6: Downloading appimagetool..."
echo "----------------------------------------"
cd "${BUILD_DIR}"
APPIMAGETOOL="appimagetool-x86_64.AppImage"
if [ ! -f "$APPIMAGETOOL" ]; then
    if ! wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/${APPIMAGETOOL}"; then
        echo "Error: Failed to download appimagetool"
        exit 1
    fi
    chmod +x "$APPIMAGETOOL"
fi

echo ""
echo "Step 7: Creating AppImage..."
echo "----------------------------------------"
ARCH=x86_64 "./${APPIMAGETOOL}" "${APPDIR}" "${APP_NAME}-${APP_VERSION}-x86_64.AppImage"

# Deactivate virtual environment
deactivate

echo ""
echo "========================================"
echo "Build complete!"
echo "AppImage: ${BUILD_DIR}/${APP_NAME}-${APP_VERSION}-x86_64.AppImage"
echo "========================================"

# Make the AppImage executable
chmod +x "${BUILD_DIR}/${APP_NAME}-${APP_VERSION}-x86_64.AppImage"

echo ""
echo "To run the AppImage:"
echo "  ${BUILD_DIR}/${APP_NAME}-${APP_VERSION}-x86_64.AppImage"

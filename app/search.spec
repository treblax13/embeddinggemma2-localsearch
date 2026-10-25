# -*- mode: python ; coding: utf-8 -*-
# Packages search.py as a double-clickable app, bundling Python, torch and the other
# dependencies so the target machine needs nothing pre-installed. The model weights
# are NOT bundled (same ~1.4GB first-run download as running from source) — only the
# Python runtime and libraries are.
#
# Build:  pyinstaller search.spec --noconfirm
# Output: dist/EmbeddingGemma2LocalSearch.app (macOS) or dist/EmbeddingGemma2LocalSearch/ (Windows/Linux)

import sys

from PyInstaller.utils.hooks import collect_all

datas = [("web", "web")]
binaries = []
hiddenimports = []

# collect_all (not just the hooks-contrib entries for torch/transformers) because
# sentence-transformers and pymupdf dynamically pull in submodules/data files that
# plain import analysis won't see.
for pkg in ("torch", "torchvision", "transformers", "sentence_transformers", "pymupdf", "pillow_heif"):
    d, b, h = collect_all(pkg)
    datas += d
    binaries += b
    hiddenimports += h

a = Analysis(
    ["search.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="EmbeddingGemma2LocalSearch",
    debug=False,
    strip=False,
    upx=False,  # UPX compression is a known source of crashes with torch's binaries
    console=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="EmbeddingGemma2LocalSearch",
)

# BUNDLE makes a double-clickable .app and only means anything on macOS; on
# Windows/Linux the COLLECT folder above (dist/EmbeddingGemma2LocalSearch/) is the
# deliverable as-is, with the executable at its root.
if sys.platform == "darwin":
    BUNDLE(
        coll,
        name="EmbeddingGemma2LocalSearch.app",
        icon=None,
        bundle_identifier="com.treblax13.embeddinggemma2localsearch",
        info_plist={"NSHighResolutionCapable": "True"},
    )

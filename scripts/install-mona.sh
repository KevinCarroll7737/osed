#!/bin/bash                                                                                                                                                 
set -euo pipefail

# --- config ---
TOOLS=(
  "https://github.com/corelan/windbglib/raw/master/pykd/pykd.zip"
  "https://github.com/corelan/windbglib/raw/master/windbglib.py"
  "https://github.com/corelan/mona/raw/master/mona.py"
  "https://www.python.org/ftp/python/2.7.17/python-2.7.17.msi"
  "https://download.microsoft.com/download/2/E/6/2E61CFA4-993B-4DD4-91DA-3737CD5CD6E3/vcredist_x86.exe"
  "https://raw.githubusercontent.com/epi052/osed-scripts/main/install-mona.ps1"
)

SHARE_TMP="mona-share"    # name that will appear on the remote for the temp tools
SHARE_LOCAL="local-share" # name that will appear on the remote for your current dir

# --- prepare ---
ORIG_PWD="$(pwd)"
TMPDIR="$(mktemp -d)"
trap 'rc=$?; rm -rf "$TMPDIR"; exit $rc' EXIT

echo "[+] Temp dir: $TMPDIR"
echo "[+] Downloading tools into the temp dir..."

# Download into the temp directory
pushd "$TMPDIR" >/dev/null
for url in "${TOOLS[@]}"; do
    echo "[=] downloading: $url"
    wget -q --show-progress "$url"
done

# try to unzip pykd if present (ignore errors)
if [ -f pykd.zip ]; then
    echo "[=] extracting pykd.zip"
    unzip -qqo pykd.zip || true
fi
popd >/dev/null

# Inform the user how to run the installer from the remote side
echo
echo "[+] Once the RDP window opens, run this in an Administrator PowerShell on the remote:"
echo
echo "powershell -c \"Get-Content \\\\$${SHARE_TMP}\\\\install-mona.ps1 | powershell -\""
echo

# --- connect, share BOTH folders ---
# Note: we pass two -r disk options: one for the temp tools and one for your current working dir
rdesktop "${1}" -u offsec -p lab \
    -r "disk:${SHARE_TMP}=${TMPDIR}" \
    -r "disk:${SHARE_LOCAL}=${ORIG_PWD}"

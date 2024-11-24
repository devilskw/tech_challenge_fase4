@echo off
if %1 == -u (
  echo "Uninstalling %2...."
  echo .
  ".venv/Scripts/pip.exe" uninstall %2
  echo .
) ELSE (
  echo "Installing %1...."
  echo .
  ".venv/Scripts/pip.exe" install %1
  echo .
)
cd ..
exit 0
#!/bin/bash

set -e

cd ~/Documents/aggregator

VENV_PY="/Users/xrlmop/Documents/aggregator/venv/bin/python"

if [ ! -x "$VENV_PY" ]; then
    echo "❌ venv-python не найден: $VENV_PY"
    exit 1
fi

"$VENV_PY" -c "import PyInstaller" 2>/dev/null \
    || "$VENV_PY" -m pip install pyinstaller

# Чистим прошлое
rm -rf build dist KAI_Root.spec KAI_Aggregator.spec

echo "🏗  ROOT..."
"$VENV_PY" -m PyInstaller \
    --windowed \
    --noconfirm \
    --name="KAI_Root" \
    --paths=. \
    --collect-all PyQt6 \
    --collect-all cryptography \
    --add-data="core:core" \
    --add-data="ui_root:ui_root" \
    --hidden-import=core.crypto \
    --hidden-import=core.admin \
    --hidden-import=core.license \
    --hidden-import=core.machine \
    --hidden-import=ui_root.root_window \
    --hidden-import=ui_root.root_theme \
    root_admin.py

echo ""
echo "🏗  STUDENT..."
"$VENV_PY" -m PyInstaller \
    --windowed \
    --noconfirm \
    --name="KAI_Aggregator" \
    --paths=. \
    --collect-all PyQt6 \
    --collect-all cryptography \
    --collect-all openai \
    --add-data="core:core" \
    --add-data="ui:ui" \
    --add-data="data:data" \
    --hidden-import=core.crypto \
    --hidden-import=core.admin \
    --hidden-import=core.license \
    --hidden-import=core.machine \
    --hidden-import=ui.main_window \
    --hidden-import=ui.license_view \
    --hidden-import=ui.deepseek_view \
    --hidden-import=ui.notes_view \
    --hidden-import=ui.c_editor \
    --hidden-import=ui.meet_view \
    --hidden-import=ui.left_panel \
    --hidden-import=ui.right_panel \
    --hidden-import=ui.cards \
    --hidden-import=ui.theme \
    --hidden-import=ui.icons \
    --hidden-import=data.fake_data \
    main.py

# Снимаем карантин с обоих
xattr -cr dist/KAI_Root.app 2>/dev/null || true
xattr -cr dist/KAI_Aggregator.app 2>/dev/null || true

echo ""
echo "🎉 Готово"
ls -la dist/
echo ""
echo "Запускай:"
echo "    open dist/KAI_Root.app"
echo "    open dist/KAI_Aggregator.app"

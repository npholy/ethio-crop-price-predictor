@echo off
echo ============================================
echo  EthioPrice - Structure Verification
echo ============================================
echo.

echo Checking required files and folders...
echo.

echo [CHECKING] api/app.py
if exist "api\app.py" (
    echo   ✅ Found
) else (
    echo   ❌ MISSING
)

echo [CHECKING] api/requirements.txt
if exist "api\requirements.txt" (
    echo   ✅ Found
) else (
    echo   ❌ MISSING
)

echo [CHECKING] api/Procfile
if exist "api\Procfile" (
    echo   ✅ Found
) else (
    echo   ❌ MISSING
)

echo [CHECKING] api/runtime.txt
if exist "api\runtime.txt" (
    echo   ✅ Found
) else (
    echo   ❌ MISSING
)

echo.
echo [CHECKING] api/models/ folder
if exist "api\models\" (
    echo   ✅ Folder exists
    echo   [CHECKING] Model files...
    if exist "api\models\crop_price_model.pkl" (
        echo     ✅ crop_price_model.pkl
    ) else (
        echo     ❌ crop_price_model.pkl MISSING
    )
    if exist "api\models\le_commodity.pkl" (
        echo     ✅ le_commodity.pkl
    ) else (
        echo     ❌ le_commodity.pkl MISSING
    )
    if exist "api\models\le_admin.pkl" (
        echo     ✅ le_admin.pkl
    ) else (
        echo     ❌ le_admin.pkl MISSING
    )
    if exist "api\models\le_season.pkl" (
        echo     ✅ le_season.pkl
    ) else (
        echo     ❌ le_season.pkl MISSING
    )
) else (
    echo   ❌ FOLDER MISSING - Need to move models/ into api/
)

echo.
echo [CHECKING] api/data/ folder
if exist "api\data\raw\" (
    echo   ✅ Folder exists
    if exist "api\data\raw\wfp_food_prices_eth.csv" (
        echo     ✅ wfp_food_prices_eth.csv
    ) else (
        echo     ❌ wfp_food_prices_eth.csv MISSING
    )
) else (
    echo   ❌ FOLDER MISSING - Need to move data/ into api/
    echo.
    echo   REQUIRED ACTION:
    echo   1. Copy data folder into api:
    echo      xcopy data api\data\ /E /I /Y
    echo   2. Or move it:
    echo      move data api\data
)

echo.
echo ============================================
echo  Structure Check Complete
echo ============================================
echo.

echo Next steps:
echo 1. Fix any MISSING items above
echo 2. Run: git status
echo 3. Commit and push changes
echo 4. Deploy to Render
echo.

pause

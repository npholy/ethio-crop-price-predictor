@echo off
echo ============================================
echo  EthioPrice - Deploy CORS and 404 Fix
echo ============================================
echo.

echo Step 1: Checking git status...
git status
echo.

echo Step 2: Adding modified files...
git add api\app.py
git add test_endpoints.py
git add CORS_FIX_GUIDE.md
git add deploy_fix.bat
echo ✅ Files staged
echo.

echo Step 3: Committing changes...
git commit -m "Fix: Resolve CORS and 404 errors - update Flask endpoints and CORS config"
echo ✅ Changes committed
echo.

echo Step 4: Pushing to GitHub...
git push origin master
echo ✅ Pushed to GitHub
echo.

echo ============================================
echo  🎉 Deployment Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Wait 2-3 minutes for Render to auto-deploy
echo 2. Check Render Dashboard for deployment status
echo 3. Test your endpoints with: python test_endpoints.py
echo.
echo Your API should now be live at:
echo https://ethio-crop-price-predictor-api.onrender.com
echo.

pause

================================================================================
CONNECTING VERCEL FRONTEND TO LOCAL BACKEND - COMPLETE GUIDE
================================================================================

Your frontend is now deployed on Vercel, and you want to connect it to your
local backend running on your machine. This guide explains 3 methods.

================================================================================
1. FIND YOUR LOCAL MACHINE'S IP ADDRESS
================================================================================

WINDOWS:
--------
1. Open Command Prompt (cmd)
2. Type: ipconfig
3. Look for "IPv4 Address" under your network adapter
   Example: 192.168.1.100 or 192.168.0.50

Mac/Linux:
----------
1. Open Terminal
2. Type: ifconfig or hostname -I
3. Look for "inet" address starting with 192.168 or 10.0

================================================================================
2. THREE METHODS TO CONNECT VERCEL TO LOCAL BACKEND
================================================================================

⭐ METHOD 1: NGROK TUNNEL (RECOMMENDED - EASIEST & SAFEST)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHY NGROK?
✓ Secure tunnel from internet to your local machine
✓ No port forwarding needed
✓ Works even behind firewalls and NAT
✓ HTTPS encrypted
✓ Free tier available

SETUP NGROK:
1. Download: https://ngrok.com/download
2. Sign up for free account: https://ngrok.com
3. Get your auth token: https://dashboard.ngrok.com/auth
4. Install ngrok (unzip and add to PATH)
5. Set auth token:
   ngrok config add-authtoken YOUR_AUTH_TOKEN

EXPOSE YOUR BACKEND:
1. Open Terminal/PowerShell in your RAGnosis folder
2. Start ngrok tunnel:
   ngrok http 5000
3. You'll see:
   Forwarding https://1234-567-890.ngrok.io -> http://localhost:5000
4. Copy this URL: https://1234-567-890.ngrok.io

SET VERCEL ENVIRONMENT VARIABLE:
1. Go to Vercel Dashboard → Your Project → Settings
2. Click "Environment Variables"
3. Add new variable:
   Name: VITE_API_BASE_URL
   Value: https://1234-567-890.ngrok.io (from ngrok)
   Environments: Production (select if deploying production)
4. Click Save
5. Redeploy your frontend (Vercel will rebuild)

Now your Vercel frontend can access your local backend via ngrok! ✅

⚠️  NOTE: Every time you restart ngrok, you'll get a new URL
    (unless you have ngrok Pro). Update Vercel env variable with new URL.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
METHOD 2: LOCAL IP ADDRESS + PORT FORWARDING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHY LOCAL IP?
✓ Direct connection (no intermediary)
✓ No additional tools needed
✗ Requires port forwarding on your router
✗ Less secure (backend exposed to internet)
✗ Only works if you have static/public IP

SETUP:
1. Get your local IP: (see section 1 above)
   Example: 192.168.1.100

2. Forward port 5000 on your router:
   - Log in to your router admin panel (usually 192.168.1.1)
   - Find "Port Forwarding" settings
   - Create rule: External Port 5000 → Internal IP 192.168.1.100:5000
   - Save and apply

3. Get your PUBLIC IP:
   - Go to: https://whatismyipaddress.com/
   - Copy the IPv4 address (your public IP)
   - Example: 203.45.67.89

4. Update Vercel Environment Variable:
   Name: VITE_API_BASE_URL
   Value: http://203.45.67.89:5000

5. Redeploy on Vercel

⚠️  WARNING: This exposes your backend to the internet!
    Make sure your backend has proper authentication/security.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
METHOD 3: CLOUDFLARE TUNNEL (ALTERNATIVE TO NGROK)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHY CLOUDFLARE?
✓ Free (even better than ngrok free tier)
✓ Global CDN included
✓ Very fast and reliable
✓ Same tunnel URL always (no regeneration like ngrok)

SETUP:
1. Install Cloudflare Tunnel:
   npm install -g @cloudflare/wrangler
   # or download from: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/tunnel-guide/remote/

2. Authenticate:
   wrangler login
   (Opens browser to authenticate)

3. Create tunnel:
   wrangler tunnel create ragnosis
   (Saves your tunnel credentials)

4. Run tunnel:
   wrangler tunnel run ragnosis --url http://localhost:5000
   
   You'll see:
   Tunnel running at https://ragnosis.YOUR_USERNAME.workers.dev

5. Update Vercel Environment Variable:
   Name: VITE_API_BASE_URL
   Value: https://ragnosis.YOUR_USERNAME.workers.dev

✅ Same URL every time! Much easier than ngrok.


================================================================================
3. VERCEL DEPLOYMENT CHECKLIST
================================================================================

After setting up your tunnel/forwarding:

☐ 1. Verify backend is running locally:
     Windows: cd backend && python app.py
     Or: py app.py
     Look for: "Running on http://127.0.0.1:5000"

☐ 2. Verify tunnel/port forwarding is active:
     ngrok: "Forwarding https://xxx.ngrok.io -> http://localhost:5000"
     or
     Cloudflare: "Tunnel running at https://ragnosis..."

☐ 3. Test backend directly:
     Open in browser: https://xxx.ngrok.io/api/health
     or: http://YOUR_PUBLIC_IP:5000/api/health
     Should see: {"status": "ok"}

☐ 4. Add environment variable to Vercel:
     Settings → Environment Variables
     VITE_API_BASE_URL = https://xxx.ngrok.io (or your URL)

☐ 5. Redeploy frontend on Vercel:
     Push to GitHub or manually redeploy in Vercel dashboard
     (Settings → Deployments → Redeploy)

☐ 6. Check browser console:
     Go to your Vercel app
     Open DevTools (F12) → Console
     Look for: "🔗 API Base URL: https://xxx.ngrok.io"
     No CORS errors = ✅ Success!

☐ 7. Test a feature:
     - Try logging in
     - Upload a report
     - Check Network tab in DevTools
     Should see requests going to your tunnel URL


================================================================================
4. ENVIRONMENT CONFIGURATION
================================================================================

LOCAL DEVELOPMENT (.env.local):
────────────────────────────────
VITE_API_BASE_URL=http://localhost:5000
(Used when you run: npm run dev locally)


PRODUCTION/VERCEL (.env.production):
───────────────────────────────────
VITE_API_BASE_URL=https://xxx.ngrok.io
or
VITE_API_BASE_URL=http://YOUR_PUBLIC_IP:5000
(Set in Vercel Dashboard → Environment Variables)


BACKEND CONFIGURATION (.env or backend/.env):
──────────────────────────────────────────────
VERCEL_FRONTEND_URL=https://your-app.vercel.app
ALLOW_ALL_ORIGINS=false  (false = secure, true = dev only)

OR for local development:

ALLOW_ALL_ORIGINS=true
(Allows requests from any origin during development)


================================================================================
5. TROUBLESHOOTING
================================================================================

Problem: "CORS error: blocked by CORS policy"
Solution:
  1. Check backend is running
  2. Check tunnel/port forwarding is active
  3. Verify VITE_API_BASE_URL is correct in Vercel
  4. Check browser console for actual URL being called
  5. Make sure backend CORS allows Vercel domain
     → Set VERCEL_FRONTEND_URL in backend/.env

Problem: "Cannot GET /api/reports" (404 error)
Solution:
  - Verify backend has routes registered
  - Check if routes/reports.py exists
  - Test with: https://xxx.ngrok.io/api/health

Problem: "Connection refused"
Solution:
  - Is backend running? (python app.py)
  - Is ngrok tunnel running?
  - Check firewall isn't blocking port 5000
  - Try: ngrok http 5000 with verbose flag

Problem: "Request timeout"
Solution:
  - Backend might be slow (BART model loading?)
  - Check backend logs for errors
  - Increase timeout in vite.config.js:
    proxyTimeout: 180000 (3 minutes)
  - Or: Check if MongoDB connection is failing

Problem: "ngrok URL keeps changing"
Solution:
  - Upgrade to ngrok Pro ($5/month) for permanent URL
  - Or use Cloudflare Tunnel (permanently same URL, free)


================================================================================
6. SECURITY BEST PRACTICES
================================================================================

✓ Always use HTTPS (ngrok/Cloudflare provide this)
✓ Never expose MongoDB URI in frontend code
✓ Keep JWT_SECRET in backend .env file only
✓ Use environment variables for sensitive data
✓ Enable CORS only for trusted domains
✓ Don't set ALLOW_ALL_ORIGINS=true in production
✓ Use ngrok auth token (prevents others from hijacking)
✓ Rotate JWT_SECRET periodically
✓ Monitor backend logs for suspicious requests


================================================================================
7. QUICK START (NGROK METHOD - FASTEST)
================================================================================

1. Install ngrok: https://ngrok.com/download
2. Authenticate: ngrok config add-authtoken YOUR_TOKEN
3. Start backend: python backend/app.py
4. Expose backend: ngrok http 5000
5. Copy ngrok URL (https://xxx.ngrok.io)
6. Add to Vercel → Settings → Environment Variables:
   VITE_API_BASE_URL=https://xxx.ngrok.io
7. Redeploy on Vercel
8. Test! 🎉


================================================================================
NEXT STEPS
================================================================================

1. Choose your method (ngrok recommended)
2. Set up tunnel/forwarding
3. Add VITE_API_BASE_URL to Vercel environment variables
4. Redeploy frontend
5. Test by logging in or uploading a report
6. Check browser console (F12) for any errors

If you need help, check the browser's Network tab in DevTools:
- See actual API requests
- Check for CORS errors
- Verify response status codes

Good luck! 🚀

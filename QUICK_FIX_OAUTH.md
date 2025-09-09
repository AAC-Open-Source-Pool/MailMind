# 🚨 Quick Fix for OAuth Redirect URI Mismatch

## **The Problem:**
You're getting `Error 400: redirect_uri_mismatch` when trying to authenticate with Google.

## **The Solution:**

### **Step 1: Update Google Cloud Console**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services** → **Credentials**
3. Click on your **OAuth 2.0 Client ID**
4. In the **Authorized redirect URIs** section, add:
   ```
   http://localhost:8090/
   http://localhost:8091/
   http://localhost:8092/
   http://localhost:8093/
   http://localhost:8094/
   http://localhost:8095/
   http://localhost:8096/
   http://localhost:8097/
   http://localhost:8098/
   http://localhost:8099/
   ```
5. Click **Save**

### **Step 2: Wait 5 Minutes**
Google Cloud Console changes take a few minutes to propagate.

### **Step 3: Try Again**
```bash
python main.py
```

## **What I Fixed:**
- Updated the code to use port 8080 instead of automatic port selection
- This ensures the redirect URI matches what's configured in Google Cloud Console

## **If Still Having Issues:**

### **Alternative Redirect URIs to Add:**
```
http://localhost:8080/
http://localhost:8090/
http://localhost:0/
http://127.0.0.1:8080/
```

### **Check Your Setup:**
1. ✅ Firebase configured
2. ✅ Google APIs enabled (Gmail, Calendar)
3. ✅ OAuth 2.0 Client ID created
4. ✅ credentials.json in project root
5. 🔧 **Add redirect URI in Google Cloud Console**

## **Expected Result:**
After fixing the redirect URI, you should see:
```
🔐 Authenticating with Google APIs...
✅ Google APIs authenticated successfully
📧 Fetching unread emails...
```

The OAuth flow will open a browser window for you to authorize the application, and then it will work perfectly!

## **Need Help?**
- Check that your Google Cloud project is correct
- Verify the credentials.json file is from the right project
- Make sure Gmail and Calendar APIs are enabled
- Wait 5-10 minutes after making changes in Google Cloud Console

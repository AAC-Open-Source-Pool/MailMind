# Fixing OAuth Redirect URI Mismatch Error

## 🚨 **Error: redirect_uri_mismatch**

This error occurs when the redirect URI configured in Google Cloud Console doesn't match what the application is using.

## 🔧 **Solution Steps:**

### **Step 1: Check Current OAuth Configuration**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to your project
3. Go to **APIs & Services** → **Credentials**
4. Find your OAuth 2.0 Client ID
5. Click on it to edit

### **Step 2: Update Redirect URIs**

In the OAuth 2.0 Client ID settings, add these redirect URIs:

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
http://127.0.0.1:8090/
http://127.0.0.1:8091/
http://127.0.0.1:8092/
http://127.0.0.1:8093/
http://127.0.0.1:8094/
http://127.0.0.1:8095/
http://127.0.0.1:8096/
http://127.0.0.1:8097/
http://127.0.0.1:8098/
http://127.0.0.1:8099/
```

**Important:** The `http://localhost:0/` is used by the Google OAuth library when it automatically finds an available port.

### **Step 3: Alternative - Use Specific Port**

If you want to use a specific port, modify the OAuth flow in your code:

```python
# In enhanced_email_processor.py, modify the authenticate_google_apis method:

flow = InstalledAppFlow.from_client_secrets_file(
    self.config.CREDENTIALS_FILE, 
    self.config.GMAIL_SCOPES
)
# Use a specific port instead of port=0
creds = flow.run_local_server(port=8080)
```

Then add `http://localhost:8080/` to your redirect URIs in Google Cloud Console.

### **Step 4: Verify Application Type**

Make sure your OAuth 2.0 Client ID is configured as:
- **Application type:** Desktop application
- **Name:** Your application name

### **Step 5: Test the Fix**

After updating the redirect URIs:

1. Wait 5-10 minutes for changes to propagate
2. Try running the application again:
   ```bash
   python main.py
   ```

## 🔍 **Troubleshooting:**

### **If the error persists:**

1. **Clear cached tokens:**
   ```bash
   # Delete any existing token files
   rm -f token.json
   ```

2. **Check credentials.json:**
   - Ensure it's the correct file from Google Cloud Console
   - Verify it's in the project root directory

3. **Verify scopes:**
   - Make sure Gmail and Calendar APIs are enabled
   - Check that the scopes in your code match the enabled APIs

### **Common Redirect URIs for Desktop Apps:**

```
http://localhost:8080/
http://localhost:8090/
http://localhost:0/
http://127.0.0.1:8080/
http://127.0.0.1:8090/
http://127.0.0.1:0/
```

## 🎯 **Quick Fix:**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. **APIs & Services** → **Credentials**
3. Edit your OAuth 2.0 Client ID
4. Add these redirect URIs:
   ```
   http://localhost:8080/
   http://localhost:8090/
   http://localhost:0/
   ```
5. Save changes
6. Wait 5 minutes
7. Try again

## 📞 **If Still Having Issues:**

1. Check the exact error message in the browser
2. Verify your Google Cloud project is correct
3. Ensure you're using the right credentials.json file
4. Make sure the Gmail and Calendar APIs are enabled

The redirect URI mismatch is a configuration issue, not a code issue. Once you update the redirect URIs in Google Cloud Console, it should work perfectly!

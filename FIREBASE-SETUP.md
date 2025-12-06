# Firebase Setup Guide for Community Captioner

This guide will help you set up Firebase Realtime Database for multi-user caption syncing.

## Why Firebase?

Firebase allows multiple users to have their own caption channels that work from anywhere:
- User A gets: `overlay.html?channel=abc123`
- User B gets: `overlay.html?channel=xyz789`
- Each channel syncs independently
- Works with static hosting (Netlify, GitHub Pages, etc.)
- Free tier is generous (100 simultaneous connections, 10GB/month)

---

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Create a project"** (or "Add project")
3. Name it something like `community-captioner`
4. Disable Google Analytics (not needed) and click **Create Project**
5. Wait for setup to complete, then click **Continue**

---

## Step 2: Create a Realtime Database

1. In the left sidebar, click **Build** → **Realtime Database**
2. Click **Create Database**
3. Choose a location (pick one close to your users)
4. Select **Start in test mode** (we'll secure it later)
5. Click **Enable**

---

## Step 3: Get Your Firebase Config

1. Click the **gear icon** (⚙️) next to "Project Overview" → **Project settings**
2. Scroll down to **"Your apps"** section
3. Click the **</>** (Web) icon to add a web app
4. Name it `captioner-web` and click **Register app**
5. You'll see a config object like this:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyC.....................",
  authDomain: "your-project.firebaseapp.com",
  databaseURL: "https://your-project-default-rtdb.firebaseio.com",
  projectId: "your-project",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abcdef123456"
};
```

6. **Copy these values** - you'll need them in the next step

---

## Step 4: Add Config to Your Files

Open `index.html` and find this section near the top of the `<script>` tag:

```javascript
// FIREBASE CONFIG - Replace with your values from Firebase Console
const FIREBASE_CONFIG = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_PROJECT.firebaseapp.com",
    databaseURL: "https://YOUR_PROJECT-default-rtdb.firebaseio.com",
    projectId: "YOUR_PROJECT",
    storageBucket: "YOUR_PROJECT.appspot.com",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};
```

Replace the placeholder values with your actual Firebase config.

Do the same in `overlay.html`.

---

## Step 5: Set Database Security Rules

1. In Firebase Console, go to **Realtime Database** → **Rules** tab
2. Replace the rules with:

```json
{
  "rules": {
    "channels": {
      "$channelId": {
        // Anyone can read (needed for OBS overlay)
        ".read": true,
        // Anyone can write (for simplicity - see below for stricter rules)
        ".write": true,
        // Auto-delete old data after 24 hours (optional)
        ".indexOn": ["updatedAt"]
      }
    }
  }
}
```

3. Click **Publish**

### Optional: Stricter Rules

For production, you might want rate limiting or authentication. Here's a stricter version:

```json
{
  "rules": {
    "channels": {
      "$channelId": {
        ".read": true,
        ".write": "newData.child('updatedAt').val() === now",
        ".validate": "newData.hasChildren(['caption', 'updatedAt'])"
      }
    }
  }
}
```

---

## Step 6: Test It!

1. Open your `index.html` in a browser (via local server or Netlify)
2. You should see a **Channel ID** displayed (e.g., `abc123`)
3. Start captioning and speak
4. Open the overlay URL in another tab/browser:
   - `https://your-site.netlify.app/overlay.html?channel=abc123`
5. Captions should appear in real-time!

---

## Hosting on Netlify

1. Push your files to GitHub
2. Connect the repo to Netlify
3. Deploy!

Your URLs will be:
- Control Panel: `https://your-site.netlify.app/`
- Overlay: `https://your-site.netlify.app/overlay.html?channel=CHANNEL_ID`

---

## Troubleshooting

### "Firebase is not defined"
- Check that the Firebase SDK scripts are loading
- Make sure you're not blocking third-party scripts

### "Permission denied" errors
- Check your database rules in Firebase Console
- Make sure you're in "test mode" or have proper rules set

### Captions not syncing
- Check browser console for errors
- Verify your `databaseURL` is correct (must include `https://`)
- Make sure both control panel and overlay have the same Firebase config

### Channel not found
- The channel ID must match exactly (case-sensitive)
- Check that the control panel is actually writing to Firebase

---

## Cost & Limits

Firebase Spark (Free) plan includes:
- **1 GB** stored data
- **10 GB/month** downloaded
- **100** simultaneous connections

This is plenty for most community media use. If you exceed limits, Firebase will pause your database until the next billing period.

---

## Need Help?

- [Firebase Documentation](https://firebase.google.com/docs/database)
- [Community Captioner GitHub](https://github.com/amateurmenace/community-captioner)

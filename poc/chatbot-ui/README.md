
# Control vs. Speed to start. 

Option 1: React UI from scratch
Option 2: Use OpenWebUI 


# Option 1: React UI from scratch

## How to build this UI 

### Method 1 - Shortcut using a codespaces react instance 

#### Step 1: start a new codespace using the Github react template 

#### Step 2:  Install lucide-react

 npm install lucide-react

#### Step 3: Replace the App.jsx file 

#### Step 4: Run 

npm start 
---



### Method 2 Long way using a bare instance 

#### Step 1: check npm and node are installed 

``` npm -v 
node -v
```

#### Step 2: Set Up the React Project
Since `create-react-app` is deprecated, we used **Vite** for better performance.  
1. **Create a new React project with Vite:**  
   ```bash
   npm create vite@latest chatbot-ui --template react
   ```
   - Selected **React** as the framework.  
   - Chose **JavaScript** instead of TypeScript (since you’re a beginner).  

2. **Go into the project directory:**  
   ```bash
   cd chatbot-ui
   ```

3. **Install dependencies:**  
   ```bash
   npm install
   ```

---

#### Step 3: Install Tailwind CSS  
To style the chatbot, we set up Tailwind CSS:  

1. **Install Tailwind and its dependencies:**  
   ```bash
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```
2. **Configure `tailwind.config.js`:**  
   - Added the correct content paths:  
     ```js
     export default {
       content: [
         "./index.html",
         "./src/**/*.{js,ts,jsx,tsx}",
       ],
       theme: { extend: {} },
       plugins: [],
     };
     ```
3. **Add Tailwind to `index.css`:**  
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

---

#### Step 4: Start the Project  
1. **Run the development server:**  
   ```bash
   npm run dev
   ```
2. **Opened the preview link in the browser.**  
   - **Issue:** The default Vite page was showing instead of the chatbot.  

---

#### Step 5: Fix Vite Showing Default Page
1. **Checked `src/main.jsx`** – It was correct, rendering `<App />`.  
2. **Checked `src/App.jsx`** – It was using the default Vite page.  
3. **Replaced `App.jsx` with chatbot UI code.**  
4. **Restarted the server:**  
   ```bash
   npm run dev
   ```

---

#### Step 6: Fixed Missing Dependencies & Errors
### **Issue 1: `lucide-react` Not Found**  
- Error:  
  ```
  Failed to resolve import "lucide-react" from "src/App.jsx".
  ```
- **Fix:** Installed `lucide-react`:  
  ```bash
  npm install lucide-react
  ```
- Restarted the app.

### **Issue 2: `Input is not defined` Error**  
- React does **not** have a built-in `Input` component.  
- **Fix:** Replaced it with a regular `<input>` HTML tag.

### **Issue 3: Left Panel Was Not Dedicated**  
- The left panel (past chats) was merging with the main UI.  
- **Fix:** Applied a dedicated **fixed-width layout** for the sidebar.

---

#### Step 7: UI Improvements
1. **Added a Left Panel for Past Chats** – Empty for now.  
2. **Divided the Right Panel:**  
   - **Top:** Chat history.  
   - **Bottom:** User input section with a text box and a `+` button for uploads.  
3. **Fixed UI Layout Issues** to ensure:
   - Chat messages are properly aligned.
   - The input section is always at the bottom.
   - The left panel stays fixed.

---

#### Step 8: Running the Chatbot UI
After all the fixes, **started the chatbot UI successfully:**
```bash
npm run dev
```
**🎉 Done! The chatbot UI is now fully functional.**  

---

## Host the website on S3 

### **🚀 Steps to Deploy Your Chatbot UI on AWS S3**  
Now that your **chatbot UI files are still present**, follow these steps to **deploy it to AWS S3** as a static website.

---

## **✅ Step 1: Build the React App**  
Since Vite is being used, we need to generate a production-ready **build folder**.

Run:
```bash
npm run build
```
This will create a `dist/` folder containing the **optimized static files** (HTML, JS, CSS).

---

## **✅ Step 2: Create an S3 Bucket**  
1. **Go to AWS Console → S3**  
2. Click **"Create bucket"**  
3. **Set Bucket Name** (e.g., `my-chatbot-app`)  
4. **Disable "Block all public access"**  
   - Uncheck **“Block all public access”** (since we are hosting a website).  
   - Confirm in the warning prompt.  
5. Click **"Create bucket"**

---

## **✅ Step 3: Upload the Build Files to S3**
Now, upload the `dist/` folder to the S3 bucket.

### **Option 1: Upload via AWS CLI** (Recommended)
1. **Ensure you have AWS CLI installed**  
   - Check by running:  
     ```bash
     aws --version
     ```
   - If not installed, follow: [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).

2. **Configure AWS CLI (If Not Set Up)**
   ```bash
   aws configure
   ```
   - Enter your **AWS Access Key, Secret Key, Region**, and **output format**.

3. **Sync the `dist/` folder to S3**
   ```bash
   aws s3 sync dist/ s3://my-chatbot-app --delete
   ```

### **Option 2: Upload Manually via AWS Console**
1. Open your **S3 bucket** in the AWS Console.  
2. Click **"Upload" → "Add Files/Folders"**  
3. **Select all files from the `dist/` folder**  
4. Click **Upload**

---

## **✅ Step 4: Enable Static Website Hosting**
1. Open **S3 Console → Your Bucket**  
2. Go to **Properties → Static website hosting**  
3. Enable it and set:
   - **Index document**: `index.html`
4. Save the changes.

---

## **✅ Step 5: Make the Website Public**
1. Go to the **Permissions tab** of your S3 bucket.  
2. Scroll down to **Bucket Policy** and add this policy:  

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-chatbot-app/*"
    }
  ]
}
```
- **Replace `my-chatbot-app`** with your actual bucket name.
- Click **Save**.

---

## **✅ Step 6: Access Your Chatbot UI**
- Go to **Properties → Static Website Hosting**  
- **Copy the Website URL** (something like `http://my-chatbot-app.s3-website-us-east-1.amazonaws.com/`)  
- Open it in your browser! 🎉🚀

---

### **✅ Bonus: Use CloudFront for HTTPS (Optional)**
S3 static websites **do not support HTTPS by default**.  
To enable **HTTPS**, set up **AWS CloudFront** (a CDN).  
Would you like instructions for that? 😊
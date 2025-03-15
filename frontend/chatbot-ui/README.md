# How to Install this UI 

## Method 1 - Shortcut using a codespaces react instance 

### Step1-: start a new codespace using the Github react template 

### Install lucide-react

 npm install lucide-react

### Run 

npm start 
---


## Method -2 Long way using a bare instance 
### Step 1: check npm and node are installed 

``` npm -v 
node -v
```

### **✅ Step 2: Set Up the React Project**  
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

### **✅ Step 3: Install Tailwind CSS**  
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

### **✅ Step 4: Start the Project**  
1. **Run the development server:**  
   ```bash
   npm run dev
   ```
2. **Opened the preview link in the browser.**  
   - **Issue:** The default Vite page was showing instead of the chatbot.  

---

### **✅ Step 5: Fix Vite Showing Default Page**  
1. **Checked `src/main.jsx`** – It was correct, rendering `<App />`.  
2. **Checked `src/App.jsx`** – It was using the default Vite page.  
3. **Replaced `App.jsx` with chatbot UI code.**  
4. **Restarted the server:**  
   ```bash
   npm run dev
   ```

---

### **✅ Step 6: Fixed Missing Dependencies & Errors**  
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

### **✅ Step 7: UI Improvements**  
1. **Added a Left Panel for Past Chats** – Empty for now.  
2. **Divided the Right Panel:**  
   - **Top:** Chat history.  
   - **Bottom:** User input section with a text box and a `+` button for uploads.  
3. **Fixed UI Layout Issues** to ensure:
   - Chat messages are properly aligned.
   - The input section is always at the bottom.
   - The left panel stays fixed.

---

### **✅ Final Step: Running the Chatbot UI**
After all the fixes, **started the chatbot UI successfully:**
```bash
npm run dev
```
**🎉 Done! The chatbot UI is now fully functional.**  

---


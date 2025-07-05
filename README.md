# 🚀 SocialNetwork

A lightweight social network built with **Django** and **Bootstrap 5**.

---

## 📣 The Project

- 📝 **User Authentication**  
  - Sign up, log in, log out  
  - Secure “next” redirect handling  
- 👤 **Profile**  
  - One-to-one extended profile (avatar, bio, location, birth date, status)  
  - Follow / unfollow other users  
- 📰 **Feed & Posts**  
  - Create text + image posts  
  - Inline comments on feed  
  - Detailed post view with threaded comments  
  - “Like” (❤️) toggle on any post  
- 📂 **Organization**  
  - Clean URL design (`/feed/`, `/profile/<username>/`, `/post/<id>/`)  
  - DRY, function-based views  
- 🎨 **Styling**  
  - Powered by Bootstrap 5 for responsive UI  
  - Custom cards, buttons, and forms  

---

## 📦 Installation

```bash
# 1. Clone repo
git clone https://github.com/DataSpieler12345/socialnetwork.git
cd socialnetwork

# 2. Create & activate virtualenv
python3 -m venv env
source env/bin/activate        # Linux / macOS
# env\Scripts\activate         # Windows PowerShell

# 3. Install dependencies
pip install -r requirements.txt

# 4. Database migrations
python manage.py migrate

# 5. Run the dev server
python manage.py runserver

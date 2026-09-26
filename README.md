# 📱 Telegram Direct Uploader

> Android phone ko server bana kar Telegram channel me files upload karo — bina bot, bina third-party server ke!

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🏠 Self-hosted | Phone hi server, koi external server nahi |
| 🔐 No Bot | Direct Telegram account se upload |
| 📁 Folder Upload | Ek folder ki sabhi files auto upload |
| ⏸️ Resume Support | Network error par wait karke resume hoga |
| 📦 2 GB Support | Bot API limit (50 MB) nahi, pure 2 GB |
| 💾 Progress Save | Beech me roko, baad me wahi se continue |

---

## 📥 Installation

### Step 1: Termux Install

- F-Droid se Termux download karo
- Settings → Apps → Termux → Permissions → Storage ON karo

### Step 2: Setup Commands

```bash
pkg update
pkg upgrade -y
pkg install python python-pip termux-api -y
pip install telethon
termux-setup-storage

Ye multiline caamand me hi fas ja rha

Theek hai, multiline command Termux me problem karta hai. Single line me ya step-by-step karte hain.

***

## Step 1: Pehle File Delete Karo

```bash
rm README.md
```

***

## Step 2: Nano Editor Me Banao

```bash
nano README.md
```

Ab nano editor khulega. Usme yeh content paste karo:

```
# 📱 Telegram Direct Uploader

> Android phone ko server bana kar Telegram channel me files upload karo — bina bot, bina third-party server ke!

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🏠 Self-hosted | Phone hi server, koi external server nahi |
| 🔐 No Bot | Direct Telegram account se upload |
| 📁 Folder Upload | Ek folder ki sabhi files auto upload |
| ⏸️ Resume Support | Network error par wait karke resume hoga |
| 📦 2 GB Support | Bot API limit (50 MB) nahi, pure 2 GB |
| 💾 Progress Save | Beech me roko, baad me wahi se continue |

---

## 📥 Installation

### Step 1: Termux Install

- F-Droid se Termux download karo
- Settings → Apps → Termux → Permissions → Storage ON karo

### Step 2: Setup Commands

```bash
pkg update
pkg upgrade -y
pkg install python python-pip termux-api -y
pip install telethon
termux-setup-storage
```

---

## 🔑 API Credentials

### 1. my.telegram.org par jaao

https://my.telegram.org

### 2. Login karo

- Telegram number se login
- OTP Telegram par aayega

### 3. App Create karo

- **API development tools** → **Create Application**
- App name: `MyUploader`
- Short name: `uploader`
- Platform: `Desktop`

### 4. Credentials Copy karo

- `api_id` (number)
- `api_hash` (text)

---

## ⚙️ Setup

### .env File Banao

```bash
cat > .env << 'ENVEOF'
API_ID=12345678
API_HASH=your_api_hash_here
PHONE=+919876543210
CHANNEL=-1001234567890
ENVEOF
```

**Edit karo:**
```bash
nano .env
```

- `API_ID` → apna api_id
- `API_HASH` → apna api_hash
- `PHONE` → apna Telegram number
- `CHANNEL` → channel ID (`-100` prefix sahit)

---

## 🚀 Run

```bash
python tg_uploader.py
```

### Process:

1. Telegram login (OTP first time)
2. Channel confirm
3. Folder select (1-6 choice)
4. Sabhi files auto upload
5. Network error → wait → resume
6. Final report

---

## 📂 Common Paths

```
/storage/emulated/0/Download
/storage/emulated/0/DCIM/Camera
/storage/emulated/0/Movies
/storage/emulated/0/Documents
/storage/emulated/0/Pictures
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Permission denied | Termux Settings me Storage ON karo |
| Channel not found | `-100` prefix sahit ID dalo |
| Network error | Internet check karo, auto retry hoga |
| Module not found | `pip install telethon` run karo |

---

## 📝 Notes

- `.env` file ko private rakho (GitHub public mat dalna)
- `my_session.session` file ko kisi ko mat dena
- Beech me rokna ho to `Ctrl+C` — progress save rahegi

---

## 📄 License

Free to use, modify, share.

---

<div align="center">

**Made with ❤️ for self-hosted uploads**

</div>
```

***

## Step 3: Save Karo

Nano me:
- **Ctrl + O** → Enter dabao (save)
- **Ctrl + X** → Exit

***

## Step 4: Git Commit + Push

```bash
git add README.md
git commit -m "Update README with full details"
git push -u origin main
```

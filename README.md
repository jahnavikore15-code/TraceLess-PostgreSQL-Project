# TraceLess — Take Control of Your Digital Identity

> A simple digital footprint tracker powered by Flask and PostgreSQL.

TraceLess helps users organize their online presence, keep track of digital accounts, review inactive accounts, and manage privacy-related tasks from one dashboard.

The application provides a centralized place to manually record online platforms and monitor account activity. It helps users become more aware of their digital footprint and take practical steps toward better digital privacy.

---

## 🚀 Live Demo

**Frontend:** https://trace-less-postgre-sql-project.vercel.app

**GitHub:** https://github.com/jahnavikore15-code/TraceLess-PostgreSQL-Project

---

## 📌 Problem

People use multiple online platforms every day, including social media, professional networks, shopping websites, and other digital services.

Over time, it becomes difficult to remember all the accounts created across different platforms.

Users may face challenges such as:

- Forgetting old online accounts.
- Losing track of inactive accounts.
- Having no centralized record of their digital presence.
- Forgetting to review account privacy settings.
- Finding it difficult to organize digital account information.
- Not regularly reviewing their online privacy practices.

Without proper organization, managing a digital footprint can become difficult.

TraceLess aims to make this process simpler and more organized.

---

## 💡 Solution

TraceLess is a web-based Digital Footprint Tracker that helps users manage their online presence through a centralized dashboard.

Users can register, log in, add their online accounts, record their activity, and maintain a privacy checklist.

The application identifies accounts that have not been marked as recently used within the configured 90-day review period.

It also provides a privacy checklist where users can add tasks, mark them as completed, and monitor their progress.

TraceLess combines account organization, inactivity review, and privacy task management in one simple application.

---

## 🚀 Features

**User Authentication:** Register and log in securely using password hashing.

**Digital Account Management:** Add and organize online accounts from different platforms.

**Account Activity Tracking:** Mark accounts as recently used and maintain activity records.

**Inactive Account Detection:** Identify accounts requiring review based on a 90-day inactivity threshold.

**Privacy Checklist:** Create personal privacy-related tasks and manage them.

**Task Management:** Add, complete, and delete privacy checklist items.

**Dashboard Overview:** View account statistics, inactive account counts, and privacy checklist progress.

**PostgreSQL Database:** Persist user information, platforms, account records, activity logs, and privacy checklist data.

**Personalized Dashboard:** Each registered user manages their own digital footprint information.

---

## 🏗️ Architecture

TraceLess follows a simple web application architecture using Flask and PostgreSQL.

```text
                  ┌────────────────────────┐
                  │          USER          │
                  │   Register / Login     │
                  └────────────┬───────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │     Flask Web App      │
                  │    Request Handling    │
                  └────────────┬───────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
       ┌──────────────────┐         ┌──────────────────┐
       │  Authentication  │         │ Account Management│
       │  & User Sessions │         │ Add / View / Delete│
       └────────┬─────────┘         └────────┬─────────┘
                │                             │
                └──────────────┬──────────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │   Activity Tracking   │
                  │  Inactivity Review    │
                  └────────────┬───────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │   Privacy Checklist   │
                  │  Tasks & Progress     │
                  └────────────┬───────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │    PostgreSQL DB       │
                  │   Persistent Storage   │
                  └────────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| PostgreSQL | Relational database |
| Psycopg2 | PostgreSQL database connectivity |
| HTML5 | Frontend structure |
| CSS3 | User interface styling |
| Jinja2 | Dynamic HTML templates |
| Werkzeug | Password hashing and security utilities |
| Python-dotenv | Environment variable management |
| Git & GitHub | Version control and source code hosting |
| Vercel | Planned application deployment |

---

## 🗄️ Database Design

TraceLess uses PostgreSQL to store and organize application data.

The database contains the following main tables:

| Table | Purpose |
|---|---|
| users | Stores registered user information |
| platforms | Stores supported platform information |
| user_accounts | Stores users' digital account records |
| activity_logs | Maintains account activity history |
| privacy_checks | Stores privacy checklist tasks and completion status |

The relational database structure helps organize account information and maintain user-specific records.

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/TraceLess-PostgreSQL-Project.git
cd TraceLess-PostgreSQL-Project
```

If your project files are inside an additional `Traceless` folder, enter it:

```bash
cd Traceless
```

### 2. Create a virtual environment

```bash
py -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

Open pgAdmin 4 and create a database named:

```text
traceless_db
```

### 5. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=traceless_db
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
SECRET_KEY=your_secret_key
```

Replace the example values with your actual PostgreSQL credentials.

### 6. Start the application

```bash
python app.py
```

### 7. Open the application

Visit:

```text
http://127.0.0.1:5000
```

---

## 🌐 Deployment

The deployment architecture is planned as follows:

| Component | Platform |
|---|---|
| Web application | Vercel |
| PostgreSQL database | Neon |
| Source code | GitHub |

The application will use a hosted PostgreSQL database for production rather than relying on a local database.

Deployment and live demo links will be added after successful deployment and testing.

---

## 🔐 Security

- User passwords are hashed using Werkzeug security utilities.
- Database credentials are managed through environment variables.
- `.env` files are excluded from GitHub.
- User-specific account and checklist operations are protected by login sessions.
- The application does not require users to store their actual website passwords.

---

## 🔮 Future Enhancements

- Digital footprint analytics and visualizations.
- Account activity reminders.
- Exportable digital footprint reports.
- Advanced privacy recommendations.
- More detailed account categorization.
- Account review notifications.
- Improved dashboard analytics.

---

## 🔗 Project Links

**Live Demo:** https://trace-less-postgre-sql-project.vercel.app

**GitHub:** https://github.com/jahnavikore15-code/TraceLess-PostgreSQL-Project

**Technology:** Flask + PostgreSQL

---

## 👩‍💻 Author

**K. Sai Jahnavi**

B.Tech AIML Student

**GitHub:** https://github.com/jahnavikore15-code

---

## ⚠️ Disclaimer

TraceLess is a personal digital footprint organization tool. It relies on information manually entered and updated by users.

It does not automatically scan the internet, detect every account associated with a user, verify whether accounts have been deleted, or measure actual security exposure.

The inactivity review is based on recorded activity within TraceLess and should not be interpreted as proof that an online account is unused.

---

**TraceLess — Take Control of Your Digital Identity.**

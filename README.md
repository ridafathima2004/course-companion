 Course Companion

An AI-powered learning platform that helps students get answers strictly from their course videos — no confusion, no irrelevant information.

 What Problem Does It Solve?
 
When students watch course videos, they often have doubts — but searching the internet gives too much unrelated information. Course Companion solves this by providing an AI assistant that answers questions only from the uploaded course video content, keeping learners focused and on track.

 Features
Video-based AI assistance — AI answers are generated strictly from video transcriptions, not from the wider internet

Course material upload — Course providers can upload videos and materials to the platform

AI doubt clarification — Students ask questions and get answers sourced only from their course content

Admin panel — Manage course providers, users, approvals, and reviews

Cross-platform — Works on both web browser and Android

 Technologies Used
Layer            Technology
Backend          Python (Django)
Frontend         HTML, CSS
Mobile           Android Studio (Dart)
AI / NLP         Video Transcription, FAISS, Embeddings
Database         SQLite

 How It Works

Course Provider signs up and uploads course videos and materials
Platform transcribes the video content automatically
Student enrolls in a course and asks doubts via the AI chatbot
AI searches only the transcribed content and returns a relevant answer
No outside information is mixed in — keeping learning focused

 My Role
I was the Team Lead and primary developer for this project (team of 4).

Led project planning, system architecture, and documentation
Built the core backend logic in Python/Django
Designed the UI/UX for all screens
Integrated the AI video transcription and chatbot (chat_bot.py, videototext.py)
Coordinated team tasks and managed timelines

 Project Structure (Key Files)

course-companion/
├── views.py          # Core application logic

├── models.py         # Database models

├── urls.py           # URL routing

├── chat_bot.py       # AI chatbot logic

├── videototext.py    # Video transcription module

├── settings.py       # Django configuration

├── templates/        # HTML pages (login, dashboard, course views)

└── manage.py         # Django project manager

How to Run Locally
# 1. Clone the repository
git clone https://github.com/ridafathima2004/course-companion.git

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Start the server
python manage.py runserver

Author
Rida Fathima PP
BCA Graduate — Noble Women's College, Malappuram
UI/UX Designer | Aspiring Data Analyst | Frontend Developer

Status

Project completed as part of BCA final year — actively maintained and open for feedback.

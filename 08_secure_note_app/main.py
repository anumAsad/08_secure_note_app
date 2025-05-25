# secure_notes_app.py

import streamlit as st

# Base class
class Person:
    def __init__(self, username, password):
        self.username = username
        self._password = password  # encapsulation

    def check_password(self, password):
        return self._password == password

# User class
class User(Person):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def get_notes(self):
        return self.notes

# App logic
class SecureNotesApp:
    def __init__(self):
        self.users = {}

    def register_user(self, username, password):
        if username in self.users:
            return False
        self.users[username] = User(username, password)
        return True

    def login_user(self, username, password):
        user = self.users.get(username)
        if user and user.check_password(password):
            return user
        return None

# Initialize app state
if 'app' not in st.session_state:
    st.session_state.app = SecureNotesApp()
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

st.title("🔐 Secure Notes App")

# Registration and Login
if not st.session_state.current_user:
    tab1, tab2 = st.tabs(["Register", "Login"])

    with tab1:
        st.subheader("Create Account")
        reg_user = st.text_input("Username", key="reg_user")
        reg_pass = st.text_input("Password", type="password", key="reg_pass")
        if st.button("Register"):
            if st.session_state.app.register_user(reg_user, reg_pass):
                st.success("Registered successfully!")
            else:
                st.error("Username already taken.")

    with tab2:
        st.subheader("Login")
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            user = st.session_state.app.login_user(login_user, login_pass)
            if user:
                st.session_state.current_user = user
                st.success(f"Welcome, {user.username}!")
            else:
                st.error("Invalid credentials.")

# User Dashboard
else:
    user = st.session_state.current_user
    st.success(f"Logged in as {user.username}")

    new_note = st.text_area("Write a new note:")
    if st.button("Add Note"):
        user.add_note(new_note)
        st.info("Note added.")

    st.subheader("📒 Your Notes")
    notes = user.get_notes()
    if notes:
        for idx, note in enumerate(notes, 1):
            st.markdown(f"**{idx}.** {note}")
    else:
        st.write("No notes yet.")

    if st.button("Logout"):
        st.session_state.current_user = None
        st.experimental_rerun()

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.video import Video
from kivy.uix.modalview import ModalView
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.clock import Clock, mainthread
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.scrollview import ScrollView
from datetime import datetime
import os
import webbrowser
from plyer import notification
from kivymd.toast import toast
from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread
import pyrebase

# Firebase Configuration
firebase_config = {
    "apiKey": "AIzaSyChVoNLaFnfZScOmOvzf25xTPnvuKOA9a0",
    "authDomain": "memerdevs.firebaseapp.com",
    "projectId": "memerdevs",
    "storageBucket": "memerdevs.appspot.com",
    "messagingSenderId": "196291753965",
    "appId": "1:196291753965:web:62d382045826b757d999e4",
    "measurementId": "G-E0E0X8CQ98",
    "databaseURL": "https://memerdevs-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

# UI Definitions
KV = '''
ScreenManager:
    LoginScreen:
    SignUpScreen:
    HomeScreen:
    ProfileScreen:
    CommunityScreen:
    ChatScreen:

<LoginScreen>:
    name: "login"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 30
        MDLabel:
            text: "Login"
            halign: 'center'
            theme_text_color: "Primary"
            font_style: "H4"
        MDTextField:
            id: login_email
            hint_text: "Email"
            icon_right: "email"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.8
            required: True
        MDTextField:
            id: login_password
            hint_text: "Password"
            icon_right: "lock"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.8
            required: True
            password: True
        MDFlatButton:
            text: "forgot password?"
            on_release: app.forgot_password()
        MDRaisedButton:
            text: "Login"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.8
            on_release: app.login()
        MDFlatButton:
            text: "Don't have an account? Sign Up"
            pos_hint: {"center_x": 0.5}
            halign: 'center'
            theme_text_color: "Primary"
            on_press: app.switch_to_signup()

<SignUpScreen>:
    name: "signup"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        MDLabel:
            text: "Sign Up"
            halign: 'center'
            theme_text_color: "Primary"
            font_style: "H4"
        MDTextField:
            id: signup_username
            hint_text: "Username"
            icon_right: "account"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.8
            required: True
        MDTextField:
            id: signup_email
            hint_text: "Email"
            icon_right: "email"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.8
            required: True
        MDTextField:
            id: signup_password
            hint_text: "Password"
            icon_right: "lock"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.8
            required: True
            password: True
        MDRaisedButton:
            text: "Sign Up"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.8
            on_release: app.sign_up()
        MDFlatButton:
            text: "Already have an account? Login"
            pos_hint: {"center_x": 0.5, "center_y": 0}
            halign: 'center'
            theme_text_color: "Primary"
            on_press: app.switch_to_login()

<HomeScreen>:
    name: "home"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        MDLabel:
            text: "Home"
            halign: 'center'
            theme_text_color: "Primary"
            font_style: "H4"
        MDIcon:
            icon: "access-point-network"
            pos_hint: {"center_x": 0.5}
        MDBoxLayout:
            orientation: "vertical"
            id: server_results
        MDBoxLayout:
            orientation: 'horizontal'
            md_bg_color: 0, 0, 0, 0.1
            size_hint_y: None
            height: "50dp"
            MDIconButton:
                icon: "home"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.8
                on_release: app.switch_to_home()
            MDIconButton:
                icon: "account-group"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.8
                on_release: app.switch_to_community()
            MDIconButton:
                icon: "account"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.8
                on_release: app.switch_to_profile()
            
<ProfileScreen>:
    name: "profile"
    MDBoxLayout:
        padding: 20
        spacing: 10
        orientation: "vertical"
        MDIconButton:
            icon: "delete-forever-outline"
            pos_hint: {"top": 0.95, "right": 1}
            on_release: app.del_account_dialog()
        MDLabel:
            text: "Profile"
            halign: 'center'
            theme_text_color: "Primary"
            font_style: "H4"
        # Profile Picture Box
        MDBoxLayout:
            orientation: "vertical"
            size_hint_y: None
            size_hint_x: 0.6
            height: "230dp"
            padding: 20
            pos_hint: {"center_x": 0.5}
            FitImage:
                id: profile_picture
                source: ""
                allow_stretch: True
                keep_ratio: True
                radius: 100, 100, 100, 100
            MDIconButton:
                id: edit_pp_button
                icon: "image-edit"
                pos_hint: {"center_x": 0.5}
                disabled: True
                on_release: app.select_profile_picture()
        # Username Field (Editable)
        MDTextField:
            id: username_field
            text: "Username" # Placeholder text
            hint_text: "Username"
            halign: "center"
            disabled: True  # Start in view mode (disabled)
        # User Email Field (Editable)
        MDTextField:
            id: user_email_field
            text: "user@example.com"  # Placeholder text
            hint_text: "Email"
            halign: "center"
            disabled: True  # Start in view mode (disabled)
        # Bio Field (Editable)
        MDTextField:
            id: bio_field
            text: "Hey there, i'm using MemerDevs!"  # Placeholder text
            hint_text: "Bio"
            halign: "center"
            multiline: True
            disabled: True  # Start in view mode (disabled)
        # Edit and Save Buttons
        MDBoxLayout:
            orientation: 'horizontal'
            spacing: 20
            size_hint_y: None
            height: "50dp"
            MDIconButton:
                icon: "account-edit"
                on_release: app.toggle_edit_mode(True)
            MDIconButton:
                id: save_button
                icon: "content-save"
                on_release: app.save_profile_changes()
                disabled: True  # Disabled by default until edit mode is enabled
        MDBoxLayout:
            orientation: 'horizontal'
            md_bg_color: 0, 0, 0, 0.1
            size_hint_y: None
            height: "50dp"
            MDIconButton:
                icon: "home"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.8
                on_release: app.switch_to_home()
            MDIconButton:
                icon: "account-group"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.8
                on_release: app.switch_to_community()
            MDIconButton:
                icon: "account"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.8
                on_release: app.switch_to_profile()
                
<CommunityScreen>:
    name: "community"
    MDBoxLayout:
        padding: 20
        spacing: 10
        orientation: "vertical"
        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: "200dp"
            MDLabel:
                text: "Available Sections"
                size_hint_y: None
                height: "40dp"
                bold: True
                pos_hint: {"top": 1}
            ScrollView:
                MDList:
                    id: section_list
            MDIconButton:
                icon: "chat-plus"
                pos_hint: {"bottom": 1, "right": 1}
                on_release: app.show_create_section_dialog()
        MDBoxLayout:
            orientation: 'horizontal'
            md_bg_color: 0, 0, 0, 0.1
            size_hint_y: None
            height: "50dp"
            MDIconButton:
                icon: "home"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.8
                on_release: app.switch_to_home()
            MDIconButton:
                icon: "account-group"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.8
                on_release: app.switch_to_community()
            MDIconButton:
                icon: "account"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.8
                on_release: app.switch_to_profile()
                
<ChatScreen>:
    name: "chat"
    MDIconButton:
        icon: "keyboard-backspace"
        pos_hint: {"top": 1, "left": 1}
        on_release: app.switch_to_community()
    ScrollView:
        MDBoxLayout:
            id: chat_area
            orientation: "vertical"
            size_hint_y: None
            height: self.minimum_height
    MDBoxLayout:
        size_hint_y: None
        height: "50dp"
        MDTextField:
            id: message_input
            hint_text: "Type your message..."
            multiline: True
        MDRaisedButton:
            text: "Send"
            on_release: app.send_message_to_current_section()
'''

class LoginScreen(Screen):
    pass

class SignUpScreen(Screen):
    pass

class HomeScreen(Screen):
    pass
    
class ProfileScreen(Screen):
    pass

class CommunityScreen(Screen):
    pass
    
class ChatScreen(Screen):
    pass

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Directory where media will be saved
MEDIA_DIR = "/storage/emulated/0/MemerDevs/Media"

if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

@app.route('/upload_post', methods=['POST'])
def post_update():
    data = request.json
    username = data.get('username')
    post_text = data.get('caption')
    media_path = data.get('media_path')
    if not post_text and not media_path:
        toast("No content to post.")
        return jsonify ({"message": "No content to post."})

    # Upload media to Firebase storage if media is selected
    media_url = ""
    if media_path:
        media_filename = f"media/{current_user}/{media_path.split('/')[-1]}"
        storage.child(media_filename).put(media_path, user_id_token)
        media_url = storage.child(media_filename).get_url(user_id_token)
        print("Media uploaded, URL:", media_url)

    # Post data to Firebase Database
    post_data = {
        "usename": username,
        "text": post_text,
        "media_url": media_url,
        "likes": [],
        "comments": []
    }
    db.child("posts").push(post_data, user_id_token)
    return jsonify({"message": "Post created successfully."})
    toast("Post created successfully.")
        
@app.route('/get_posts', methods=['GET'])
def get_posts():
    posts = db.child("posts").get(user_id_token).val()
    return jsonify(posts)

@app.route('/search_posts', methods=['POST'])
def search_posts():
    posts = db.child("posts").get(user_id_token).val()
    data = request.json
    search_input = data.get("search_input")
    for text in posts.get("text"):
        if search_input in text:
            return jsonify(posts)
    
@app.route('/get_username', methods=['GET'])
def get_username():
    return jsonify({"username": username})
  
@app.route('/like_post', methods=['POST'])
def like_post():
    data = request.json
    post_key = data.get('post_key')
    username = data.get('username')

    post_data = db.child("posts").child(post_key).get(user_id_token).val()
    likes = post_data.get("likes", [])

    if username not in likes:
        likes.append(username)
        db.child("posts").child(post_key).update({"likes": likes}, user_id_token)
    
    return jsonify({"message": "Post liked.", "likes": len(likes)})

@app.route('/download_media', methods=['POST'])
def download_media():
    data = request.json
    media_url = data.get('media_url')
    save_path = os.path.join(MEDIA_DIR, media_url.split("/")[-1])
    
    try:
        import urllib.request
        urllib.request.urlretrieve(media_url, save_path)
        toast(f"Media saved to {save_path}")
        return jsonify({"message": f"Media saved to {save_path}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_comments', methods=['POST'])
def get_comments():
    data = request.json
    post_key = data.get('post_key')
    post_data = db.child("posts").child(post_key).get(user_id_token).val()
    comments = post_data.get("comments", [])
    return jsonify(comments)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    data = request.json
    post_key = data.get('post_key')
    comment_text = data.get('comment_text')
    username = data.get('username')

    if comment_text:
        post_data = db.child("posts").child(post_key).get(user_id_token).val()
        comments = post_data.get("comments", [])

        new_comment = {"username": username, "text": comment_text}
        comments.append(new_comment)

        db.child("posts").child(post_key).update({"comments": comments}, user_id_token)

        return jsonify({"message": "Comment added.", "comments": comments})
    return jsonify({"message": "Comment text is required."}), 400
    
def run_flask():
    app.run(debug=False, use_reloader=False, port=5000)
    
class TokenManager:
    def __init__(self, user):
        self.user = user
        self.time = 3000  # Initial countdown time in seconds

    def start_timer(self):
        Clock.schedule_interval(self.stop_timer, 1)  # Schedule stop_timer to run every second

    def stop_timer(self, dt):
        if self.time > 0:
            self.time -= 1
        else:
            Clock.unschedule(self.stop_timer)
            self.keep_token_fresh()

    def keep_token_fresh(self):
        new_id_token = self.refresh_id_token()
        print("Token refreshed. New ID token:", new_id_token)
        global user_id_token
        user_id_token = new_id_token

    def refresh_id_token(self):
        # Refresh the token before it expires
        refreshed_user = auth.refresh(self.user['refreshToken'])
        return refreshed_user['idToken']

class MemerDevsApp(MDApp):
    media_path = None
    global current_user
    current_user = None
    global user_id_token
    user_id_token = None
    edit_mode = False
    current_section_id = None
    my_stream = None
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.sm = Builder.load_string(KV)
        return self.sm
        
    def switch_to_signup(self):
        self.sm.current = "signup"
        
    def switch_to_login(self):
        self.sm.current = "login"
        
    def switch_to_home(self):
        self.sm.current = "home"
        
    def switch_to_community(self):
        self.check_if_user_in_community()
        
    def switch_to_profile(self):
        self.sm.current = "profile"
        self.load_user_profile()
        
    def notify(self, title, message):
        notification.notify(title=f'{title}', message=f'{message}', app_name='MemerDevs')
        toast(f"{title}: {message}")
        
    def login(self):
        email = self.sm.get_screen('login').ids.login_email.text
        global password
        password = self.sm.get_screen('login').ids.login_password.text
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            manager = TokenManager(user)
            manager.start_timer()
            self.current_user = user['localId']
            self.user_id_token = user['idToken']
            user_data = db.child("users").child(self.current_user).get(self.user_id_token).val()
            global username
            username = user_data.get("username", "")
            self.switch_to_home()
            self.show_medias()
        except Exception as e:
            print("Invalid credentials:", e)
            self.notify("Invalid credentials", "Login failed.")

    def sign_up(self):
        email = self.sm.get_screen('signup').ids.signup_email.text
        global password
        password = self.sm.get_screen('signup').ids.signup_password.text
        global username
        username = self.sm.get_screen("signup").ids.signup_username.text
        try:
            user = auth.create_user_with_email_and_password(email, password)
            manager = TokenManager(user)
            manager.start_timer()
            self.current_user = user['localId']
            self.user_id_token = user['idToken']
            auth.send_email_verification(self.user_id_token)
            data = {
                "username": username,
                "photo_url": "https://firebasestorage.googleapis.com/v0/b/memerdevs.appspot.com/o/Default%2Fdefault-profile-pic.jpg?alt=media&token=8e017016-e28d-4bc6-81d0-bb96cd354d3e",
                "email": email,
                "bio": "Hey there, i'm using MemerDevs!"
            }
            db.child("users").child(self.current_user).set(data, self.user_id_token)
            self.switch_to_home()
            self.show_medias()
        except Exception as e:
            print("Sign-up failed:", e)
            self.notify("Sign Up Error", "Error signing up.")
            
    def forgot_password(self):
        self.email_popup = ModalView(size_hint_y=None, height="250dp", auto_dismiss=False)
        box_layout = MDBoxLayout(orientation="vertical", md_bg_color=(1, 1, 1, 1))
        label = MDLabel(text="Enter your email address and check your email to reset password.", bold=True, pos_hint={"center_x": 0.5})
        self.pass_email_input = MDTextField(hint_text="Enter your email address.")
        self.cont_button = MDRaisedButton(text="Continue", pos_hint={"right": 0.95}, on_release=self.send_pass_reset_email)
        box_layout.add_widget(label)
        box_layout.add_widget(self.pass_email_input)
        box_layout.add_widget(self.cont_button)
        self.email_popup.add_widget(box_layout)
        self.email_popup.open()
        
    def send_pass_reset_email(self, obj):
        try:
            auth.send_password_reset_email(self.pass_email_input.text)
            toast("check your email for password reset link.")
            self.email_popup.dismiss()
        except Exception:
            self.notify("Password Reset", "Error occured")
            self.email_popup.dismiss()
        
    def del_account_dialog(self):
        self.del_acc_dialog = MDDialog(
            text="Are you sure you want to delete your account?\n it will be deleted forever.",
            buttons=[
                MDFlatButton(text="NO", on_release=self.close_del_dialog),
                MDRaisedButton(text="YES", on_release=self.delete_account)
            ]
        )
        self.del_acc_dialog.open()
        
    def delete_account(self, obj):
        self.acc_popup = ModalView(size_hint_y=None, height="300dp", auto_dismiss=False)
        box_layout = MDBoxLayout(orientation="vertical", md_bg_color=(1, 1, 1, 1))
        self.acc_label = MDLabel(text="Delete Account.", font_style="H3", pos_hint={"center_x": 0.5})
        self.del_pass_input = MDTextField(hint_text="Confirm password.")
        self.confirm_del_button = MDRaisedButton(text="Continue", pos_hint={"right": 0.95}, on_release=self.del_acc_conclusion)
        box_layout.add_widget(self.acc_label)
        box_layout.add_widget(self.del_pass_input)
        box_layout.add_widget(self.confirm_del_button)
        self.acc_popup.add_widget(box_layout)
        self.acc_popup.open()
        
    def del_acc_conclusion(self, obj):
        if self.del_pass_input == password:
           try:
               db.child("users").child(self.current_user).remove(self.user_id_token)
               storage.delete(f"Profile_Pictures/{self.current_user}", self.user_id_token)
               auth.delete_user_account(self.user_id_token)
               self.notify("Account removal", "Account deleted successfully.")
               self.acc_popup.dismiss()
               self.switch_to_login()
           except Exception:
               self.notify("Account removal", "Error deleting account.")
               self.acc_popup.dismiss()
        else:
           self.del_pass_input.error = True
    
    def close_del_dialog(self):
        self.del_acc_dialog.dismiss()
        
    def check_if_user_in_community(self):
        user_data = db.child("users").child(self.current_user).get(self.user_id_token).val()

        if not user_data.get("is_in_community", False):
            self.show_join_community_prompt()
        else:
            self.load_available_sections
            self.sm.current = "community"

    def show_join_community_prompt(self):
        self.join_community_dialog = MDDialog(
            text="Would you like to join the community?",
            buttons=[
                MDFlatButton(text="NO", on_release=self.close_dialog),
                MDRaisedButton(text="YES", on_release=self.join_community)
            ]
        )
        self.join_community_dialog.open()

    def join_community(self, *args):
        db.child("users").child(self.current_user).update({"is_in_community": True}, self.user_id_token)
        self.close_dialog()
        toast("Successfully joined communities.")
        self.sm.current = "community"

    def close_dialog(self):
            self.join_community_dialog.dismiss()

    def create_section(self, section_name):
        section_data = {
            "name": section_name,
            "created_by": self.current_user,
            "members": [self.current_user]
        }
        db.child("sections").push(section_data, self.user_id_token)

    def load_available_sections(self):
        sections = db.child("sections").get(self.user_id_token).val()
        section_list = self.sm.get_screen('community').ids.section_list

        if sections:
            for section_id, section_data in sections.items():
                section_name = section_data.get('name', '')
                section_list.add_widget(
                    OneLineListItem(
                        text=section_name,
                        on_release=lambda x, section_id=section_id: self.handle_section_click(section_id)
                    )
                )

    def handle_section_click(self, section_id):
        section_data = db.child("sections").child(section_id).get(self.user_id_token).val()

        if self.current_user not in section_data['members']:
            self.join_section(section_id)
        else:
            self.switch_section(section_id)

    def join_section(self, section_id):
        section_data = db.child("sections").child(section_id).get(self.user_id_token).val()
        members = section_data.get('members', [])
        if self.current_user not in members:
            members.append(self.current_user)
            db.child("sections").child(section_id).update({"members": members}, self.user_id_token)
        self.switch_section(section_id)

    def load_messages(self, section_id):
        messages = db.child("sections").child(section_id).child("messages").get(self.user_id_token).val()
        if messages:
            for msg_id, msg_data in messages.items():
                self.display_message(msg_data)

    @mainthread
    def display_message(self, msg_data):
        sender_id = msg_data['sender']
        sender_data = db.child("users").child(sender_id).get(self.user_id_token).val()

        sender_name = sender_data['name']
        sender_profile_pic = sender_data.get('photo_url', '')

        chat_screen = self.sm.get_screen('chat')
        chat_layout = chat_screen.ids.chat_area
        chat_layout.add_widget(
            MDBoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height="40dp",
                children=[
                    MDIconButton(
                        icon=sender_profile_pic,
                        user_font_size="24sp",
                        size_hint_x=None,
                        width="40dp"
                    ),
                    MDLabel(
                        text=f"{sender_name}:\n {msg_data['text']}",
                        halign="left"
                    )
                ]
            )
        )

    def send_message_to_current_section(self):
        if not self.current_section_id:
            return

        message_text = self.sm.get_screen("chat").ids.message_input.text.strip()
        if message_text == "":
            return

        message_data = {
            "sender": self.current_user,
            "text": message_text,
            "timestamp": self.get_current_time(),
        }

        db.child("sections").child(self.current_section_id).child("messages").push(message_data, self.user_id_token)
        self.sm.get_screen("chat").ids.message_input.text = ""

    def start_message_listener(self, section_id):
        self.my_stream = db.child("sections").child(section_id).child("messages").stream(self.on_new_message)

    @mainthread
    def on_new_message(self, message):
        if message["data"] is not None:
            self.display_message(message["data"])

    def stop_message_listener(self):
        if self.my_stream:
            self.my_stream.close()

    def switch_section(self, new_section_id):
        if self.my_stream:
            self.stop_message_listener()

        self.current_section_id = new_section_id
        self.sm.current = "chat"
        self.start_message_listener(new_section_id)
        self.root.ids.chat_area.clear_widgets()
        self.load_messages(new_section_id)

    def get_current_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def show_create_section_dialog(self):
        self.create_section_dialog = MDDialog(
            title="Create New Section",
            type="custom",
            content_cls=MDTextField(
                hint_text="Enter section name",
                id="section_name_input"
            ),
            buttons=[
                MDRaisedButton(
                    text="CANCEL",
                    on_release=self.close_create_section_dialog
                ),
                MDRaisedButton(
                    text="CREATE",
                    on_release=self.create_section_handler
                ),
            ],
        )
        self.create_section_dialog.open()

    def close_create_section_dialog(self, obj):
        self.create_section_dialog.dismiss()

    def create_section_handler(self, *args):
        section_name = self.create_section_dialog.content_cls.text
        if section_name:
            self.create_section(section_name)
            self.close_create_section_dialog()
        else:
            self.create_section_dialog.content_cls.error = True
        
    def load_user_profile(self):
        user_data = db.child("users").child(self.current_user).get(self.user_id_token).val()
        profile_screen = self.sm.get_screen('profile')
        profile_screen.ids.profile_picture.source = user_data.get("photo_url", "")
        profile_screen.ids.username_field.text = user_data.get("username", "")
        profile_screen.ids.user_email_field.text = user_data.get("email", "")
        profile_screen.ids.bio_field.text = user_data.get("bio", "")

    def toggle_edit_mode(self, enable):
        profile_screen = self.sm.get_screen('profile')
        
        # Enable or disable fields based on edit mode
        profile_screen.ids.username_field.disabled = not enable
        profile_screen.ids.bio_field.disabled = not enable
        profile_screen.ids.edit_pp_button.disabled = not enable
        profile_screen.ids.save_button.disabled = not enable
        self.edit_mode = enable

    def save_profile_changes(self):
        if self.edit_mode:
            # Save the changes to Firebase
            profile_screen = self.sm.get_screen('profile')
            db_user_data = db.child("users").child(self.current_user).get(self.user_id_token).val()
            new_username = profile_screen.ids.username_field.text
            new_bio = profile_screen.ids.bio_field.text
            new_pp = profile_screen.ids.profile_picture.source
            user_data = {
                "username": new_username,
                "bio": new_bio
            }
            if new_pp != db_user_data.get("profile_url", ""):
                image_filename = f"Profile_Pictures/{self.current_user}/{new_pp.split('/')[-1]}"
                storage.delete(f"Profile_Pictures/{self.current_user}", self.user_id_token)
                storage.child(image_filename).put(self.image_path, self.user_id_token)
                image_url = storage.child(image_filename).get_url(self.user_id_token)
                user_data["profile_url"] = image_url
            db.child("users").child(self.current_user).update(user_data, self.user_id_token)
            print("Profile updated successfully.")
            self.notify("Profile Update", "Profile updated successfully.")
            
            # Exit edit mode
            self.toggle_edit_mode(False)

    def select_profile_picture(self):
        content = FileChooserIconView(filters=["*.jpeg", "*.jpg", "*.png", "*.webp", "*.ico"], size_hint=(1, 1))

        self.image_popup = Popup(title="Select Profile Picture", content=content, size_hint=(0.9, 0.9))
        content.bind(selection=self.on_picture_select)
        self.image_popup.open()
        
    def on_picture_select(self, instance, selection):
        if selection:
            self.image_path = selection[0]
            print("image selected: ", self.image_path)
            self.sm.get_screen("profile").ids.profile_picture.source = f"{self.image_path}"

    def show_medias(self):
        flask_thread = Thread(target=run_flask)
        flask_thread.start()
        home_screen = self.sm.get_screen('home')
        box_layout = home_screen.ids.server_results
        message = MDLabel(text="Running on browser...", pos_hint={"center_x": 0.5}, bold=True)
        toast("URL: https://memerdevs.web.app")
        redirect_button = MDRaisedButton(text="Open Browser", pos_hint={"center_x": 0.5}, on_release=self.open_link)
        box_layout.add_widget(message)
        box_layout.add_widget(redirect_button)
        
    def open_link(self, instance):
        webbrowser.open("https://memerdevs.web.app")

if __name__ == '__main__':
    MemerDevsApp().run()
from kivy import Config
Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'gl_backend', 'angle_sdl2')
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.modalview import ModalView
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem, OneLineAvatarListItem, ImageLeftWidget
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.clock import Clock
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivy.uix.image import AsyncImage
from kivymd.uix.fitimage import FitImage
from kivymd.uix.dialog import MDDialog
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from datetime import datetime
import os
import platform
import webbrowser
from plyer import notification
from kivymd.toast import toast
from PIL import Image
from io import BytesIO
import requests
import urllib.request
import random
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
    SettingsScreen:
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
            hint_text: "password"
            icon_right: "lock"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.8
            required: True
            password: True
        MDFlatButton:
            text: "forgot password?"
            on_release: app.forgot_password()
            pos_hint: {"center_x": 0.25}
            theme_text_color: "Secondary"
        MDRaisedButton:
            text: "Login"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.8
            on_release: app.login()
        MDFlatButton:
            text: "Don't have an account? Sign Up"
            pos_hint: {"center_x": 0.5}
            halign: 'center'
            theme_text_color: "Custom"
            text_color: "blue"
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
            hint_text: "password"
            icon_right: "lock"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.8
            required: True
            password: True
        MDBoxLayout:
            size_hint_y: None
            height: 80
            md_bg_color: 0, 0, 0.4, 0.025
            CheckBox:
                id: checkbox
                size_hint_x: 0.1
                color: 0.1, 0.1, 0.4, 1
                on_press: app.checkbox_state()
            MDLabel:
                text: "I agree to User Agreement"
                size_hint_x: 0.3
                color: 0.1, 0.1, 0.4, 0.9
        MDRaisedButton:
            id: signup_button
            disabled: True
            text: "Sign Up"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.8
            on_release: app.sign_up()
        MDFlatButton:
            text: "Already have an account? Login"
            pos_hint: {"center_x": 0.5, "center_y": 0}
            halign: 'center'
            theme_text_color: "Custom"
            text_color: "blue"
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
            size_hint_y: None
            height: "50dp"
        ScrollView:
            id: post_render
        MDIconButton:
            icon: "attachment-plus"
            pos_hint: {"bottom": 1, "right": 1}
            on_release: app.add_post()
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
            MDIconButton:
                icon: "cog"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.8
                on_release: app.switch_to_settings()
            
<ProfileScreen>:
    name: "profile"
    MDBoxLayout:
        padding: 20
        spacing: 10
        orientation: "vertical"
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
        MDBoxLayout:
            orientation: "horizontal"
            md_bg_color: 0, 0, 0, 0.05
            MDLabel:
                id: followers
                bold: True
                pos_hint: {"center_x": 0.5}
            MDLabel:
                id: following
                bold: True
                pos_hint: {"center_x": 0.5}
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
            MDIconButton:
                icon: "cog"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.8
                on_release: app.switch_to_settings()

<SettingsScreen>:
    name: "settings"
    MDBoxLayout:
        padding: 20
        spacing: 10
        orientation: "vertical"
        MDLabel:
            text: "Settings"
            halign: 'center'
            theme_text_color: "Primary"
            font_style: "H4"
            size_hint_y: None
            height: "50dp"
        ScrollView:
            MDList:
                OneLineIconListItem:
                    text: "Become a patreon."
                    on_release: app.support()
                    IconLeftWidget:
                        icon: "hand-coin"
                OneLineIconListItem:
                    text: "Change password"
                    on_release: app.forgot_password()
                    IconLeftWidget:
                        icon: "key"
                OneLineIconListItem:
                    text: "Delete Account"
                    on_release: app.del_account_dialog()
                    IconLeftWidget:
                        icon: "delete-forever-outline"
                OneLineIconListItem:
                    text: "Legal Information"
                    on_release: app.legal_info()
                    IconLeftWidget:
                        icon: "file-document-multiple"
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
            MDIconButton:
                icon: "cog"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.8
                on_release: app.switch_to_settings()

<CommunityScreen>:
    name: "community"
    MDBoxLayout:
        padding: 20
        spacing: 10
        orientation: "vertical"
        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: "50dp"
            MDLabel:
                text: "Available Sections"
                bold: True
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
            MDIconButton:
                icon: "cog"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.8
                on_release: app.switch_to_settings()
                
<ChatScreen>:
    name: "chat"
    MDBoxLayout:
        orientation: "vertical"
        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: "50dp"
            md_bg_color: 0.1, 0.1, 0.1, 0.1
            MDIconButton:
                icon: "keyboard-backspace"
                on_release: app.switch_to_community()
            MDLabel:
                id: section_name
                bold: True
        ScrollView:
            MDBoxLayout:
                id: chat_area
                spacing: 20
                padding: 20
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
            MDIconButton:
                icon: "send"
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
    
class SettingsScreen(Screen):
    pass

def get_media_dir():
    system = platform.system()

    if system == "Linux" or system == "Darwin":
        if "iPhone" in platform.platform() or "iPad" in platform.platform():
            media_dir = os.path.expanduser("~/Documents/MemerDevs/Media")
        else:
            media_dir = os.path.expanduser("~/MemerDevs/Media")
    elif system == "Windows":
        media_dir = os.path.join(os.getenv('USERPROFILE'), "MemerDevs", "Media")
    elif system == "Android":
        media_dir = "/storage/emulated/0/MemerDevs/Media"
    else:
        raise Exception("Unsupported platform")

    if not os.path.exists(media_dir):
        os.makedirs(media_dir)
    
    return media_dir

MEDIA_DIR = get_media_dir()
            
class PostRenderer(MDList):
    def __init__(self, posts, user_id_token, **kwargs):
        super().__init__(**kwargs)
        self.render_posts(posts)
        self.spacing = 10
        self.user_id_token = user_id_token

    def render_posts(self, posts):
        for post in posts:
            post_key = post["postId"]
            post_card = MDCard(orientation='vertical', padding=10, size_hint_y=None)
            post_card.height = "500dp"

            username_label = MDFlatButton(
                text=post['username'], 
                theme_text_color='Primary', 
                halign='center',
                font_size=48
            )
            username_label.bind(on_release=lambda instance: self.view_profile(post['userId']))
            post_card.add_widget(username_label)

            # Post text
            if 'text' in post:
                post_text = MDLabel(
                    text=post['text'],
                    theme_text_color='Secondary',
                    halign='center'
                )
                post_card.add_widget(post_text)

            # Post image
            if post['media_url'] != "":
                post_image = AsyncImage(source=post['media_url'], size_hint_y=None, size_hint_x=0.7, pos_hint={"center_x": 0.5})
                post_image.height = "300dp"
                post_card.add_widget(post_image)
                button_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height="50dp")

            # Like button with dynamic heart
            is_liked = post.get('likes') and username in post['likes']
            self.like_icon = 'heart' if is_liked else 'heart-outline'
            self.like_button = MDIconButton(
                icon=self.like_icon,
                on_release=lambda x, post_key=post_key: self.like_post(post_key)
            )
            self.like_len = MDLabel(text=f'{len(post.get("likes", []))}')
            button_layout.add_widget(self.like_button)
            button_layout.add_widget(self.like_len)

            comments_button = MDIconButton(
                icon="comment-outline",
                on_release=lambda x, post_key=post_key: self.show_comments(post_key)
            )
            self.comments_len = MDLabel(text=f'{len(post.get("comments", []))}')
            button_layout.add_widget(comments_button)
            button_layout.add_widget(self.comments_len)
            
            if 'media_url' in post:
                download_button = MDIconButton(
                    icon="download",
                    on_release=lambda x, media_url=post['media_url']: self.download_post(media_url)
                )
                button_layout.add_widget(download_button)

            views_label = MDLabel(
                text=f'Views: {post["views"]}',
                theme_text_color='Secondary',
                halign='left'
            )
            button_layout.add_widget(views_label)
            post_card.add_widget(button_layout)

            self.add_widget(post_card)
            
    def view_profile(self, user_id):
        if user_id != current_user:
            user_data = db.child("users").child(user_id).get(self.user_id_token).val()
            if user_data:
                profile_screen = UserProfile(user_data=user_data, user_id_token=self.user_id_token)
                profile_screen.open()
            else:
                toast("User not found.")
        else:
            MDApp.get_running_app().switch_to_profile()

    def like_post(self, post_key):
        # Fetch post data from Firebase
        post_data = db.child("posts").child(post_key).get(self.user_id_token).val()
        likes = post_data.get("likes", [])
        
        # Toggle like status
        if username not in likes:
            likes.append(username)
        else:
            likes.remove(username)

        # Update post likes in Firebase
        db.child("posts").child(post_key).update({"likes": likes}, self.user_id_token)
        toast(f"{'Liked' if username in likes else 'Unliked'} the post.")
        is_liked = likes and username in likes
        self.like_icon = 'heart' if is_liked else 'heart-outline'
        self.like_button.icon = self.like_icon
        self.like_len.text = f"{len(likes)}"

    def show_comments(self, post_key):
        post_data = db.child("posts").child(post_key).get(self.user_id_token).val()
        comments = post_data.get("comments", [])
        
        self.comments_screen = ModalView(auto_dismiss=True)

        comments_slideshow = self.create_comments_slideshow(comments)
        self.comments_screen.add_widget(comments_slideshow)
        comment_field_layout = MDBoxLayout(orientation="horizontal", spacing=10)
        comment_field = MDTextField(
            hint_text="Add a comment...",
            size_hint_x=0.9,
            pos_hint={'center_x': 0.5},
            multiline=True
        )
        comment_field_layout.add_widget(comment_field)

        submit_button = MDIconButton(
            icon="send",
            on_release=lambda x: self.add_comment(post_key, comment_field.text)
        )
        comment_field_layout.add_widget(submit_button)
        self.comments_screen.add_widget(comment_field_layout)
        self.comments_screen.open()

    def create_comments_slideshow(self, comments):
        slideshow_layout = MDBoxLayout(orientation='vertical', md_bg_color=(1, 1, 1, 1))
        comment_scrollview = ScrollView()
        comment_listview = MDList(spacing=10)
        slideshow_layout.add_widget(comment_scrollview)
        comment_scrollview.add_widget(comment_listview)

        for comment in comments:
            comment_user = db.child("users").child(current_user).get(self.user_id_token).val()
            comment_card = MDBoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height="80dp",
                md_bg_color=(0.1, 0.1, 0.3, 0.1),
                radius=(30, 30, 30, 30)
            )

            header_box = MDBoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height="40dp",
                md_bg_color=(0.05, 0.05, 0.15, 0.1)
            )

            avatar = ImageLeftWidget(source=comment_user.get("photo_url",""), radius=(100, 100, 100, 100), size_hint_x=0.15)
            header_box.add_widget(avatar)

            sender_label = MDLabel(
                text=comment_user.get("username",""),
                halign="left",
                font_style="Subtitle1" 
            )
            header_box.add_widget(sender_label)

            comment_card.add_widget(header_box)

            message_text = MDLabel(
                text=comment['text'],
                color=(0.1, 0.1, 0.4, 0.9),
                halign="left",
                size_hint_y=None,
                height="40dp"
            )
            comment_card.add_widget(message_text)
            
            comment_listview.add_widget(comment_card)
        
        return slideshow_layout

    def get_current_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def add_comment(self, post_key, comment_text):
        if comment_text:
            post_data = db.child("posts").child(post_key).get(self.user_id_token).val()
            comments = post_data.get("comments", [])

            new_comment = {"user": current_user, "text": comment_text, "timestamp": self.get_current_time()}
            comments.append(new_comment)

            db.child("posts").child(post_key).update({"comments": comments}, self.user_id_token)

            toast("Comment added.")
            self.comments_screen.dismiss()
            self.comments_len.text = f"{len(comments)}"
        else:
            toast("Comment text cannot be empty.")

    def download_post(self, media_url):
        filename = media_url.split("/")[-1].split("?")[0].split("%2F")[-1]
        save_path = os.path.join(MEDIA_DIR, filename)
        try:
            urllib.request.urlretrieve(media_url, save_path)
            toast(f"File downloaded successfully and saved as: {save_path}")
        except Exception as e:
            print(f"Error downloading the file: {e}")
        
class UserProfile(ModalView):
    def __init__(self, user_data, user_id_token, **kwargs):
        super().__init__(**kwargs)
        self.size_hint=(None, None)
        self.size =("300dp", "400dp")
        self.padding = 10
        self.auto_dismiss = True
        self.user_data = user_data
        self.user_id_token = user_id_token
        self.render_profile(user_data)

    def render_profile(self, user_data):
        # Main profile card
        profile_card = MDCard(orientation='vertical', padding=20, size_hint=(None, None), size=("300dp", "400dp"))
        
        # User Details Layout
        user_details_layout = MDBoxLayout(orientation='horizontal', size_hint=(1, None), height="150dp")

        # User Avatar
        avatar = FitImage(
            source=user_data.get("photo_url", ""),  # You can replace with actual image link
            size_hint=(None, None),
            size=("120dp", "120dp"),
            radius=(50, 50, 50, 50)
        )
        user_details_layout.add_widget(avatar)

        # User Text Layout
        user_text_layout = MDBoxLayout(orientation='vertical', padding=10)
        
        # Username
        username_label = MDLabel(
            text=f"Username: {user_data.get('username', 'N/A')}",
            theme_text_color="Primary"
        )
        user_text_layout.add_widget(username_label)

        # Bio
        bio_label = MDLabel(
            text=f"Bio: {user_data.get('bio', 'N/A')}",
            theme_text_color="Secondary"
        )
        user_text_layout.add_widget(bio_label)

        user_details_layout.add_widget(user_text_layout)
        profile_card.add_widget(user_details_layout)

        # User Interactions (Likes, Followers, Following)
        interactions_layout = MDBoxLayout(orientation='horizontal', padding=10)
        
        self.followers_label = MDLabel(
            text=f"Followers: {len(user_data.get('followers', []))}",
            theme_text_color="Primary"
        )
        interactions_layout.add_widget(self.followers_label)

        following_label = MDLabel(
            text=f"Following: {len(user_data.get('following', []))}",
            theme_text_color="Primary"
        )
        interactions_layout.add_widget(following_label)

        profile_card.add_widget(interactions_layout)

        # Add the profile card to the layout
        self.add_widget(profile_card)

        # Buttons Section
        buttons_layout = MDBoxLayout(orientation='horizontal', size_hint=(1, None), height="50dp", padding=(0, 20))

        # Follow Button with dynamic text
        is_following = self.check_following_status(user_data.get('userId'))
        follow_button_text = "Unfollow" if is_following else "Follow"

        self.follow_button = MDRaisedButton(
            text=follow_button_text,
            on_release=lambda x: self.toggle_follow_user(user_data.get('userId'))
        )
        buttons_layout.add_widget(self.follow_button)
        
        self.add_widget(buttons_layout)

    def check_following_status(self, user_id):
        # Fetch the current user's data
        current_user_data = db.child("users").child(current_user).get(self.user_id_token).val()
        following = current_user_data.get('following', [])

        # Check if the current user is following the profile user
        return user_id in following

    def toggle_follow_user(self, user_id):
        current_user_data = db.child("users").child(current_user).get(self.user_id_token).val()
        following = current_user_data.get('following', [])
        if user_id in following:
            following.remove(user_id)
            self.follow_button.text = "Follow"
        else:
            following.append(user_id)
            self.follow_button.text = "Unfollow"

        db.child("users").child(current_user).update({'following': following}, self.user_id_token)

        followers = self.user_data.get('followers', [])

        if current_user in followers:
            followers.remove(current_user)
        else:
            followers.append(current_user)

        db.child("users").child(user_id).update({'followers': followers}, self.user_id_token)
        self.followers_label.text = f"Followers: {len(followers)}"

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
        print("Token refreshed.")
        global user_id_token
        user_id_token = new_id_token

    def refresh_id_token(self):
        # Refresh the token before it expires
        refreshed_user = auth.refresh(self.user['refreshToken'])
        return refreshed_user['idToken']

class MemerDevsApp(MDApp):
    media_path = None
    edit_mode = False
    current_section_id = None
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.sm = Builder.load_string(KV)
        return self.sm
        
    def support(self):
        webbrowser.open("https://patreon.com/gofaone315")
        
    def legal_info(self):
        webbrowser.open("https://memerdevs.app.web/legal-information.html")
        
    def switch_to_signup(self):
        self.sm.current = "signup"
        
    def switch_to_login(self):
        self.sm.current = "login"
        
    def switch_to_home(self):
        self.sm.current = "home"
        self.show_medias()
        
    def switch_to_community(self):
        self.check_if_user_in_community()
        
    def switch_to_profile(self):
        self.sm.current = "profile"
        self.load_user_profile()
     
    def switch_to_settings(self):
        self.sm.current = "settings"
        
    def notify(self, title, message):
        notification.notify(title=f'{title}', message=f'{message}', app_name='MemerDevs')
    
    def checkbox_state(self):
        checkbox = self.sm.get_screen('signup').ids.checkbox
        signup_btn = self.sm.get_screen('signup').ids.signup_button
        if checkbox.active:
            signup_btn.disabled = False
        else:
            signup_btn.disabled = True
            
    def login(self):
        email = self.sm.get_screen('login').ids.login_email.text
        self.password = self.sm.get_screen('login').ids.login_password.text
        try:
            user = auth.sign_in_with_email_and_password(email, self.password)
            manager = TokenManager(user)
            manager.start_timer()
            global current_user
            current_user = user['localId']
            self.user_id_token = user['idToken']
            user_data = db.child("users").child(current_user).get(self.user_id_token).val()
            global username
            username = user_data.get("username", "")
            self.switch_to_home()
        except Exception as e:
            print("Invalid credentials:", e)
            self.notify("Invalid credentials", "Login failed.")

    def sign_up(self):
        email = self.sm.get_screen('signup').ids.signup_email.text
        self.password = self.sm.get_screen('signup').ids.signup_password.text
        global username
        username = self.sm.get_screen("signup").ids.signup_username.text
        try:
            user = auth.create_user_with_email_and_password(email, self.password)
            manager = TokenManager(user)
            manager.start_timer()
            global current_user
            current_user = user['localId']
            self.user_id_token = user['idToken']
            auth.send_email_verification(self.user_id_token)
            data = {
                "username": username,
                "photo_url": "https://firebasestorage.googleapis.com/v0/b/memerdevs.appspot.com/o/Default%2Fdefault-profile-pic.jpg?alt=media&token=8e017016-e28d-4bc6-81d0-bb96cd354d3e",
                "email": email,
                "bio": "Hey there, i'm using MemerDevs!",
                "followers": [],
                "following": []
            }
            db.child("users").child(current_user).set(data, self.user_id_token)
            self.switch_to_home()
            self.show_medias()
        except Exception as e:
            print("Sign-up failed:", e)
            self.notify("Sign Up Error", "Error signing up.")
        
    def forgot_password(self):
        self.email_popup = ModalView(size_hint_y=None, height="250dp", auto_dismiss=True)
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
            self.notify("password Reset", "Error occured")
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
        self.acc_popup = ModalView(size_hint_y=None, height="300dp", auto_dismiss=True)
        box_layout = MDBoxLayout(orientation="vertical", md_bg_color=(1, 1, 1, 1))
        self.acc_label = MDLabel(text="Delete Account.", font_style="H3", pos_hint={"center_x": 0.5})
        self.del_pass_input = MDTextField(hint_text="Confirm password.", password=True)
        self.confirm_del_button = MDRaisedButton(text="Continue", pos_hint={"right": 0.95}, on_release=self.del_acc_conclusion)
        box_layout.add_widget(self.acc_label)
        box_layout.add_widget(self.del_pass_input)
        box_layout.add_widget(self.confirm_del_button)
        self.acc_popup.add_widget(box_layout)
        self.acc_popup.open()
        
    def del_acc_conclusion(self, obj):
        if self.del_pass_input.text == self.password:
            try:
                # Remove user data from database
                db.child("users").child(current_user).remove(self.user_id_token)
            
                # Try deleting profile picture if it exists
                try:
                    storage.delete(f"profile_pictures/{current_user}", self.user_id_token)
                except Exception as e:
                    print("Profile picture not found or couldn't be deleted:", e)

                # Try deleting media files if they exist
                try:
                    storage.delete(f"media/{current_user}", self.user_id_token)
                except Exception as e:
                    print("Media files not found or couldn't be deleted:", e)
            
                # Delete user account
                auth.delete_user_account(self.user_id_token)
                self.notify("Account removal", "Account deleted successfully.")
                self.acc_popup.dismiss()
                self.switch_to_login()
            
            except Exception as e:
                print("Error during account removal:", e)
                self.notify("Account removal", "Error deleting account.")
                self.acc_popup.dismiss()
        else:
            self.del_pass_input.error = True
    
    def close_del_dialog(self, instance):
        self.del_acc_dialog.dismiss()
        
    def check_if_user_in_community(self):
        user_data = db.child("users").child(current_user).get(self.user_id_token).val()

        if not user_data.get("is_in_community", False):
            self.show_join_community_prompt()
        else:
            self.load_available_sections()
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
        db.child("users").child(current_user).update({"is_in_community": True}, self.user_id_token)
        self.close_dialog()
        toast("Successfully joined communities.")
        self.sm.current = "community"
        self.load_available_sections()

    def close_dialog(self):
            self.join_community_dialog.dismiss()

    def create_section(self, section_name):
        section_data = {
            "name": section_name,
            "created_by": current_user,
            "members": [current_user]
        }
        db.child("sections").push(section_data, self.user_id_token)

    def load_available_sections(self):
        sections = db.child("sections").get(self.user_id_token).val()
        section_list = self.sm.get_screen('community').ids.section_list
        section_list.clear_widgets()

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

        if current_user not in section_data['members']:
            self.join_section(section_id)
        else:
            self.switch_section(section_id)

    def join_section(self, section_id):
        section_data = db.child("sections").child(section_id).get(self.user_id_token).val()
        members = section_data.get('members', [])
        if current_user not in members:
            members.append(current_user)
            db.child("sections").child(section_id).update({"members": members}, self.user_id_token)
        self.switch_section(section_id)

    def load_messages(self, section_id):
        self.sm.get_screen("chat").ids.chat_area.clear_widgets()
        messages = db.child("sections").child(section_id).child("messages").get(self.user_id_token).val()
        if messages:
            for msg_id, msg_data in messages.items():
                self.display_message(msg_data)

    def display_message(self, msg_data):
        sender_id = msg_data['sender']
        sender_data = db.child("users").child(sender_id).get(self.user_id_token).val()

        sender_name = sender_data['username']
        sender_profile_pic = sender_data.get('photo_url', '')

        chat_screen = self.sm.get_screen('chat')
        chat_layout = chat_screen.ids.chat_area

        message_box = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height="80dp",
            md_bg_color=(0.1, 0.1, 0.3, 0.1),
            radius=(30, 30, 30, 30)
        )

        # Create a horizontal layout for avatar and sender name
        header_box = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height="40dp",
            md_bg_color=(0.05, 0.05, 0.15, 0.1)
        )

        # Add avatar (IconLeftWidget) to the header_box
        avatar = ImageLeftWidget(source=sender_profile_pic, radius=(100, 100, 100, 100), size_hint_x=0.15)
        header_box.add_widget(avatar)

        # Add sender name to the header_box
        sender_label = MDLabel(
            text=sender_name,
            halign="left",
            font_style="Subtitle1"  # You can adjust the font style if needed
        )
        header_box.add_widget(sender_label)

        # Add the header (avatar and name) to the message box
        message_box.add_widget(header_box)

        # Add the message text below the header
        message_text = MDLabel(
            text=msg_data['text'],
            color=(0.1, 0.1, 0.4, 0.9),
            halign="left",
            size_hint_y=None,
            height="40dp"
        )
        message_box.add_widget(message_text)

        # Add the message box to the chat layout
        chat_layout.add_widget(message_box)
    
    def send_message_to_current_section(self):
        if not self.current_section_id:
            return

        message_text = self.sm.get_screen("chat").ids.message_input.text.strip()
        if message_text == "":
            return

        message_data = {
            "sender": current_user,
            "text": message_text,
            "timestamp": self.get_current_time(),
        }

        db.child("sections").child(self.current_section_id).child("messages").push(message_data, self.user_id_token)
        self.sm.get_screen("chat").ids.message_input.text = ""
        self.load_messages(self.current_section_id)

    def switch_section(self, new_section_id):
        section_data = db.child("sections").child(new_section_id).get(self.user_id_token).val()
        self.current_section_id = new_section_id
        self.sm.current = "chat"
        self.sm.get_screen("chat").ids.chat_area.clear_widgets()
        self.sm.get_screen("chat").ids.section_name.text = f"{section_data['name']}"
        self.load_messages(self.current_section_id)

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
            self.create_section_dialog.dismiss()
            self.load_available_sections()
        else:
            self.create_section_dialog.content_cls.error = True
        
    def load_user_profile(self):
        user_data = db.child("users").child(current_user).get(self.user_id_token).val()
        profile_screen = self.sm.get_screen('profile')
        profile_screen.ids.profile_picture.source = user_data.get("photo_url", "")
        profile_screen.ids.followers.text = f"Followers: {len(user_data.get('followers', []))}"
        profile_screen.ids.following.text = f"Following: {len(user_data.get('following', []))}"
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
            db_user_data = db.child("users").child(current_user).get(self.user_id_token).val()
            new_username = profile_screen.ids.username_field.text
            new_bio = profile_screen.ids.bio_field.text
            new_pp = profile_screen.ids.profile_picture.source
            user_data = {
                "username": new_username,
                "bio": new_bio
            }
            if new_pp != db_user_data.get("photo_url", ""):
                image_filename = f"profile_pictures/{current_user}/{new_pp.split('/')[-1]}"
                storage.child(image_filename).put(self.image_path, self.user_id_token)
                image_url = storage.child(image_filename).get_url(self.user_id_token)
                user_data["photo_url"] = image_url
            db.child("users").child(current_user).update(user_data, self.user_id_token)
            print("Profile updated successfully.")
            self.notify("Profile Update", "Profile updated successfully.")
            
            # Exit edit mode
            self.toggle_edit_mode(False)

    def select_profile_picture(self):
        content = FileChooserIconView(filters=["*.jpeg", "*.jpg", "*.png", "*.webp"], size_hint=(1, 1))

        self.image_popup = Popup(title="Select Profile Picture", content=content, size_hint=(0.9, 0.9))
        content.bind(selection=self.on_picture_select)
        self.image_popup.open()
        
    def on_picture_select(self, instance, selection):
        if selection:
            self.image_path = selection[0]
            print("image selected: ", self.image_path)
            self.sm.get_screen("profile").ids.profile_picture.source = f"{self.image_path}"
            self.image_popup.dismiss()

    def show_medias(self):
        home_screen = self.sm.get_screen('home')
        box_layout = home_screen.ids.post_render
        box_layout.clear_widgets()
        the_posts = self.get_posts()
        post_renderer = PostRenderer(posts=the_posts, user_id_token=self.user_id_token)
        box_layout.add_widget(post_renderer)
        
    def add_post(self):
        self.post_box = ModalView(size_hint_y=None, height="250dp", auto_dismiss=True)
        box_layout = MDBoxLayout(orientation="vertical", md_bg_color=(1, 1, 1, 1))
        self.caption = MDTextField(hint_text="caption")
        layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height="50dp", spacing=10)
        add_image = MDIconButton(icon="image-plus", on_release=self.add_image)
        self.preview_image = AsyncImage(size_hint_x=0.5)
        layout.add_widget(add_image)
        layout.add_widget(self.preview_image)
        post_button = MDRaisedButton(text="Upload", on_release=self.upload_post)
        box_layout.add_widget(self.caption)
        box_layout.add_widget(layout)
        box_layout.add_widget(post_button)
        self.post_box.add_widget(box_layout)
        self.post_box.open()
        
    def add_image(self, instance):
        content = FileChooserIconView(filters=["*.jpeg", "*.jpg", "*.png", "*.webp"], size_hint=(1, 1))

        self.add_image_popup = Popup(title="Select Image", content=content, size_hint=(0.9, 0.9))
        content.bind(selection=self.on_image_select)
        self.add_image_popup.open()
        
    def on_image_select(self, instance, selection):
        if selection:
            self.post_image_path = selection[0]
            print("image selected: ", self.post_image_path)
            self.preview_image.source = self.post_image_path
            self.add_image_popup.dismiss()

    def watermark_image(self, file_path, upload_path):
        img = Image.open(file_path)
        img = Image.open(file_path)
        watermark_url = "https://firebasestorage.googleapis.com/v0/b/memerdevs.appspot.com/o/Default%2Fwatermark.png?alt=media&token=82c4bb6a-9562-4fa9-a121-739a83aa79f7"
        response = requests.get(watermark_url)
        watermark = Image.open(BytesIO(response.content))
        watermark.thumbnail((100, 100))
        x, y = 10, 10
        img.paste(watermark, (x, y), mask=watermark)
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        storage.child(upload_path).put(img_byte_arr, self.user_id_token)
        print(f"Image uploaded to Firebase Storage at path: {upload_path}")
            
    def upload_post(self, obj):
        post_text = self.caption.text
        media = self.post_image_path

        if not post_text and not media:
            self.notify("Post", "No content to post.")
        
        media_url = ""
        if media:
            media_path = f"media/{current_user}/{username}@MemerDevs-{datetime.utcnow()}{media.split('/')[-1]}"
            self.watermark_image(media, media_path)
            media_url = storage.child(media_path).get_url(self.user_id_token)
            print("Media uploaded, URL:", media_url)

        timestamp = str(datetime.utcnow())

        post_data = {
            "userId": current_user,
            "username": username,
            "text": post_text,
            "media_url": media_url,
            "likes": [],
            "comments": [],
            "timestamp": timestamp,
            "views": 0,
            "viewed_by": []
        }

        db.child("posts").push(post_data, self.user_id_token)
    
        self.notify("Post", "Post created successfully.")
        self.post_box.dismiss()

    def get_posts(self):
        all_posts = db.child("posts").get(self.user_id_token).val()
        followed_posts = []
        unfollowed_posts = []
        for post_id, post in all_posts.items():
            post["postId"] = post_id
            post_owner_id = post["userId"]
            post_owner = db.child("users").child(post_owner_id).get(self.user_id_token).val()
            if current_user in post_owner.get("following", []):
                followed_posts.append(post)
            else:
                unfollowed_posts.append(post)

        post_frequencies = {}
        for post in followed_posts:
            post_key = post["postId"]
            post_frequencies[post_key] = post_frequencies.get(post_key, 0) + 1
            
        sorted_followed_posts = sorted(followed_posts, key=lambda x: (post_frequencies.get(x["postId"], 0), x.get("timestamp", 0)), reverse=True)
        posts = sorted_followed_posts + unfollowed_posts

        for post in posts:
            post_key = post["postId"]
            self.increment_view_count(post_key)

        return posts

    def increment_view_count(self, post_key):
        post_data = db.child("posts").child(post_key).get(self.user_id_token).val()
    
        if post_data:
            viewed_by = post_data.get("viewed_by", [])
        
            if current_user not in viewed_by:
                current_views = post_data.get("views", 0)
                new_views = current_views + 1
                viewed_by.append(current_user)
                db.child("posts").child(post_key).update({
                    "views": new_views,
                "viewed_by": viewed_by
                }, self.user_id_token)
                print(f"View count updated for post {post_key}. Total views: {new_views}")
            else:
                print(f"User {current_user} has already viewed post {post_key}.")
        else:
            print(f"Post {post_key} does not exist.")
            
if __name__ == '__main__':
    MemerDevsApp().run()

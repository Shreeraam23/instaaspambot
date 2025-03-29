import logging
import getpass
import json
import os
from instagrapi import Client

def setup_logging():
    logging.basicConfig(
        filename="instagrapi_messages.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def save_session(cl, username):
    session_file = f"{username}_session.json"
    with open(session_file, "w") as f:
        json.dump(cl.get_settings(), f)
    logging.info("Session saved successfully.")

def load_session(cl, username):
    session_file = f"{username}_session.json"
    if os.path.exists(session_file):
        with open(session_file, "r") as f:
            settings = json.load(f)
        cl.set_settings(settings)
        try:
            cl.login(cl.username, cl.password)
            logging.info("Session restored successfully.")
            return True
        except Exception as e:
            logging.warning("Session restoration failed. Logging in again.")
            return False
    return False

def login():
    cl = Client()
    username = input("Enter your Instagram username: ")
    password = getpass.getpass("Enter your Instagram password: ")
    
    if load_session(cl, username):
        return cl
    
    try:
        cl.login(username, password)
        logging.info("Login successful.")
        save_session(cl, username)
        return cl
    except Exception as e:
        if "challenge_required" in str(e):
            logging.warning("2FA required.")
            two_factor_code = input("Enter your 2FA code: ")
            try:
                cl.two_factor_login(two_factor_code)
                logging.info("2FA verification successful.")
                save_session(cl, username)
                return cl
            except Exception as twofa_error:
                logging.error(f"2FA failed: {twofa_error}")
                print("2FA verification failed. Please try again.")
                return None
        else:
            logging.error(f"Login failed: {e}")
            print("Login failed. Please check your credentials.")
            return None

def send_messages(cl):
    choice = input("Send messages to a [1] User or [2] Group? (1/2): ")
    
    if choice == "1":
        target_usernames = input("Enter target Instagram usernames (comma-separated): ").split(",")
        recipients = []
        for username in target_usernames:
            try:
                user_id = cl.user_id_from_username(username.strip())
                logging.info(f"Retrieved user ID: {user_id} for {username.strip()}")
                recipients.append(user_id)
            except Exception as e:
                logging.error(f"Error retrieving user ID for {username.strip()}: {e}")
                print(f"Failed to retrieve user ID for {username.strip()}.")
    
    elif choice == "2":
        group_name = input("Enter the group name: ")
        try:
            groups = cl.direct_threads()
            group_id = None
            for thread in groups:
                if group_name in thread.title:
                    group_id = thread.id
                    break
            if not group_id:
                print("Group not found.")
                return
            logging.info(f"Retrieved group ID: {group_id} for {group_name}")
            recipients = [group_id]
        except Exception as e:
            logging.error(f"Error retrieving group ID: {e}")
            print("Failed to retrieve group ID.")
            return
    
    else:
        print("Invalid choice.")
        return
    
    messages = []
    print("Enter messages to send (type 'DONE' to finish):")
    while True:
        msg = input()
        if msg.upper() == "DONE":
            break
        messages.append(msg)
    
    print("Messages to be sent:")
    for msg in messages:
        print(f"- {msg}")
    confirm = input("Do you want to send these messages? (yes/no): ").lower()
    if confirm != "yes":
        print("Message sending cancelled.")
        return
    while True:
        for msg in messages:
            try:
                cl.direct_send(msg, recipients)
                print(f"Sent: {msg}")
                logging.info(f"Sent message: {msg}")
            except Exception as e:
                logging.error(f"Failed to send message: {e}")
                print(f"Failed to send: {msg}")
def main():
    setup_logging()
    cl = login()
    if not cl:
        return
    send_messages(cl)
    print("Messages sent successfully!")
    cl.logout()

if __name__ == "__main__":
    main()

import logging
import getpass
from instagrapi import Client

def setup_logging():
    logging.basicConfig(
        filename="instagrapi_messages.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def login():
    cl = Client()
    username = input("Enter your Instagram username: ")
    password = getpass.getpass("Enter your Instagram password: ")
    try:
        cl.login(username, password)
        logging.info("Login successful.")
        return cl
    except Exception as e:
        if "challenge_required" in str(e):
            logging.warning("2FA required.")
            two_factor_code = input("Enter your 2FA code: ")
            try:
                cl.two_factor_login(two_factor_code)
                logging.info("2FA verification successful.")
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
        target_username = input("Enter the target's Instagram username: ")
        try:
            user_id = cl.user_id_from_username(target_username)
            logging.info(f"Retrieved user ID: {user_id} for {target_username}")
        except Exception as e:
            logging.error(f"Error retrieving user ID: {e}")
            print("Failed to retrieve user ID.")
            return
        recipient = [user_id]
    
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
        except Exception as e:
            logging.error(f"Error retrieving group ID: {e}")
            print("Failed to retrieve group ID.")
            return
        recipient = [group_id]
    
    else:
        print("Invalid choice.")
        return
    
    messages = [
        "msg 1", "msg 2", "msg 3", "msg 4", "add more msgs here"
    ]
    while True:
        for msg in messages:
            try:
                cl.direct_send(msg, recipient)
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
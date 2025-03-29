import os
# import time
import logging
from getpass import getpass
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired,
    ChallengeRequired,
    TwoFactorRequired,
    ClientError,
    ClientConnectionError
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_message_sender.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def setup_client():
    """Initialize and configure the Instagram client"""
    client = Client()
    client.delay_range = [1, 3]  # Random delay between 1-3 seconds for actions
    return client

def login_user(client, username, password, verification_code=None):
    """Handle Instagram login with potential 2FA"""
    try:
        logger.info(f"Attempting to login as {username}")
        
        if verification_code:
            client.login(username, password, verification_code=verification_code)
        else:
            client.login(username, password)
            
        logger.info("Login successful!")
        return True
    except TwoFactorRequired:
        logger.warning("Two-factor authentication required")
        verification_code = input("Enter your 2FA verification code: ")
        return login_user(client, username, password, verification_code)
    except ChallengeRequired:
        logger.error("Challenge required. Instagram may require additional verification.")
        # Here you could implement challenge resolution logic
        return False
    except LoginRequired:
        logger.error("Login failed. Please check your credentials.")
        return False
    except Exception as e:
        logger.error(f"An error occurred during login: {str(e)}")
        return False

def get_target_info(client):
    """Get target user or group information"""
    print("\nChoose where to send messages:")
    print("1. Send to a user")
    print("2. Send to a group")
    
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == "1":
        target_username = input("Enter target username: ")
        try:
            user_id = client.user_id_from_username(target_username)
            logger.info(f"Found user ID: {user_id} for username: {target_username}")
            return [user_id], f"user {target_username}"
        except Exception as e:
            logger.error(f"Error finding user: {str(e)}")
            return None, None
    elif choice == "2":
        print("\nNote: For groups, you need the thread ID which can be found in the group's URL.")
        thread_id = input("Enter group thread ID: ")
        return [thread_id], f"group with ID {thread_id}"
    else:
        logger.error("Invalid choice")
        return None, None

def send_messages(client, recipient_ids, messages, target_description):
    """Send multiple messages with error handling"""
    if not messages:
        logger.error("No messages to send")
        return False
    
    logger.info(f"Preparing to send {len(messages)} messages to {target_description}")
    
    success_count = 0
    for i, msg in enumerate(messages, 1):
        try:
            logger.debug(f"Sending message {i}/{len(messages)}: {msg[:20]}...")
            client.direct_send(msg, recipient_ids)
            logger.info(f"Sent message {i}: {msg[:20]}...")
            success_count += 1
            # time.sleep(1)  # Add delay between messages
        except ClientError as e:
            logger.error(f"Failed to send message {i}: {str(e)}")
        except ClientConnectionError as e:
            logger.error(f"Connection error on message {i}: {str(e)}")
            # Implement retry logic here if desired
        except Exception as e:
            logger.error(f"Unexpected error sending message {i}: {str(e)}")
    
    logger.info(f"Message sending complete. Successfully sent {success_count}/{len(messages)} messages")
    return success_count > 0

def get_messages_to_send():
    """Get messages from user input"""
    print("\nEnter the messages you want to send (type 'DONE' on a new line when finished):")
    messages = []
    while True:
        msg = input("> ")
        if msg.upper() == "DONE":
            break
        if msg.strip():
            messages.append(msg)
    
    if not messages:
        logger.warning("No messages entered")
        return None
    
    logger.info(f"Prepared {len(messages)} messages to send")
    return messages

def main():
    print("Instagram Multiple Message Sender")
    print("--------------------------------")
    
    # Get user credentials
    username = input("Enter your Instagram username: ")
    password = getpass("Enter your Instagram password: ")
    
    # Initialize client
    client = setup_client()
    
    # Login
    if not login_user(client, username, password):
        logger.error("Unable to proceed without successful login")
        return
    
    # Get target info
    recipient_ids, target_description = get_target_info(client)
    if not recipient_ids:
        logger.error("Invalid target selection")
        return
    
    # Get messages
    messages = get_messages_to_send()
    if not messages:
        return
    
    # Confirm before sending
    print(f"\nAbout to send {len(messages)} messages to {target_description}")
    confirm = input("Are you sure you want to proceed? (yes/no): ")
    if confirm.lower() != "yes":
        logger.info("Message sending cancelled")
        return
    
    # Send messages
    send_messages(client, recipient_ids, messages, target_description)
    
    logger.info("Script completed")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
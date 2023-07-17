import os

import pandas as pd
from chatbot.mongo_database.mongo_database_manager import MongoDatabaseManager
from dotenv import load_dotenv

if __name__ == '__main__':
    mongo_database = MongoDatabaseManager()
    student_profile_collection = mongo_database.get_collection('student_profiles')
    load_dotenv()
    student_usernames = student_profile_collection.distinct('student_username')
    username_email_dict = os.getenv('STUDENT_USER_NAMES_AND_EMAIL')

    student_info = pd.read_csv('../../student_info.csv')
    for student_username in student_usernames:
        student_profile_collection.update_one(
            {'student_username': student_username},
            {'$set': {'student_email': username_email_dict[student_username]}}
        )

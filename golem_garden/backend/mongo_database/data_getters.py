from typing import Dict

from chatbot.mongo_database.mongo_database_manager import MongoDatabaseManager
from chatbot.student_info.student_profiles.student_profile_models import StudentProfile


async def get_student_profiles() -> Dict[str, StudentProfile]:
    mongo_database_manager = MongoDatabaseManager()
    collection = mongo_database_manager.get_collection(collection_name="student_profiles")
    profile_list = await collection.find().to_list(length=None)
    student_profiles = {profile["initials"]: StudentProfile(**profile) for profile in profile_list}

    to_delete = []
    for student_id in student_profiles.keys():
        if len(student_id) == 1:
            to_delete.append(student_id)
    for student_id in to_delete:
        del student_profiles[student_id]
    return student_profiles

import logging

from chatbot.mongo_database.mongo_database_manager import MongoDatabaseManager
from chatbot.system.filenames_and_paths import get_thread_backups_collection_name

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def grab_green_check_messages(server_name: str,
                                    all_thread_collection_name: str = None,
                                    overwrite: bool = False,
                                    save_to_json: bool = True,
                                    collection_name: str = "green_check_messages"):
    mongo_database = MongoDatabaseManager()
    if all_thread_collection_name is None:
        all_thread_collection_name = get_thread_backups_collection_name(server_name=server_name)

    all_thread_collection = mongo_database.get_collection(all_thread_collection_name)
    all_threads = await all_thread_collection.find().to_list(length=None)

    total_cost = 0
    for thread_entry in all_threads:

        if not thread_entry["thread_statistics"]["green_check_emoji_present"]:
            continue

        print("=====================================================================================================")
        print("=====================================================================================================")
        print(
            f"Thread: {thread_entry['thread_title']}, Channel: {thread_entry['channel']}, Created at: {thread_entry['created_at']}")
        print(f"{thread_entry['thread_url']}")
        query = {"_student_initials": thread_entry["_student_initials"],
                 "_student_uuid": thread_entry["_student_uuid"],
                 "thread_id": int(thread_entry["thread_id"]),
                 "thread_url": thread_entry["thread_url"],
                 "channel": thread_entry["channel"], }

        messages_with_green_check = []
        for message in thread_entry["messages"]:
            if len(message["reactions"]) > 0:
                if any([reaction == "✅" for reaction in message["reactions"]]):
                    messages_with_green_check.append(message["content"])

                    await mongo_database.upsert(
                        collection=collection_name,
                        query=query,
                        data={"$addToSet": {"green_check_messages": message["content"]}}
                    )
        print(f"Student: {thread_entry['_student_name']}: \n"
              f"Messages with green check: {messages_with_green_check}")

    if save_to_json:
        await mongo_database.save_json(collection_name=collection_name)


if __name__ == "__main__":
    import asyncio

    asyncio.run(grab_green_check_messages(server_name="Neural Control of Real World Human Movement 2023 Summer1",
                                          overwrite=True,
                                          save_to_json=True,
                                          ))

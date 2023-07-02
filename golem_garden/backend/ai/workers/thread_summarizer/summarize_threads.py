import logging
from datetime import datetime

from chatbot.ai.workers.thread_summarizer.split_thread_data_into_chunks import split_thread_data_into_chunks
from chatbot.ai.workers.thread_summarizer.thread_summarizer import logger, ThreadSummarizer
from chatbot.mongo_database.mongo_database_manager import MongoDatabaseManager
from chatbot.student_info.load_student_info import load_student_info
from chatbot.system.filenames_and_paths import get_thread_backups_collection_name

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def summarize_threads(server_name: str,
                            all_thread_collection_name: str = None,
                            overwrite: bool = False,
                            save_to_json: bool = True,
                            channel_name: str = None, ):
    mongo_database = MongoDatabaseManager()
    if all_thread_collection_name is None:
        all_thread_collection_name = get_thread_backups_collection_name(server_name=server_name)
    all_thread_collection = mongo_database.get_collection(all_thread_collection_name)

    student_info = load_student_info()

    logger.info("Generating thread summary")
    total_cost = 0

    all_threads = await all_thread_collection.find().to_list(length=None)
    number_of_threads = len(all_threads)
    for thread_number, thread_entry in enumerate(all_threads):

        if channel_name is not None and thread_entry["channel"] != channel_name:
            logger.info(
                f"Skipping thread: `{thread_entry['thread_title']}` created at {str(thread_entry['created_at'])} because it is not in channel: {channel_name}")
            continue

        print("=====================================================================================================")
        print(
            f"Thread: {thread_entry['thread_title']}, Channel: {thread_entry['channel']}, Created at: {thread_entry['created_at']}")
        print(f"{thread_entry['thread_url']}")
        print(f"Thread number: {thread_number + 1} of {number_of_threads}")
        print("=====================================================================================================")

        if "summary" in thread_entry and not overwrite:
            logger.info(
                f"Thread summary already exists, skipping thread: `{thread_entry['thread_title']}` created at {str(thread_entry['created_at'])}")
            continue

        logger.info(f"Summarizing: `{thread_entry['thread_title']}` created at {str(thread_entry['created_at'])}")

        thread_chunks = split_thread_data_into_chunks(messages=thread_entry["thread_as_list_of_strings"])

        try:
            thread_summarizer = ThreadSummarizer(use_anthropic=True)
            thread_summary = await thread_summarizer.summarize(thread_chunks=thread_chunks)
        except Exception as e:
            logger.error(f"Summary generation failed with error: {e}. Trying again with OpenAI API")
            thread_summarizer = ThreadSummarizer(use_anthropic=False)
            thread_summary = await thread_summarizer.summarize(thread_chunks=thread_chunks)

        # logger.info(f"Saving thread summary to mongo database, summary: {thread_summary}")
        thread_cost = 0
        for chunk in thread_chunks:
            thread_cost += chunk["token_count"] * thread_summarizer.dollars_per_token
        total_cost += thread_cost

        await mongo_database.upsert(
            collection=get_thread_backups_collection_name(server_name=server_name),
            query={"_id": thread_entry["_id"]},
            data={
                "$set": {
                    "summary": {"summary": thread_summary["output_text"],
                                "intermediate_steps": thread_summary["intermediate_steps"],
                                "thread_chunks": thread_chunks,
                                "cost": thread_cost,
                                "model": thread_summarizer.llm_model,
                                "created_at": datetime.now().isoformat(),
                                }
                }
            }
        )
        print(f"Thread summary: {thread_summary['output_text']}\n"
              f"Thread summary cost: ${thread_cost:.5f}\n"
              f"Total cost (so far): ${total_cost:.5f}\n"
              f"----------------------------\n")


    print(f"Done summarizing threads!\n\n Total estimated cost (final): ${total_cost:.2f}\n\n")
    if save_to_json:
        await mongo_database.save_json(collection_name=all_thread_collection_name)


if __name__ == "__main__":
    import asyncio

    # asyncio.run(summarize_threads(server_name="Neural Control of Real World Human Movement 2023 Summer1",
    #                               overwrite=True,
    #                               save_to_json=True,
    #                               channel_name="video-chatter-bot"))
    # asyncio.run(summarize_threads(server_name="Neural Control of Real World Human Movement 2023 Summer1",
    #                               overwrite=True,
    #                               save_to_json=True,
    #                               ))
    asyncio.run(summarize_threads(server_name="Neural Control of Real World Human Movement 2023 Summer1",
                                  all_thread_collection_name="thread_backups_for_Neural_Control_of_Real_World_Human_Movement_2023_Summer1",
                                  overwrite=True,
                                  save_to_json=True,
                                  ))

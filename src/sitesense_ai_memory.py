#
# Description: Source code for the chat memory for Site Sense AI
# Author: Alexander Powell
# Version: v1.0
# Dependencies: N/A
#


class SiteSenseAIMemory:
    def __init__(self):
        self.chat_history: list = []

    def append(self, chat_messages: str):
        """
        Appends the chat message to the chat history for memory context.

        :param chat_messages:
        :return:
        """
        if len(self.chat_history) > 10:
            self.remove()

        self.chat_history.append(chat_messages)

    def remove(self):
        """
        Removes the oldest item from the chat history.

        :return:
        """
        self.chat_history.pop(0)

    def get_chat_history(self):
        return "".join(self.chat_history)

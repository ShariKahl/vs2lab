from phone_book_entry import PhoneBookEntry
from typing import List

class PhoneBookController:
    _entries: List[PhoneBookEntry] = [
        {
            "name": "John Doe",
            "phone_number": "1234567890",
            "city": "New York"
        },
        {
            "name": "Jane Doe",
            "phone_number": "0987654321",
            "city": "Los Angeles"
        }
    ]

    def addEntry(self, entry):
        self._entries.append(entry)

    def getEntry(self, query: str) -> List[PhoneBookEntry]:
        query = query.lower()

        return [
            entry for entry in self._entries
            if query in entry["name"].lower() or
               query in entry["phone_number"].lower() or
               query in entry["city"].lower()
        ]

    def getAllEntries(self):
        return self._entries

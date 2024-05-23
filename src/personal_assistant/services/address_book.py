from collections import UserDict

class AddressBook(UserDict):
    # Ініціалізація класу AddressBook. Створює порожній список контактів та об'єкт TagManager для управління тегами
    def __init__(self):
        self.contacts = []
        self.next_id = 1
        self.tag_manager = TagManager()

    # Метод додає новий контакт до адресної книги.
    def add_contact(self, contact: Contact):
        contact.contact_id = self.next_id
        self.contacts.append(contact)
        self.tag_manager.add_tags(contact.contact_id, contact.tags)
        self.next_id += 1

    # Метод видаляє контакт за унікальним ID, включаючи очищення асоційованих тегів через TagManager.
    def remove_contact(self, contact_id: int):
        contact = self.contacts.pop(contact_id, None)
        if contact:
            self.tag_manager.remove_tags(contact_id, contact.tags)
    
        
    # Метод видаляє контакт за унікальним ID або переданими атрибутами(ім'я, телефон, email), включаючи очищення асоційованих тегів через TagManager.
    def remove_contact(self, contact_id: int = None, name: str = None, phone: str = None, email: str = None):  
        if contact_id is None:
            for cid, contact in self.contacts.items():
                if name and contact.name == name:
                    contact_id = cid
                    break
                if phone and contact.phone == phone:
                    contact_id = cid
                    break
                if email and contact.email == email:
                    contact_id = cid
                    break

        removed_contact = self.contacts.pop(contact_id, None)
        if removed_contact is None:
            print(f"Contact not found.")
        else:
            print(f"Contact has been deleted.")
            self.tag_manager.remove_tags(contact_id, contact.tags)
        

    # Метод оновлює атрибути контакту згідно переданих аргументів.
    # contact_id: Унікальний ідентифікатор контакту, який оновлюється.
    # kwargs: Словник параметрів, які потрібно оновити.
    def update_contact(self, contact_id: int, **kwargs):
        contact = self.find_by_id(contact_id)
        if contact:
            old_tags = contact.tags.copy()
            contact.update(**kwargs)
            self.tag_manager.remove_tags(contact_id, old_tags)
            self.tag_manager.add_tags(contact_id, contact.tags)

    # Метод знахидить контакт за унікальним ID.
    def find_by_id(self, contact_id: int) -> Contact:
        return next((contact for contact in self.contacts if contact.contact_id == contact_id), None)
    
    # Метод виконує гнучкий пошук контактів за вказаними критеріями.
    # search_query: Рядок пошукового запиту.
    # return: Список об'єктів Contact, які відповідають пошуковому запиту.
    def find(self, search_query: str) -> List[Contact]:
        search_query = search_query.lower()
        results = []
        for contact in self.contacts:
            if (search_query in contact.name.lower() or
                search_query in contact.phone.lower() or
                search_query in contact.email.lower() or
                search_query in contact.address.lower() or
                any(search_query in tag.lower() for tag in contact.tags)):
                results.append(contact)
        return results
        
    
    # Метод серіалізує всі контакти у JSON формат для зберігання. 
    # Повертає рядок у форматі JSON, який представляє всі контакти.
    def serialize(self) -> str:
        contacts_data = [contact.to_dict() for contact in self.contacts]
        return json.dumps(contacts_data, indent=4)

    # Метод відновлює стан AddressBook з серіалізованих даних.
    # json_data: Рядок у форматі JSON, який представляє серіалізовані контакти.
    def deserialize(self, json_data: str):
        contacts_data = json.loads(json_data)
        self.contacts = [Contact.from_dict(data) for data in contacts_data]
        self.next_id = max(contact.contact_id for contact in self.contacts) + 1 if self.contacts else 1
        for contact in self.contacts:
            self.tag_manager.add_tags(contact.contact_id, contact.tags)

    # Повертає рядкове представлення всіх контактів у адресній книзі.
    def __str__(self):
        return '\n'.join(str(contact) for contact in self.contacts.values())


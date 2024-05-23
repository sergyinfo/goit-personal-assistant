

class AddressBook:
    # Ініціалізація класу AddressBook. Створює порожній список контактів та об'єкт TagManager для управління тегами
    def __init__(self):
        self.contacts = {}
        self.next_id = 1
        self.tag_manager = TagManager()

    # Метод додає новий контакт до адресної книги.
    def add_contact(self, contact):
        if isinstance(contact, Contact):
            contact.contact_id = self.next_id
            self.contacts[self.next_id] = contact
            self.tag_manager.add_tags(contact.contact_id, contact.tags)
            self.next_id += 1
        else:
            print("Invalid contact type. Please provide an instance of Contact.")

    # Метод видаляє контакт за унікальним ID або переданим атрибутом, включаючи очищення асоційованих тегів через TagManager.
    def remove_contact(self, contact_id=None, name=None, phone=None, email=None):
        contact_id = contact_id or self._find_contact_id(name, phone, email)
        if contact_id in self.contacts:
            removed_contact = self.contacts.pop(contact_id)
            self.tag_manager.remove_tags(contact_id, removed_contact.tags)
            print("Contact has been deleted.")
        else:
            print("Contact not found.")
    
    # Метод здійснює пошук ID контакту за наданим ім'ям, телефоном або email.
    def _find_contact_id(self, name=None, phone=None, email=None):
        for cid, contact in self.contacts.items():
            if (name and contact.name == name) or (phone and contact.phone == phone) or (email and contact.email == email):
                return cid
        return None

    # Метод оновлює атрибути контакту згідно переданих аргументів, враховуючи старі теги при оновленні контакту
    # contact_id: Унікальний ідентифікатор контакту, який оновлюється.
    # kwargs: Словник параметрів, які потрібно оновити.
    def update_contact(self, contact_id, **kwargs):
        contact = self.contacts.get(contact_id)
        if contact:
            old_tags = contact.tags.copy()
            contact.update(**kwargs)
            self.tag_manager.remove_tags(contact_id, old_tags)
            self.tag_manager.add_tags(contact_id, contact.tags)


    # Метод знахидить контакт за унікальним ID.
    def find_by_id(self, contact_id):
        return self.contacts.get(contact_id)
    
    # Метод виконує гнучкий пошук контактів за вказаними критеріями.
    # search_query: Рядок пошукового запиту.
    # return: Список об'єктів Contact, які відповідають пошуковому запиту.
    def find(self, search_query):
        search_query = search_query.lower()
        results = []
        for contact in self.contacts.values():
            if (search_query in contact.name.lower() or
                    search_query in contact.phone.lower() or
                    search_query in contact.email.lower() or
                    search_query in contact.address.lower() or
                    any(search_query in tag.lower() for tag in contact.tags)):
                results.append(contact)
        return results
        
    
    # Метод серіалізує всі контакти у JSON формат для зберігання. 
    # Повертає рядок у форматі JSON, який представляє всі контакти.
    def serialize(self):
        contacts_data = [contact.to_dict() for contact in self.contacts.values()]
        return json.dumps(contacts_data, indent=4)

    # Метод відновлює стан AddressBook з серіалізованих даних.
    # json_data: Рядок у форматі JSON, який представляє серіалізовані контакти.
    def deserialize(self, json_data):
        contacts_data = json.loads(json_data)
        self.contacts = {data['contact_id']: Contact.from_dict(data) for data in contacts_data}
        self.next_id = max(self.contacts.keys()) + 1 if self.contacts else 1
        for contact in self.contacts.values():
            self.tag_manager.add_tags(contact.contact_id, contact.tags)

    # Повертає рядкове представлення всіх контактів у адресній книзі.
    def __str__(self):
        return '\n'.join(str(contact) for contact in self.contacts.values())


class Doctor:
    name: str
    role: str
    image: str
    link: str
    def __init__(self, data: dict):
        self.name = data.get("name", "")
        self.role = data.get("role", "")
        self.image = f'www.clevelandclinicabudhabi.ae/${data.get("image", "")}'
        self.link = f'www.clevelandclinicabudhabi.ae{data.get("link", "")}'

    def __str__(self):
        return f"Doctor(\n\tname={self.name},\n\trole={self.role},\n\timage={self.image},\n\tlink={self.link})\n"
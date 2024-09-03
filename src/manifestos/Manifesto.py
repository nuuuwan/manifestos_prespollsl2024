import os
from dataclasses import dataclass


@dataclass
class Manifesto:
    file_name: str

    DIR_PDF = os.path.join('data', 'pdf-original')
    DIR_PDF_UNIX = DIR_PDF.replace('\\', '/')

    @property
    def readme_line(self):
        return f'* [{self.lang}]({self.DIR_PDF_UNIX}/{self.file_name})'


    @property 
    def lang_code(self):
        return self.file_name.split('.')[0].split('-')[-1]
    
    @property
    def lang(self):
        return {
            'en': 'English',
            'si': 'සිංහල',
            'ta': 'தமிழ்',
        }.get(self.lang_code, self.lang_code)
    
    @property
    def party_code(self):
        return '-'.join(self.file_name.split('.')[0].split('-')[:-1])  
    
    @property 
    def party(self):
        return {
            'ind-rw': 'Ranil Wickremesinghe (Independent)',
            'npp': 'Anura Kumara Dissanayake (National People\'s Power)',
            'slpp': 'Namal Rajapakse (Sri Lanka Podujana Peramuna)',
            'sjb': 'Sajith Premadasa (Samagi Jana Balawegaya)',
            'mjp': 'Dilith Jayaweera (Sarvajana Balaya)',
        }.get(self.party_code, self.party_code)
    
    @classmethod
    def list_all(cls) -> list['Manifesto']:
        manifesto_list = []
        for file_name in os.listdir(Manifesto.DIR_PDF):
            if not file_name.endswith('.pdf'):
                continue
            manifesto_list.append(Manifesto(file_name))
        return manifesto_list

    @classmethod
    def list_by_party(cls) -> dict:
        manifesto_list = cls.list_all()
        idx = {}
        for manifesto in manifesto_list:
            party_code = manifesto.party_code
            if party_code not in idx:
                idx[party_code] = []
            idx[party_code].append(manifesto)
        return idx
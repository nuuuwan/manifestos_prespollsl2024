import os
from dataclasses import dataclass
from functools import cached_property

from utils import JSONFile


@dataclass
class Manifesto:
    file_name: str

    DIR_PDF = os.path.join('data', 'pdf')
    DIR_PDF_UNIX = DIR_PDF.replace('\\', '/')
    METADATA_PATH = os.path.join('data', 'metadata.json')

    @cached_property
    def id(self):
        return '.'.join(self.file_name.split('.')[:-1])

    @cached_property
    def lang_code(self):
        return self.id.split('-')[-1]

    @cached_property
    def lang(self):
        return {
            'en': 'English',
            'si': 'සිංහල',
            'ta': 'தமிழ்',
        }.get(self.lang_code, self.lang_code)

    @cached_property
    def party_code(self):
        return '-'.join(self.id.split('-')[:-1])

    @cached_property
    def party(self):
        return {
            'ind-rw': 'Ranil Wickremesinghe (Independent)',
            'npp': 'Anura Kumara Dissanayake (National People\'s Power)',
            'slpp': 'Namal Rajapakse (Sri Lanka Podujana Peramuna)',
            'sjb': 'Sajith Premadasa (Samagi Jana Balawegaya)',
            'mjp': 'Dilith Jayaweera (Sarvajana Balaya)',
        }.get(self.party_code, self.party_code)

    @cached_property
    def file_path(self):
        return os.path.join(self.DIR_PDF, self.file_name)

    @cached_property
    def file_size(self):
        return os.path.getsize(self.file_path)

    @cached_property
    def n_pages(self):
        from PyPDF2 import PdfFileReader

        with open(self.file_path, 'rb') as f:
            pdf = PdfFileReader(f)
            return pdf.getNumPages()

    # metadata.json
    @staticmethod
    def metadata_idx():
        return JSONFile(Manifesto.METADATA_PATH).read()

    @property
    def source(self):
        return self.metadata_idx()[self.id]['source']

    # README
    @cached_property
    def readme_line_label(self):
        return f'{self.lang} ({self.n_pages} Pages, {self.file_size / 1_000_000:.1f}MB)'

    @cached_property
    def readme_line(self):
        return f'* [{self.readme_line_label}]({self.DIR_PDF_UNIX}/{self.file_name}) - [Original Source]({self.source})'

    # Loaders
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

import os
from dataclasses import dataclass
from functools import cached_property

import matplotlib.pyplot as plt
from utils import File, JSONFile, Log
from wordcloud import WordCloud

from utils_future import Color

log = Log('Manifesto')


def clean(x):
    x = '\n'.join([line.strip() for line in x.split('\n')])
    while ' ' * 2 in x:
        x = x.replace(' ' * 2, ' ')
    while '\n' * 3 in x:
        x = x.replace('\n' * 3, '\n' * 2)
    return x


@dataclass
class Manifesto:
    file_name: str

    DIR_PDF = os.path.join('data', 'pdf')
    METADATA_PATH = os.path.join('data', 'metadata.json')
    URL_BASE = (
        'https://raw.githubusercontent.com/nuuuwan'
        + '/manifestos_prespollsl2024/main/data/pdf'
    )

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

    # PDF
    @cached_property
    def n_pages(self):
        from PyPDF2 import PdfFileReader

        with open(self.file_path, 'rb') as f:
            pdf = PdfFileReader(f)
            return pdf.getNumPages()

    # PDF-Text

    @cached_property
    def content_nocache(self):
        from PyPDF2 import PdfFileReader

        with open(self.file_path, 'rb') as f:
            pdf = PdfFileReader(f)
            text = ''
            for i in range(pdf.getNumPages()):
                text += pdf.getPage(i).extract_text()

            text = clean(text)
            return text

    @cached_property
    def txt_path(self):
        return os.path.join('data', 'txt', f'{self.id}.txt')

    @cached_property
    def txt_path_unix(self):
        return self.txt_path.replace('\\', '/')

    @cached_property
    def content(self):
        txt_file = File(self.txt_path)
        if txt_file.exists:
            return txt_file.read()
        content = self.content_nocache
        txt_file.write(content)
        log.info(f'Wrote {self.txt_path}')
        return content

    @cached_property
    def content_ascii(self):
        return ''.join([c if ord(c) < 128 else ' ' for c in self.content])

    @cached_property
    def words(self):
        return self.content.split()

    @cached_property
    def n_words(self):
        return len(self.words)

    # metadata.json
    @staticmethod
    def metadata_idx():
        return JSONFile(Manifesto.METADATA_PATH).read()

    @property
    def source(self):
        return self.metadata_idx()[self.id]['source']

    # Wordcloud
    @cached_property
    def wordcloud_path(self):
        return os.path.join('data', 'wordclouds', f'{self.id}.png')

    @cached_property
    def wordcloud_path_unix(self):
        return self.wordcloud_path.replace('\\', '/')

    def build_wordcloud(self):
        if self.n_words == 0 or self.lang_code != 'en':
            return None
        if os.path.exists(self.wordcloud_path):
            return self.wordcloud_path

        plt.close()
        wc = WordCloud(
            background_color="white",
            repeat=True,
            width=1600,
            height=900,
        )
        wc.generate(self.content_ascii)
        wc.recolor(color_func=Color.lk)

        plt.figure()
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.gcf().set_size_inches(4, 6)

        plt.savefig(self.wordcloud_path, dpi=150, bbox_inches='tight')
        log.info(f"Wrote {self.wordcloud_path}.")
        return self.wordcloud_path

    # README
    @cached_property
    def n_words_str(self):
        if self.n_words == 0:
            return 'Images Only'
        return f'{self.n_words / 1000:.1f}K Words'

    @cached_property
    def readme_line_label(self):
        return (
            f'{self.lang} ('
            + ', '.join(
                [
                    f'{self.n_pages} Pages',
                    f'{self.n_words_str}',
                    f'{self.file_size / 1_000_000:.1f}MB',
                ]
            )
            + ')'
        )

    @cached_property
    def pdf_url(self):
        return f'{self.URL_BASE}/{self.file_name}'

    @cached_property
    def pdf_link(self):
        return f'[{self.readme_line_label}]({self.pdf_url})'

    @cached_property
    def source_link(self):
        return f'[Original Source]({self.source})'

    @cached_property
    def raw_text_link(self):
        if not os.path.exists(self.txt_path):
            return None
        return f'[Raw Text]({self.txt_path_unix})'

    @cached_property
    def wordcloud_link(self):
        if not os.path.exists(self.wordcloud_path):
            return None
        return f'[Wordcloud]({self.wordcloud_path_unix})'

    @cached_property
    def summary_path(self):
        return os.path.join('data', 'summary', f'{self.id}.md')

    @cached_property
    def summary_path_unix(self):
        return self.summary_path.replace('\\', '/')

    @cached_property
    def summary_link(self):
        if not os.path.exists(self.summary_path):
            return None
        return (
            f'[Summary]({self.summary_path_unix})'
        )

    @cached_property
    def readme_line(self):
        self.build_wordcloud()
        return f'* ' + ' · '.join(
            [
                f'{x}'
                for x in [
                    self.pdf_link,
                    self.source_link,
                ]
                if x
            ]
        )

    @cached_property
    def render_wordcloud_lines(self):
        if not os.path.exists(self.wordcloud_path):
            return None
        return [
            '',
            '### Wordcloud',
            '',
            '*Based on English version text*',
            '',
            f'![{self.id} Wordcloud]({self.wordcloud_path_unix})',
            '',
        ]

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

    # Static README
    @staticmethod
    def get_readme_lines():
        lines = []
        for manifesto_list in Manifesto.list_by_party().values():
            first_manifesto = manifesto_list[0]
            lines.extend(['', f'## {first_manifesto.party}', ''])

            if first_manifesto.summary_link:
                lines.extend(['', first_manifesto.summary_link, ''])
            for manifesto in manifesto_list:
                lines.append(manifesto.readme_line)

            if first_manifesto.render_wordcloud_lines:
                lines.extend(first_manifesto.render_wordcloud_lines)
        return lines

from utils import File, Log

from manifestos.Manifesto import Manifesto

log = Log('ReadMe')


class ReadMe:
    PATH = 'README.md'

    def get_manifesto_lines(self):
        lines = []
        for manifesto_list in Manifesto.list_by_party().values():
            lines.extend(['', f'## {manifesto_list[0].party}', ''])
            for manifesto in manifesto_list:
                lines.append(manifesto.readme_line)
        return lines

    def build(self):
        lines = (
            [
                '# 2024 Sri Lankan Presidential Election Manifestos '
                + '(manifestos_prespollsl2024)',
                '',
                'This repository contains the manifestos '+'I could find online thus far. ',
                '',
                '📦 Where possible, images in the original source PDFs have been '
                + 'compressed.',
                '',
                '⚠️ Word counts are approximate and may not be accurate, especially for '
                + 'non-English text.',
            ]
            + self.get_manifesto_lines()
            + [
                '',
                'Note: The English Version of Namal Rajapakse\'s Manifesto '
                + 'is available as HTML at [www.nr.lk](https://www.nr.lk/manifesto).',
            ]
        )

        File(self.PATH).write_lines(lines)
        log.info(f'Wrote {self.PATH}')

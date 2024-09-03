from utils import File, Log, Time, TimeFormat

from manifestos.Manifesto import Manifesto

log = Log('ReadMe')


class ReadMe:
    PATH = 'README.md'



    def build(self):
        time_str = TimeFormat.TIME.format(Time.now())
        lines = (
            [
                '# 2024 Sri Lankan Presidential Election Manifestos '
                + '(manifestos_prespollsl2024)',
                '',
                'This repository contains the manifestos '
                + f'I could find as of **{time_str}**.',
            ]
            + Manifesto.get_readme_lines()
            + [
                '',
                '📦 Where possible, images in the original source PDFs have been '
                + 'compressed.',
                '',
                '⚠️ Word counts are approximate and may not be accurate, especially for '
                + 'non-English text.',
            ]
        )

        File(self.PATH).write_lines(lines)
        log.info(f'Wrote {self.PATH}')

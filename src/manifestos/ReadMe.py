from utils import File, Log, Time, TimeFormat

from manifestos.Manifesto import Manifesto

log = Log('ReadMe')


class ReadMe:
    PATH = 'README.md'

    def build(self):
        time_str = TimeFormat.TIME.format(Time.now())
        lines = (
            [
                '# Manifestos ',
                '',
                'This repository contains the manifestos for the '
                +'2024 Sri Lankan Presidential Election ',
                + f'I could find online, as of **{time_str}**.',
                '',
                'I\'ve **AI summaries** with chatgpt-4o '
                +'for manifestos with English Text'
                + ' including:',
                '* Most important promises',
                '* Most unrealistic promises',
                '* Top 5 reasons to vote for party',
                '* Top 5 reasons not to vote for party',
                '',
                '## Candidates & Manifestos',
                '',
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

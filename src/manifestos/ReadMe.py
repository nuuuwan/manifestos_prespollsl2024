from utils import File, Log, Time, TimeFormat

from manifestos.Manifesto import Manifesto

log = Log('ReadMe')


class ReadMe:
    PATH = 'README.md'

    def build(self):
        time_str = TimeFormat.TIME.format(Time.now())
        lines = (
            [
                '# #PresPollSL2024 Manifestos',
                '',
                'This repository contains the manifestos for the '
                + '2024 Sri Lankan Presidential Election '
                + f'I could find online, as of **{time_str}**.',
                '',
                'I\'ve generated **AI summaries** with chatgpt-4o '
                + 'for manifestos with English Text'
                + ' including:',
                '',
                '* ⭐ Most important promises',
                '* ❓ Most unrealistic promises',
                '* 👍 Top 5 reasons to vote for party',
                '* 👎 Top 5 reasons not to vote for party',
                '',
                'You can read a Comparison of the SP, AKD, RW and NR manifestos [here](data/summary/comparative.md)',
                '',
                'You can also ask the 2024 Sri Lankan '
                + 'Presidential Manifestos '
                + '[Custom ChatGPT](https://chatgpt.com/g/g-ZLkBo9b1v-2024-sri-lankan-presidential-manifestos)'
                + ' your own questions.',
                '',
                '![Custom ChatGPT](data/misc_images/custom-chatgpt.png)',
                '',
                '📦 Where possible, images in the original source PDFs have been '
                + 'compressed for more efficient storage.',
                '',
                '⚠️ Word counts are approximate and may not be accurate, especially for '
                + 'සිංහල and தமிழ்.',
                '',
                '## Candidates & Manifestos',
            ]
            + Manifesto.get_readme_lines()
            + [
                '',
            ]
        )

        File(self.PATH).write_lines(lines)
        log.info(f'Wrote {self.PATH}')

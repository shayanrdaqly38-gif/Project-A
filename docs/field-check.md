# Field check: local Markdown links

These are independent, read-only checks, not evidence that either team uses DocSignal.

| Repository and revision | Markdown files | Local references checked | Findings |
| --- | ---: | ---: | ---: |
| [Click](https://github.com/pallets/click/tree/08b803cf32ceb2ae6a772c62d5da42757a897d44) | 40 | 13 | 0 |
| [Typer](https://github.com/fastapi/typer/tree/2517edde5a1292a712e2f16e600754c52c6f00d9) | 81 | 28 | 3 |

## What the Typer findings mean

In the [root README, lines 57–59](https://github.com/fastapi/typer/blob/2517edde5a1292a712e2f16e600754c52c6f00d9/README.md#L57-L59), two links target `tutorial/install.md`. That file is not beside the README: it lives at `docs/tutorial/install.md`. This affects readers following the relative links from the repository README. A site rendering the same text at a different location can resolve the links differently.

The third finding is in `includes/agent-banner.md`. Its target, `ai-development.md`, exists under `docs/`. An included fragment may intentionally use the final page's base directory. We do not count this as a confirmed site bug. We did not test the deployed site or submit changes upstream.

## Reproduce from the DocSignal directory

```sh
git clone https://github.com/fastapi/typer /tmp/docsignal-typer
git -C /tmp/docsignal-typer checkout --detach 2517edde5a1292a712e2f16e600754c52c6f00d9
python3 docsignal.py /tmp/docsignal-typer
```

Expected exit code: 1 because findings exist. Zero findings on Click means only that the supported local links passed, not that every link on its website works.

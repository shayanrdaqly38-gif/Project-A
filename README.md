# DocSignal | راهنمای سالم

یک ابزار آفلاین برای پیدا کردن لینک‌های خراب در راهنمای پروژه. مثلاً اگر نام یک فایل یا عنوان یک بخش عوض شود، DocSignal فایل و شمارهٔ خطِ لینک خراب را نشان می‌دهد و اگر نام مشابهی پیدا کند، آن را پیشنهاد می‌دهد. هیچ فایلی را تغییر نمی‌دهد.

## شروع سریع

پایتون ۳٫۹ یا جدیدتر کافی است. پوشهٔ پروژه را در ترمینال باز کن و بنویس:

```sh
python3 docsignal.py .
```

برای امتحان واقعی، در [راهنمای نمونه](examples/guide/start.md) مقصد لینک را از `setup.md` به `setop.md` تغییر بده و دستور را دوباره اجرا کن. سپس تغییر را برگردان.

## For maintainers

Scan a directory without network access, credentials, or dependencies:

```sh
python3 docsignal.py /path/to/project
python3 docsignal.py . --format json
python3 docsignal.py . --format html > report.html
python3 -m unittest -v
```

Exit status: 0 = clean; 1 = broken references. A CI workflow runs the tests and audits this repository on pushes and pull requests.

Checks inline Markdown links and images, relative paths, root-relative paths, and fragments targeting scanned Markdown headings. Handles percent-encoded paths, simple Unicode headings and duplicate headings. Skips fenced examples, external URLs and hidden directories. Not a full Markdown renderer: reference-style links, HTML anchors, setext headings and complex inline formatting are not supported. Fragment rules can differ between documentation sites.

## آزمایش روی پروژه‌های واقعی

[نتیجهٔ بررسی Click و Typer، همراه با روش تکرار آزمایش](docs/field-check.md)

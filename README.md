# Log Analyzer

A command-line tool that reads a web server access log (Combined Log Format)
and reports traffic stats: totals, unique IPs, top endpoints, error rate,
hourly traffic, and suspicious login activity.

## Requirements

- Python 3.8+
- libraries needed (`re`, `collections`, `gzip`, `argparse`, `json`, `subprocess`, `unittest`)

## How to Run

**Direct mode** — one section, prints and exits:
```
logger summary access.log
logger endpoints access.log
logger hourly access.log
logger suspicious access.log
logger all access.log
```

You can add `--json` to any command to also save the full report as `report.json`:

```
logger all access.log --json
```

`.gz` compressed logs are supported directly, no need to unzip first:
```
logger all access.log.gz
```

**Interactive mode** — a menu, pick a report as many times as you want:
```
logger                # asks for the file path first
logger access.log     # file path already given, skips straight to the menu
```

## Running the Tests

```
python3 tests.py
```

or, from interactive mode, choose option `6` from the menu.

## Releases:
- release.yml file created to create releases for both linux and windows os for users to download and use. no need to clone the source code.

## توضیح پیاده سازی:

این پروژه شامل چهار قسمت اصلی هست که به تفکیک فایل توضیحات مربوط به آن آورده شده: 

- فایل parser.py فایلی هست که لاگ‌های فایل ورودی را خط به خط parse می‌کند. parse کردن لاگ‌ها با استفاده از regex انجام می‌شود.
- فایل analyzer.py  از لاگ‌های خوانده شده آمار مورد نیاز را جمع‌آوری می‌کند.
- فایل cli.py فایلی هست که در آن interface و محیط تعامل با اپلیکیشن و user پیاده‌سازی شده.
- فایل report.py آمار دریافت شده را در محیط ترمینال به شکل گرافیکی نمایش می‌دهد. 
- در نهایت یک فایل release.yml برای ساختن فایل‌های قابل اجرا در سیستم‌عامل‌های مختلف پیاده شد. به این شکل که github actions از طریق کد پوش شده و تگ خورده در ریپو یک نسخه قابل اجرایی برای هر سیستم‌عامل ایجاد می‌کند و در قسمت releases قرار می‌دهد.

## تصمیم‌های مهم و مشکلاتی که توی مسیر کار باهاشون مواجه شدم

- یکی از مشکلاتی که در استفاده از این ابزار داشتم، نوشتن و اجرای سرویس از طریق دستور python3 cli.py بود. در نتیجه سرچ‌هایی که داشتم با ساختن فایل اجرایی با استفاده از github actions آشنا شدم. بعد از پیاده‌سازی این مورد امکان اجرای این سرویس در هر سیستم‌عامل ویندوزی و لینوکسی بدون نیاز به clone کردن کل پروژه فراهم شد.

- نمودار ساعتی هم چند بار عوض شد. اول یک نمودار افقی بود که خیلی شلوغ به نظر
می‌رسید، بعد به عمودی تبدیلش کردم، ولی نسخه‌ی اول عدد هر ردیف رو کنارش
می‌نوشت که خوندنش گیج‌کننده بود. آخرش رسیدم به این که دقیقاً بالای هر ستون،
عدد واقعی همون ساعت رو یک‌جا می‌نویسم و مقیاس رو از صفر تا بیشترین مقدار
نشون می‌دم — خیلی خواناتر شد
[![fa](https://img.shields.io/badge/lang-fa-blue.svg)](https://github.com/SEPAD-Project/WebApplication/blob/main/README.fa.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/SEPAD-Project/WebApplication/blob/main/README.md)

# وب‌اپلیکیشن

این ریپازیتوری بخشی از پروژه SEPAD است که توسط [Parsa Safaie](https://github.com/parsasafaie) برای ارائه خدمات به مدارس در قالب سیستم جامع SEPAD توسعه داده شده است.

برای مشاهده سازمان SEPAD [اینجا کلیک کنید](https://github.com/SEPAD-Project).

این برنامه در حال حاضر بر روی دامنه زیر در حال اجرا است:  
**http://sepad-project.ir**

---

##  کلون کردن ریپازیتوری

برای کلون کردن این ریپازیتوری همراه با زیرماژول‌ها، دستور زیر را در ترمینال اجرا کنید:

```bash
git clone --recurse-submodules https://github.com/SEPAD-Project/WebApplication.git
cd WebApplication
```

---

## نصب پیش‌نیازها

1. ساخت محیط مجازی:

```bash
python -m venv .venv
```

2. فعال‌سازی محیط مجازی:

- در **ویندوز**:
```bash
.venv\Scripts\activate.bat
```

- در **لینوکس**:
```bash
source .venv/bin/activate
```

3. نصب کتابخانه‌ها:

```bash
pip install -r requirements.txt
```

---

## نصب Redis برای Celery

این پروژه از Celery برای اجرای وظایف پس‌زمینه استفاده می‌کند و Redis به‌عنوان message broker نیاز است.

- در **ویندوز**:
  1. فایل Redis را از [اینجا](https://github.com/microsoftarchive/redis/releases) دانلود کنید.
  2. مراحل نصب را طی کنید.
  3. پورت پیش‌فرض 6379 را انتخاب کنید.

- در **لینوکس**:

```bash
sudo apt update
sudo apt install redis
```

---

## اجرای پروژه

برای اجرای همزمان Django و Celery از فایل‌های اسکریپت زیر استفاده کنید:

- در **ویندوز**:
```bash
scripts/start_server.bat
```

- در **لینوکس**:
```bash
chmod +x scripts/start_server.sh
scripts/start_server.sh
```

پس از اجرا، پروژه از طریق آدرس زیر قابل مشاهده خواهد بود:

```
http://0.0.0.0:8080
```
[![fa](https://img.shields.io/badge/lang-fa-blue.svg)](https://github.com/SEPAD-Project/WebApplication/blob/main/README.fa.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/SEPAD-Project/WebApplication/blob/main/README.md)
# وب اپلیکیشن
این ریپازیتوری بخشی از پروژه SEPAD است که توسط [Parsa Safaie](https://github.com/parsasafaie) برای خدمت به مدارس در سیستم بزرگتر SEPAD توسعه داده شده است.

برای مشاهده سازمان SEPAD [اینجا](https://github.com/SEPAD-Project) کلیک کنید.

اپلیکیشن هم اکنون در آدرس زیر قابل دسترسی است:
http://sepad-project.ir/

> نکته: این اپلیکیشن وابستگی‌های خاص ویندوز دارد و برای محیط‌های ویندوز بهینه شده است.

## کلون کردن ریپازیتوری
برای کلون کردن این ریپازیتوری، در ترمینال دستور زیر را اجرا کنید:
```bash
git clone --recurse-submodules https://github.com/SEPAD-Project/WebApplication.git
```
بعد به دایرکتوری WebApplication بروید:
```bash
cd WebApplication
```

## نصب نیازمندی ها
   1. یک محیط مجازی بسازید:
      ```bash
      python -m venv .venv
      ```

   2. محیط مجازی را فعال کنید:
      ```bash
      .venv\Scripts\activate.bat
      ```

      1. نیازمندی ها را نصب کنید:
      ```bash
      pip install -r requirements.txt
      ```

## نیازمندی های Flask limiter
برای اجرای پروژه شما نیاز دارید برنامه redis را نصب کنید:
   1. فایل msi را از این ادرس دانلود کنید [Microsoft's Redis releases](https://github.com/microsoftarchive/redis/releases)
   2. فرایند نصب را طی کنید
   3. پورت پیشفرض 6379 را انتخاب کنید


## اجرای پروژه
برای اجرای آسان پروژه فایل run.bat را اجرا کنید
در ادرس زیر می توانید به خروجی دسترسی داشته باشد :
```
http://0.0.0.0:85
```

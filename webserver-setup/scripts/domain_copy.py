import os

# HTML 템플릿 정의
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>test{num}.inapp.test</title>
</head>
<body>
    <h1>Success to access test{num}.inapp.test</h1>
</body>
</html>
"""

# test1 ~ test129까지 index.html 생성
for i in range(1, 130):
    path = f"/var/www/finaltest{i}.inapp.test/public_html"
    try:
        os.makedirs(path, exist_ok=True)
        dst_file = os.path.join(path, "index.html")
        with open(dst_file, "w") as f:
            f.write(html_template.format(num=i))
        print(f"[+] Created index.html for finaltest{i}.inapp.test")
    except Exception as e:
        print(f"[!] Failed for finaltest{i}.inapp.test: {e}")

from distutils.dir_util import copy_tree
import os

from_path = '../tests'
dest_base_path = '/etc/apache2/ssl/'  # 현재 경로(/etc/apache2/ssl)에서 실행

file_list = os.listdir(from_path)

for file_name in file_list:
    # 디렉토리 이름이 test로 시작하고 숫자가 1 이상인 경우만 복사
    if file_name.startswith('test') and file_name[4:].isdigit() and int(file_name[4:]) >= 1:
        src = os.path.join(from_path, file_name)
        dst = os.path.join(dest_base_path, 'final' + file_name)
        copy_tree(src, dst)
        print(f'✅ {src} → {dst} copy completed!')

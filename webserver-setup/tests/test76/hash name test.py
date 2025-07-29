from cryptography import x509
from cryptography.hazmat.backends import default_backend
import hashlib
import subprocess

# PEM 형식의 인증서를 읽어서 x509 인증서 객체로 변환
def load_certificate(file_path):
    with open(file_path, "rb") as f:
        cert_pem = f.read()
    cert = x509.load_pem_x509_certificate(cert_pem, default_backend())
    return cert

# 주어진 인증서의 subject 또는 issuer에 대한 해시 값 계산 (SHA-256 사용)
def get_name_hash(cert, name_type='subject'):
    if name_type == 'subject':
        name = cert.subject
    elif name_type == 'issuer':
        name = cert.issuer
    else:
        raise ValueError("name_type must be 'subject' or 'issuer'")

    # X.509 Name 객체의 DER 인코딩 후 SHA-256 해시 계산
    name_bytes = name.public_bytes()
    name_hash = hashlib.sha256(name_bytes).hexdigest()
    return name_hash

#초기화(der --> pem)
cmd = f'openssl x509 -in testInterCa.pem -inform der -out testInterCa.pem -outform pem'
subprocess.run(cmd, shell=True, check=False)

cmd = f'openssl x509 -in testLeafCert.pem -inform der -out testLeafCert.pem -outform pem'
subprocess.run(cmd, shell=True, check=False)

print("\n")

# 인증서들 로드
root_cert = load_certificate("testRootCa.crt")
inter_cert = load_certificate("testInterCa.pem")
leaf_cert = load_certificate("testLeafCert.pem")

# 해시 값 비교
root_subject_hash = get_name_hash(root_cert, 'subject')
inter_issuer_hash = get_name_hash(inter_cert, 'issuer')

inter_subject_hash = get_name_hash(inter_cert, 'subject')
leaf_issuer_hash = get_name_hash(leaf_cert, 'issuer')

# 비교 결과 출력
if root_subject_hash == inter_issuer_hash:
    print("Yes: testRootCa.crt subject matches testInterCa.pem issuer.")
else:
    print("No: testRootCa.crt subject does NOT match testInterCa.pem issuer.")

if inter_subject_hash == leaf_issuer_hash:
    print("Yes: testInterCa.pem subject matches testLeafCert.pem issuer.")
else:
    print("No: testInterCa.pem subject does NOT match testLeafCert.pem issuer.")

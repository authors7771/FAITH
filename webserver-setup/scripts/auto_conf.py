import os
frompath = '../tests'
test_dir = os.listdir(frompath)
add_conf_list =sorted([int(i[4:]) for i in test_dir])
#add_conf_list = [i for i in range(200, 201)]
vh443_1 = """
    <VirtualHost *:443>
        ServerAdmin webmaster@finaltest.inapp.test"""
vh443_2 = """
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        SSLEngine on
"""
vh443_3 = """
        <FilesMatch "\.(cgi|shtml|phtml|php)$">
            SSLOptions +StdEnvVars
        </FilesMatch>
        <Directory /usr/lib/cgi-bin>
            SSLOptions +StdEnvVars
        </Directory>
    </VirtualHost>
"""
add_conf = ''
for i in add_conf_list:
    servername = """
        ServerName finaltest""" + str(i) + ".inapp.test"
    serveralias = """
        ServerAlias finaltest""" + str(i) + ".inapp.test"
    documentroot ="""
        DocumentRoot /var/www/finaltest""" + str(i) + ".inapp.test/public_html"
    SSL_setting = """
        SSLEngine on
        SSLCertificateFile  /etc/apache2/ssl/finaltest"""+ str(i) + """/testLeafCert.pem
        SSLCertificateKeyFile /etc/apache2/ssl/finaltest"""+ str(i) + """/leafPrivateEcc384.key
        SSLCertificateChainFile /etc/apache2/ssl/finaltest"""+ str(i) + "/testInterCa.pem"
    vh80 = """

    <VirtualHost *:80>
        ServerName finaltest"""+ str(i)+ """.inapp.test
	Redirect / https://finaltest"""+ str(i) +""".inapp.test/
    </VirtualHost>

"""
    add_conf = add_conf + vh443_1+servername+serveralias+documentroot+vh443_2 + SSL_setting + vh443_3 + vh80
edited_txt = ''
with open('../apache-configs/finaltest.conf','r') as f:
    check = 0
    for t in f.readlines():
        if ':80' in t and check == 0:
            edited_txt = edited_txt + add_conf + '\n' + t
            check = 1
        else:
            edited_txt = edited_txt + t
with open('/etc/apache2/sites-available/finaltest.conf', 'w') as f:
    f.write(edited_txt)


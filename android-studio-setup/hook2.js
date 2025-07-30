Java.perform(() => {
  const PKIXCertPathValidator = Java.use('sun.security.provider.certpath.PKIXCertPathValidator');
  const X500Principal = Java.use('javax.security.auth.x500.X500Principal');
  const Throwable = Java.use('java.lang.Throwable');
  const CertPathValidatorException = Java.use('java.security.cert.CertPathValidatorException');
  const X509Certificate = Java.use('java.security.cert.X509Certificate');
  const Base64 = Java.use('android.util.Base64');
  const Log = Java.use('android.util.Log');
  const TrustManagerImpl = Java.use('com.android.org.conscrypt.TrustManagerImpl');

  let currentHost = null;

  try {
    const X509TrustManagerExtensions = Java.use('android.net.http.X509TrustManagerExtensions');
    X509TrustManagerExtensions.checkServerTrusted.overload('[Ljava.security.cert.X509Certificate;', 'java.lang.String', 'java.lang.String').implementation = function (chain, authType, host) {
      currentHost = host;
      return this.checkServerTrusted(chain, authType, host);
    };
  } catch (e) {
    console.log('⚠️ Failed to hook checkServerTrusted:', e);
  }

  function shouldLogCertPath(certPath) {
    try {
      const certList = certPath.getCertificates().toArray();
      for (let i = 0; i < certList.length; i++) {
        const cert = Java.cast(certList[i], X509Certificate);
        const subject = cert.getSubjectX500Principal().getName();
        if (subject.includes("inapp.test")) {
          return true;
        }
      }
    } catch (err) {
      console.error('Error checking CN filter:', err);
    }
    return false;
  }

  function getPemString(encodedBytes) {
    const base64 = Base64.encodeToString(encodedBytes, 0); // NO_WRAP = 0
    const lines = base64.match(/.{1,64}/g);
    return lines.join('\n');
  }

  PKIXCertPathValidator.validate.overload(
    'java.security.cert.TrustAnchor',
    'sun.security.provider.certpath.PKIX$ValidatorParams'
  ).implementation = function (anchor, params) {
    const certPath = params.certPath();
    const certs = certPath.getCertificates().toArray();

    if (!shouldLogCertPath(certPath)) {
      return this.validate(anchor, params);
    }

    console.log(`\n===============================`);
    console.log(`📌 [PKIX.validate()] Triggered for *.inapp.test`);
    if (currentHost) console.log(`🌐 Host: ${currentHost}`);
    console.log(`===============================`);

    console.log(`🧾 CertPath Length: ${certs.length}`);
    for (let i = 0; i < certs.length; i++) {
      try {
        const cert = Java.cast(certs[i], X509Certificate);
        const subject = cert.getSubjectX500Principal().getName();
        const issuer = cert.getIssuerX500Principal().getName();
        console.log(`  🔹 [Cert ${i}] Subject: ${subject}`);
        console.log(`             Issuer : ${issuer}`);

        const pem = getPemString(cert.getEncoded());
        console.log(`             -----BEGIN CERTIFICATE-----\n${pem}\n-----END CERTIFICATE-----`);
      } catch (e) {
        console.log(`⚠️ Failed to print cert[${i}]: ${e}`);
      }
    }

    const anchorCert = anchor.getTrustedCert();
    if (anchorCert) {
      const anchorSubject = anchorCert.getSubjectX500Principal().getName();
      console.log(`✅ TrustAnchor SubjectDN: ${anchorSubject}`);
    } else {
      console.log(`✅ TrustAnchor is key-only (no certificate)`);
    }

    try {
      console.log(`📋 PKIX Policy Flags:`);
      console.log(`  initialPolicies          : ${params.initialPolicies().toArray().join(', ')}`);
      console.log(`  explicitPolicyRequired   : ${params.explicitPolicyRequired()}`);
      console.log(`  policyMappingInhibited   : ${params.policyMappingInhibited()}`);
      console.log(`  anyPolicyInhibited       : ${params.anyPolicyInhibited()}`);
      console.log(`  policyQualifiersRejected : ${params.policyQualifiersRejected()}`);
    } catch (e) {
      console.log(`⚠️ Could not extract PKIX policy flags: ${e}`);
    }

    try {
      const result = this.validate(anchor, params);
      console.log(`✅ validate() succeeded`);
      try {
        const throwable = Throwable.$new();
        const stackTrace = throwable.getStackTrace();
        console.log('🧵 validate() call stack:');
        for (let i = 0; i < stackTrace.length; i++) {
          console.log(`    at ${stackTrace[i].toString()}`);
        }
      } catch (stackErr) {
        console.log(`⚠️ Failed to retrieve call stack: ${stackErr}`);
      }
      return result;
    } catch (err) {
      console.log(`❌ validate() failed: ${err}`);
      try {
        const throwable = Throwable.$new();
        const stackTrace = throwable.getStackTrace();
        console.log('🧵 validate() call stack:');
        for (let i = 0; i < stackTrace.length; i++) {
          console.log(`    at ${stackTrace[i].toString()}`);
        }
      } catch (stackErr) {
        console.log(`⚠️ Failed to retrieve call stack: ${stackErr}`);
      }
      throw err;
    }
  };
});


import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# =====================================================================
# JOB 1: INITIALIZE THE ROOT CA (Run once during setup)
# =====================================================================
def generate_root_ca():
    # 1. Generate the CA's Master Private Key
    ca_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096, 
    )

    # 2. Define the CA's "Subject" (Who this certificate is about)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"VN"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Hanoi"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Hanoi"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Awesome University PKI"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"MyAwesomeRootCA"),
    ])

    # 3. Build the Certificate
    cert_builder = x509.CertificateBuilder()
    cert_builder = cert_builder.subject_name(subject)
    cert_builder = cert_builder.issuer_name(issuer)
    cert_builder = cert_builder.public_key(ca_private_key.public_key())
    
    cert_builder = cert_builder.not_valid_before(datetime.datetime.utcnow())
    cert_builder = cert_builder.not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=3650) 
    )
    
    cert_builder = cert_builder.serial_number(x509.random_serial_number())

    cert_builder = cert_builder.add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True,
    )

    # 4. Sign the certificate with its OWN private key
    root_certificate = cert_builder.sign(
        private_key=ca_private_key, 
        algorithm=hashes.SHA256()
    )

    return ca_private_key, root_certificate

# =====================================================================
# JOB 2: SIGN USER CERTIFICATES (Run every time a user applies)
# =====================================================================
def sign_approved_csr(approved_csr, ca_private_key, ca_name):
    print("Root CA: Received approved 'Passport Application' (CSR).")
    print("Root CA: Preparing the official digital passport...")
    
    cert_builder = x509.CertificateBuilder()
    cert_builder = cert_builder.subject_name(approved_csr.subject)
    cert_builder = cert_builder.issuer_name(ca_name)
    cert_builder = cert_builder.public_key(approved_csr.public_key())
    
    cert_builder = cert_builder.not_valid_before(datetime.datetime.utcnow())
    cert_builder = cert_builder.not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    )
    
    cert_builder = cert_builder.serial_number(x509.random_serial_number())
    cert_builder = cert_builder.add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True,
    )
    
    print("Root CA: Stamping the official seal (Signing)...")
    final_certificate = cert_builder.sign(
        private_key=ca_private_key, 
        algorithm=hashes.SHA256()
    )
    
    pem_certificate = final_certificate.public_bytes(serialization.Encoding.PEM)
    print("Root CA: Certificate issued successfully! 🏆")
    
    return pem_certificate
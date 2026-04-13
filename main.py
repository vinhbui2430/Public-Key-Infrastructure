import os
import ca
import client
import ra

def setup_environment():
    print("📁 Setting up directory structure...")
    # exist_ok=True means it won't crash if the folders already exist!
    os.makedirs('archive/issued_certs', exist_ok=True)
    print("📁 Vault secured: 'archive/' and 'archive/issued_certs/' are ready.\n")

def run_pki_simulation():
    print("=========================================")
    print("🏛️  STARTING PKI SIMULATION 🏛️")
    print("=========================================\n")

    # Build the folders first!
    setup_environment()

    # ---------------------------------------------------------
    # PHASE 1: The Big Boss sets up shop
    # ---------------------------------------------------------
    print("--- PHASE 1: CA INITIALIZATION ---")
    ca_private_key, root_cert = ca.generate_root_ca()
    ca_name = root_cert.subject 
    
    # 💾 SAVE THE ROOT FILES TO THE ARCHIVE
    # We use 'wb' (write binary) because our PEM data is in bytes
    with open('archive/root_private.pem', 'wb') as f:
        # Note: In cryptography, you must serialize the private key before saving
        from cryptography.hazmat.primitives import serialization
        f.write(ca_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
        
    with open('archive/root_cert.pem', 'wb') as f:
        f.write(root_cert.public_bytes(serialization.Encoding.PEM))
        
    print("Root CA initialized. Master keys locked in archive.\n")

    # ---------------------------------------------------------
    # PHASE 2: The Citizen applies for a passport
    # ---------------------------------------------------------
    print("--- PHASE 2: CLIENT REQUEST ---")
    client_private_key, pem_csr = client.generate_csr()
    
    # 💾 SAVE THE CLIENT'S PRIVATE KEY LOCALLY (NOT in the archive!)
    with open('client_private.pem', 'wb') as f:
        from cryptography.hazmat.primitives import serialization
        f.write(client_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
        
    print("Client generated keys. Private key saved locally. CSR submitted to RA.\n")

    # ---------------------------------------------------------
    # PHASE 3: The Bouncer checks the ID
    # ---------------------------------------------------------
    print("--- PHASE 3: RA VERIFICATION ---")
    approved_csr = ra.verify_csr_request(pem_csr)
    print("\n")

    # ---------------------------------------------------------
    # PHASE 4: The Big Boss stamps the passport
    # ---------------------------------------------------------
    print("--- PHASE 4: CA ISSUANCE ---")
    if approved_csr:
        final_cert_pem = ca.sign_approved_csr(approved_csr, ca_private_key, ca_name)
        
        # 💾 SAVE THE ISSUED CERTIFICATE TO THE ARCHIVE
        # We can use the serial number from the CSR/Cert to name the file
        cert_filename = f"archive/issued_certs/client_cert.pem"
        with open(cert_filename, 'wb') as f:
            f.write(final_cert_pem)
            
        print(f"\n🎉 SUCCESS! Certificate saved to {cert_filename} 🎉\n")
    else:
        print("\n🚨 ALERT: The RA rejected the request. No certificate issued.")

if __name__ == "__main__":
    run_pki_simulation()
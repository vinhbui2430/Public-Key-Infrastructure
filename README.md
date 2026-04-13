# Public-Key-Infrastructure-

Public Key Infrastructure for Asymmetric Encryption implementation
> Definition:
  A set of policies, processes, server platforms, software and workstations used
for the purpose of administering certificates and public-private key pairs, in
-cluding the ability to issue, maintain, and revoke public key certificates.

Project tree: 
``` plaintext
PKI_Project/
│
├── pki_library.py    # The Toolbelt: Shared functions like our RSA key generator.
├── ca.py             # The Big Boss: Generates the Root Cert, signs CSRs, revokes certs.
├── ra.py             # The Bouncer: Receives requests, checks identity, passes to CA.
├── client.py         # The Citizen: Generates their own keys and asks the RA for a cert.
│
└── archive/          # The Vault: Where the CA stores copies of all issued certificates.
```

*PKI Block diagram*
``` mermaid
graph TD
    subgraph "The Trust Factory (The Backend)"
        RA[<b>Registration Authority</b><br/>'The Bouncer']
        CA[<b>Certificate Authority</b><br/>'The High Priest']
    end

    subgraph "The Public Square (The Storage)"
        Repo[<b>Repository</b><br/>'The Library']
        CRL[<b>CRL Issuer</b><br/>'The Wall of Shame']
    end

    EE[<b>End Entity</b><br/>'The Student/Python Script']

    %% Workflow Connections
    EE -- "1. Identify & Apply" --> RA
    RA -- "2. Vouch For" --> CA
    CA -- "3. Sign & Issue" --> EE
    CA -- "4. Catalog" --> Repo
    CA -- "5. Revoke (If Hacked)" --> CRL
    CRL -- "6. Update Blacklist" --> Repo
    EE -- "7. Verify Others" --> Repo
```
## End Entity (EE)	
The certificate holder (User or Device).	To prove who they are without giving away their private key.
## Registration Authority (RA)
Identity verification.	To make sure "Alice" isn't actually a malicious bot in a trench coat before she gets a cert.
## Certificate Authority (CA)
The "Root of Trust" that signs certificates.	Because a certificate is just a piece of paper unless someone important (the CA) signs it.
## Repository	
A public directory of certificates.	So Bob can find Alice's public key without having to call her on the phone.
CRL Issuer

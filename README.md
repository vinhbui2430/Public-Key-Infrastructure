# Public-Key-Infrastructure-

Public Key Infrastructure for Asymmetric Encryption implementation
> Definition:
  A set of policies, processes, server platforms, software and workstations used
for the purpose of administering certificates and public-private key pairs, in
-cluding the ability to issue, maintain, and revoke public key certificates.

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


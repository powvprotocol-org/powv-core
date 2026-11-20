# Historical Sandbox Material (Retired)

This repository previously contained an early illustrative sandbox draft (2026), consisting of a repository-structure note, an embedded example encoder, gateway and feeder, a utility script and a short flow description.

**That material was retired on November 20, 2026.** It was never a current implementation, specification or validation result, and it should not be evaluated as one.

## Why it was retired

The draft had been preserved with a "historical" notice, but its own known limitations made it misleading as technical evidence:

- the example verification did not verify signatures;
- the example signature handling was not a valid encoding;
- duplicate detection was not persistent;
- keys were software-generated;
- the example integrity aggregation did not use domain-separated hashing;
- some descriptive text overstated security properties (hardware enclaves, end-to-end protection, consensus).

It also exposed implementation-level detail that the PoWV [Disclosure Boundary](https://powv-protocol.gitbook.io/powv-protocol-docs/security/disclosure-boundary) classifies as restricted.

## What superseded it

The limitations listed above were addressed in later, access-controlled engineering work, **except hardware-rooted device identity, which remains pending**. That work is experimental and unmerged, and it is summarized publicly at capability level only:

- [November 20, 2026 software engineering update](https://github.com/powvprotocol-org/powv-lab-status/blob/main/status/2026-11-software-engineering-update.md)
- [Project Status](https://powv-protocol.gitbook.io/powv-protocol-docs/project-status)
- [Physical integration record, September 18, 2026](https://github.com/powvprotocol-org/powv-scale-edge-integration/blob/main/docs/integration-module/experimental-record.md)

Still not established: hardware-backed signatures, authenticated device identity, independent edge verification, durable anchoring and a production chain of custody.

## Note for reviewers

Earlier commits of this repository still contain the retired files. They are historical artifacts and do not describe the current system. For current, authoritative information, use the links above or contact the maintainers through the official channels listed in the [README](README.md).

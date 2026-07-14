"""
PoWV Protocol - Ledger Flush Utility (tools/flush_chain_to_ledger.py)
Reconciles the in-memory blockchain state with the local immutable disk ledger.
Calculates progressive Merkle roots and appends only unseen cryptographic proofs.
"""
import requests
import json
import os
import hashlib
from datetime import datetime

# System Configuration
LEDGER = os.path.join('logs', 'immutable_anchor_ledger.log')
BLOCKS_URL = 'http://127.0.0.1:5003/blocks'

def merkle_root_list(hashes):
    """Calculates the Merkle Root for a given list of cryptographic hashes."""
    if not hashes:
        return None
    
    layer = hashes[:]
    while len(layer) > 1:
        # Duplicate the last hash if the layer has an odd number of elements
        if len(layer) % 2 == 1:
            layer.append(layer[-1])
        
        # Hash pairs together to form the next layer up the tree
        layer = [
            hashlib.sha256((layer[i] + layer[i+1]).encode()).hexdigest() 
            for i in range(0, len(layer), 2)
        ]
        
    return layer[0]

def flush_to_ledger():
    """Fetches chain state, calculates progressive roots, and persists deltas."""
    print("[*] Initiating Ledger Flush Protocol...")
    
    # 1. State Reconciliation: Read existing ledger roots into a set (O(1) lookup)
    existing_roots = set()
    if os.path.exists(LEDGER):
        with open(LEDGER, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('MERKLE_ROOT:')
                if len(parts) == 2:
                    existing_roots.add(parts[1].strip())
    
    # 2. Consensus Fetching: Pull current in-memory chain from the Audit Layer
    try:
        response = requests.get(BLOCKS_URL, timeout=5)
        if response.status_code != 200:
            print(f"[!] Target node rejected fetch request. Status: {response.status_code}")
            raise SystemExit(1)
    except requests.exceptions.ConnectionError:
        print("[!] Connection failed. Is blockchain_audit.py running on port 5003?")
        raise SystemExit(1)
        
    data = response.json()
    chain = data.get('chain', []) if isinstance(data, dict) else data

    # 3. Progressive Cryptography: Re-calculate roots iteratively
    hashes = [block.get('event_hash') for block in chain]
    new_entries = []
    
    for i in range(1, len(hashes) + 1):
        root = merkle_root_list(hashes[:i])
        # Only stage roots that are not already safely stored on disk
        if root and root not in existing_roots:
            new_entries.append((i, root))

    # 4. Append-Only Persistence: Write the cryptographic delta to the ledger
    if not new_entries:
        print("[✓] Ledger is already up to date. No new roots to append.")
    else:
        with open(LEDGER, 'a', encoding='utf-8') as f:
            for idx, root in new_entries:
                timestamp = datetime.now().isoformat()
                f.write(f"{timestamp} | MERKLE_ROOT: {root}\n")
        
        print(f"[✓] Successfully anchored {len(new_entries)} new Merkle Roots to disk.")

if __name__ == "__main__":
    flush_to_ledger()

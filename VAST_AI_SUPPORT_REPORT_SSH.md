# Vast.ai Support Report — Account-wide SSH key-propagation failure (2026-11-11)

**Account:** [your Vast.ai account email]
**Date the issue started:** 2026-11-11 (was working fine on 2026-11-10)
**Severity:** Blocker — cannot SSH into ANY rented instance

---

## 1. Symptom

I can rent instances successfully via the API, and the instances boot (sshd is running and reachable on the direct IP), but **every SSH connection is rejected**:

- `ssh -p <port> root@<direct_public_ip>`  →  **`Permission denied (publickey)`**
- `ssh -p <port> root@<sshN.vast.ai>`  (proxy)  →  **`Connection closed` / `Connection timed out during banner exchange`**

`Permission denied (publickey)` on the direct IP means the SSH daemon **is** running and accepting TCP connections, but **`/root/.ssh/authorized_keys` on the instance is empty** — none of my registered public keys were ever written to the box.

## 2. Timeline — it worked yesterday, broke today

- **2026-11-10 (~23:00):** SSH into instance **60123928** (RTX 6000D) worked perfectly with the same key.
- **2026-11-11 (from ~15:00 onwards):** every new instance fails SSH. The only change between "works" and "broken" is the calendar date — no change on my side (same keypair, same client, same tooling).

## 3. Scope tested (so it's not my key, host, or client)

| What I tried | Result |
|---|---|
| **13 instances rented** today | all fail SSH |
| **6 different host IPs** (32.196.117.67, 3.87.100.167, 23.158.136.85, 32.200.23.213, 54.82.210.84, 72.83.150.152) | all fail — not a single bad host |
| **ED25519 key** (registered, attach → "duplicate: already exists") | rejected |
| **RSA key** (freshly generated, registered as key id **1859527**, attach → "success") | rejected |
| **onstart script** that writes the pubkey to `/root/.ssh/authorized_keys` at boot (the documented fix for key-injection timing) | **never ran** — authorized_keys is still empty |
| **Direct public IP + direct port** (the documented fallback when the sshN proxy times out) | sshd answers, but `Permission denied (publickey)` — key not present |
| Verified the local private/public keypair matches (`ssh-keygen -y -f` == `.pub`) | matches — not a local-key problem |

## 4. What I believe is broken

**Vast.ai stopped propagating SSH public keys to instances — both the account-registered keys and the `onstart` key-injection.** The instance boots, sshd starts, but the key never lands in `authorized_keys`. This is account-wide and started today.

Example from the most recent instance (60255213, RTX A6000):
- direct `72.83.150.152:60400` → `Permission denied (publickey)` (sshd up, no key)
- proxy `ssh8.vast.ai:34188` → `Connection closed`

## 5. Registered SSH keys on the account

- key id **1833228** (ED25519, the one that worked on 2026-11-10)
- key id **1744975**, **1765140** (pre-existing)
- key id **1859527** (RSA, added today to test — same result)

## 6. Request

Please investigate why **no SSH public key (registered account key or onstart-injected) is being written to `/root/.ssh/authorized_keys`** on newly rented instances as of 2026-11-11. This is blocking all work. A working instance SSH is all I need.

**Credit impact so far:** ~13 instances rented and destroyed while diagnosing this (each briefly billed) — I'd appreciate a note/credit for the churn caused by the platform-side failure.
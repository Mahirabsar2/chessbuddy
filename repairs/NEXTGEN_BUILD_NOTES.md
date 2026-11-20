# ChessBuddy Next Gen 1.0.0

This branch is the isolated Next Gen release candidate. The build applies `apply_repairs.py` followed by `nextgen_1_0_0.py`, verifies JavaScript syntax, runs the JavaScript logic suite and Java policy suite, then assembles and verifies an Android APK.

The current CI signing key is preview-only unless the repository owner configures `CB_RELEASE_KEYSTORE_BASE64`, `CB_RELEASE_STORE_PASSWORD`, `CB_RELEASE_KEY_ALIAS`, and `CB_RELEASE_KEY_PASSWORD` as Actions secrets. A preview APK is not suitable for in-place auto-updates.

The APK must exceed 200 MiB before this candidate can be accepted as the requested release.

CI retry note: artifact upload path expression corrected in the default-branch workflow.
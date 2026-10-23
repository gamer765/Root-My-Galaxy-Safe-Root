#!/usr/bin/env python3
"""Apply fail-closed Safe Root app integration to a pinned upstream checkout."""
from pathlib import Path

base = Path("upstream")
def edit(path, changes):
    f=base/path
    s=f.read_text()
    for old,new in changes:
        count=s.count(old)
        if count != 1:
            raise RuntimeError(f"{path}: expected one match, got {count}: {old[:90]!r}")
        s=s.replace(old,new,1)
    f.write_text(s)

edit("app/src/main/java/dev/busung/s25uroot/PayloadRepository.kt", [
 ("BuSung-dev/Root-My-Galaxy-Payloads", "gamer765/Root-My-Galaxy-Payloads"),
])
edit("app/src/main/java/dev/busung/s25uroot/InstallViewModel.kt", [
 ("fun install(profileId: String? = null)", "fun install(profileId: String? = null, safeRoot: Boolean = false)"),
 ("installKernelSu(payloads)", "installKernelSu(payloads, safeRoot)"),
 ("private suspend fun installKernelSu(payloads: VerifiedPayloads)", "private suspend fun installKernelSu(payloads: VerifiedPayloads, safeRoot: Boolean)"),
 ('val lateLoad = runHelper("--late-load")', 'val lateLoad = if (safeRoot) runHelper("--late-load", "--safe-mode") else runHelper("--late-load")'),
])
edit("app/src/main/java/dev/busung/s25uroot/MainActivity.kt", [
 ('openInstaller: (String?) -> Unit,', 'openInstaller: (String?, Boolean) -> Unit,'),
 ('openInstaller = { profileId ->', 'openInstaller = { profileId, safeRoot ->'),
 ('val installer = Intent(this, InstallActivity::class.java)', 'val installer = Intent(this, InstallActivity::class.java)\n                            .putExtra(InstallActivity.EXTRA_SAFE_ROOT, safeRoot)'),
 ('var showInstallConfirmation by remember { mutableStateOf(false) }', 'var showInstallConfirmation by remember { mutableStateOf(false) }\n    var safeRoot by remember { mutableStateOf(false) }'),
 ('text = { Text(stringResource(R.string.install_confirm_body)) },', '''text = {
                androidx.compose.foundation.layout.Column {
                    Text(stringResource(R.string.install_confirm_body))
                    androidx.compose.material3.Row(verticalAlignment = androidx.compose.ui.Alignment.CenterVertically) {
                        androidx.compose.material3.Checkbox(checked = safeRoot, onCheckedChange = { safeRoot = it })
                        Text("Safe Root (skip third-party modules)")
                    }
                }
            },'''),
 ('openInstaller(selectedProfile?.profileId)', 'openInstaller(selectedProfile?.profileId, safeRoot)'),
])
edit("app/src/main/java/dev/busung/s25uroot/InstallActivity.kt", [
 ('val profileId = intent.getStringExtra(EXTRA_PROFILE_ID)', 'val profileId = intent.getStringExtra(EXTRA_PROFILE_ID)\n        val safeRoot = intent.getBooleanExtra(EXTRA_SAFE_ROOT, false)'),
 ('installViewModel.install(profileId)', 'installViewModel.install(profileId, safeRoot)'),
 ('const val EXTRA_PROFILE_ID = "profile_id"', 'const val EXTRA_PROFILE_ID = "profile_id"\n        const val EXTRA_SAFE_ROOT = "safe_root"'),
])
print("Safe Root app patch applied")

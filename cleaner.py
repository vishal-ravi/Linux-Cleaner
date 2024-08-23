import subprocess

def remove_temp_files():
    """Remove temporary files."""
    print("Removing temporary files...")
    subprocess.run(['sudo', 'rm', '-rf', '/tmp/*'], check=True)
    subprocess.run(['sudo', 'rm', '-rf', '/var/tmp/*'], check=True)

def clean_apt_cache():
    """Clean APT cache."""
    print("Cleaning APT cache...")
    subprocess.run(['sudo', 'apt-get', 'clean'], check=True)

def remove_old_kernels():
    """Remove old kernels."""
    print("Removing old kernels...")
    subprocess.run(['sudo', 'apt-get', 'autoremove', '--purge', '-y'], check=True)

def clean_snap_cache():
    """Clean Snap cache."""
    print("Cleaning Snap cache...")
    subprocess.run(['sudo', 'rm', '-rf', '/var/lib/snapd/cache/*'], check=True)

def clean_journal_logs():
    """Clean systemd journal logs older than 2 weeks."""
    print("Cleaning systemd journal logs...")
    subprocess.run(['sudo', 'journalctl', '--vacuum-time=2weeks'], check=True)

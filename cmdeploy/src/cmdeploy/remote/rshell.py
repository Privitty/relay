from subprocess import CalledProcessError, check_output


def shell(command, fail_ok=False):
    print(f"$ {command}")
    try:
        return check_output(command, shell=True).decode().rstrip()
    except CalledProcessError:
        if not fail_ok:
            raise
        return ""


def get_systemd_running():
    lines = shell("systemctl --type=service --state=running").split("\n")
    return [line for line in lines if line.startswith("  ")]


def write_numbytes(path, num):
    with open(path, "w") as f:
        f.write("x" * num)


def dovecot_recalc_quota(user):
    shell(f"doveadm quota recalc -u {user}")
    output = shell(f"doveadm quota get -u {user}")
    #
    # Quota name Type    Value  Limit                                              %
    # User quota STORAGE     5 102400                                              0
    # User quota MESSAGE     2      -                                              0
    #
    for line in output.split("\n"):
        parts = line.split()
        if parts[2] == "STORAGE":
            return dict(value=int(parts[3]), limit=int(parts[4]), percent=int(parts[5]))

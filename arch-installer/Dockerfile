FROM archlinux:latest

RUN pacman -Sy --noconfirm git curl tar base-devel && \
    pacman -Scc --noconfirm

WORKDIR /app

ENTRYPOINT ["tail", "-f", "/dev/null"]

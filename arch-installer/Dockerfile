FROM archlinux:latest

RUN pacman -Sy --noconfirm git curl tar base-devel && \
    pacman -Scc --noconfirm

WORKDIR /app

# COPY ./dist/arch-installer ./arch-installer
# RUN chmod +x ./arch-installer

ENTRYPOINT ["tail", "-f", "/dev/null"]

# Bygger Breakout-spelet (Pygame/pygame_menu) till en webbversion med pygbag
# (WebAssembly + Pyodide), serverar sedan resultatet som statiska filer med
# nginx. Se project/Breakout/main.py for kommentarer om vad som anpassats
# for att kora i en webblasare istallet for ett vanligt skrivbordsfonster.

FROM python:3.11-slim AS build
WORKDIR /app
COPY project/Breakout ./Breakout
RUN pip install --no-cache-dir pygbag \
    && python -m pygbag --build Breakout

FROM nginx:alpine
COPY --from=build /app/Breakout/build/web /usr/share/nginx/html
EXPOSE 80

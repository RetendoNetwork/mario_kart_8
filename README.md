# mario_kart_8
- Retendo Network Mario Kart 8 Server Replacement.

## Build
- Need Python, Docker and git.
- Git clone the repository with `git clone https://github.com/RetendoNetwork/mario_kart_8.git`.
- Rename the `example.env` to `.env` and add your configuration.
- Go to the cmd in the folder.
- And build an docker image `docker build -t mario_kart_8 .`.
- And start the server `docker run mario_kart_8`.

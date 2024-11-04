# LienHoa auto gate - ALPR API

API for license plates image processing.

![GitHub Tag](https://img.shields.io/github/v/tag/VinhNgT/lienhoa-gate-alpr-api?style=flat-square)

**Note**: Use a 64-bit x84 computer.

## Quick start

### Install Docker

#### Windows

- Download and install docker from https://www.docker.com/

#### Linux

- Install docker: https://docs.docker.com/engine/install/debian/
- Run `sudo usermod -aG docker $USER`
- Start services on boot:

  ```bash
  sudo systemctl enable docker.service
  sudo systemctl enable containerd.service
  ```

- Create file `/etc/docker/daemon.json` with content:

  ```json
  {
    "log-driver": "local"
  }
  ```

- Reboot with `sudo reboot`

### Start docker container

- Download the `compose.yaml` file.
- Run `docker compose up` or `docker compose up -d` in the folder where you saved the file.
  - Tip: You can use `--build` to force build locally if you cloned the whole project.
- Use examples in `insomnia_exports` to familiarize yourself, or go to http://localhost/docs

## Setup development enviroment

- Install Docker using the above quickstart guide.
- Install VS Code.
- Install "Dev Containers" extension.
- Open the project using devcontainer.
- Start the server.

  ```bash
  # Start on port 8000
  bash scripts/start-server.sh
  ```

  ```bash
  # Start on port 80
  sudo su
  fastapi run fastapi_app/main.py --port 80
  ```

  Alternative non-root: https://www.geeksforgeeks.org/bind-port-number-less-1024-non-root-access/

## Upgrade packages:

```bash
pip freeze > requirements.txt
sed -i 's/==/>=/g' requirements.txt
pip install -r requirements.txt --upgrade
```

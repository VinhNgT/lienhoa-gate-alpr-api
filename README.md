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

- Run `docker compose up`
  - Note: You can use `docker compose up --build` to force build locally.
- Use examples in `insomnia_exports` to familiarize yourself, or go to http://localhost/docs

## Manual start (Linux only, not automatically start on boot, more error prone)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export WORKSPACE_PATH=$(pwd)
export OPENALPR_PATH=$WORKSPACE_PATH/openalpr

bash scripts/post-create-devcontainer.sh

sudo su
fastapi run fastapi_app/main.py --port 80
```

Alternative: https://www.geeksforgeeks.org/bind-port-number-less-1024-non-root-access/

## Upgrade packages:

```bash
pip freeze > requirements.txt
sed -i 's/==/>=/g' requirements.txt
pip install -r requirements.txt --upgrade
```

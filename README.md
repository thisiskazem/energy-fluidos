# energy-fluidos
Small container to monitor the energy used/produced at home, using the BTicino energy logger, and to push data in Prometheus

git clone https://github.com/frisso/energy-fluidos.git

cd energy-fluidos

sudo docker build --pull -t energy .

sudo docker run -d energy

(to see the output)
sudo docker logs NUMBER

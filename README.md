# energy-fluidos
Small container to monitor the energy used/produced at home, using the BTicino energy logger, and to push data in Prometheus


## Docker Container Implementation

To run the energy-fluidos container, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/frisso/energy-fluidos.git
    ```

2. Change to the project directory:

    ```bash
    cd energy-fluidos
    ```

3. Build the Docker image:

    ```bash
    sudo docker build --pull -t energy .
    ```

4. Run the Docker container:

    ```bash
    sudo docker run -d -p 8000:8000 energy
    ```

5. To see the container logs, use the following command (replace `NUMBER` with your container ID):

    ```bash
    sudo docker logs NUMBER
    ```

## Port Forwarding for Prometheus

To access Prometheus UI, use Kubernetes port forwarding. Run the following command, replacing `<prometheus-service-name>` with the appropriate Prometheus service name:

```bash
kubectl port-forward -n monitoring svc/<prometheus-service-name> 9090:9090
```

This will forward the Prometheus UI to http://localhost:9090.

## Adding Docker Container as a Target in Prometheus

To configure Prometheus to scrape metrics from the energy-fluidos container, update your Prometheus configuration file with the following scrape configuration:

```yaml
global:
  scrape_interval: 15s  # Default scraping interval

scrape_configs:
  - job_name: "energy_monitoring"
    metrics_path: "/metrics"
    static_configs:
      - targets:
        - "<docker_ip>:8000"
```

Replace <docker_ip> with the IP address of your Docker container. This setup will enable Prometheus to scrape metrics from the energy-fluidos container.
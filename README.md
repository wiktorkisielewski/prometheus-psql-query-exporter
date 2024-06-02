# Prometheus SQL exporter

Expose SQL query results for porometheus.

## Helm deployment

```console
helm pull oci://registry-1.docker.io/wiktorkisielewski/prometheus-psql-exporter --version 0.1.0

helm install <my-release> oci://registry-1.docker.io/wiktorkisielewski/prometheus-psql-exporter --version 0.1.0
```
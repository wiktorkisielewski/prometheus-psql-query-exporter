# Prometheus SQL exporter

This is a tool made for exposing metrics based on SQL query results in prometheus format.

## Helm deployment

```console
helm pull oci://registry-1.docker.io/wiktorkisielewski/prometheus-psql-exporter --version 0.1.0

helm install <my-release> oci://registry-1.docker.io/wiktorkisielewski/prometheus-psql-exporter --version 0.1.0
```
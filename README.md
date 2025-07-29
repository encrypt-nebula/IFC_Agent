# IFC Agent

**IFC Agent** is an intelligent firewall control (IFC) agent designed to integrate with the Nebula networking stack for policy‑driven access control, group enforcement, and secure tunnel management. This tool runs alongside Nebula, enabling automated enforcement of network policies, host metadata management, and dynamic ACL updates.

---

## 🚀 Features

- **Dynamic policy enforcement**: Continuously monitors Nebula peer activity and applies up‑to‑date rules.
- **Certificate integration**: Uses Nebula certificates and group tags to categorize nodes and automatically generate firewall rules.
- **Audit logging**: Tracks host joins/leaves and policy changes for security visibility.
- **Configurable backend**: Support for Redis, PostgreSQL, or local file storage for state and metadata.
- **Cross‑platform compatible**: Written in Go—runs on Linux, macOS, and Windows.

---

## 📁 Repository Structure

```
.
├── cmd/
│   └── ifc-agent       # Agent CLI front‑end
├── internal/
│   └── backend/        # Storage drivers (Redis, Postgres, etc.)
├── pkg/
│   └── policy/         # Policy evaluation engine
│   └── nebula/         # Nebula status and peers API integration
├── config/
│   └── sample_config.yaml
├── scripts/
│   └── install.sh
├── Makefile            # Build, test, and packaging targets
└── README.md           
```

---

## 🧪 Installation

### Pre‑built binary

Download the latest release from [**Releases**](https://github.com/encrypt‑nebula/IFC_Agent/releases) and extract:

```bash
curl -LO https://github.com/encrypt-nebula/IFC_Agent/releases/download/vX.Y.Z/ifc-agent-vX.Y.Z-linux-amd64.tar.gz
tar -xzf ifc-agent-*.tar.gz
chmod +x ifc-agent
```

### Build from source

```bash
git clone https://github.com/encrypt-nebula/IFC_Agent.git
cd IFC_Agent
make build
# Binary will be in ./bin/ifc-agent
```

---

## ⚙️ Configuration

Create a configuration file (e.g. `config.yaml`) using the sample template:

```yaml
nebula:
  api_address: "127.0.0.1:4242"
  cert_path: "/etc/nebula/cert.pem"
policy:
  backend: "redis"
  redis:
    address: "localhost:6379"
    db: 0
acl:
  - group: "frontend"
    allow: ["group:backend"]
  - group: "backend"
    allow: ["group:database"]
```

---

## 🏃 Usage

```bash
./ifc-agent --config config/config.yaml
```

### CLI flags

| Flag               | Description                                          |
|--------------------|------------------------------------------------------|
| `--config`         | Path to agent config file                            |
| `--log-level`      | Logging verbosity (e.g. `info`, `debug`, `warn`)     |
| `--dry-run`        | Simulate policy application without enforcing rules   |
| `--metrics-addr`   | Expose metrics for Prometheus at specified HTTP addr  |

---

## 🧩 Policy Model

- Nodes authenticate via Nebula certificates.
- Each node is assigned labels/groups.
- Policies define allowed communication flows (e.g. `group:frontend → group:backend`).
- Agent updates local firewall (iptables, nftables) or cloud policy rules dynamically.

---

## 🧭 Example Deployments

### Redis backend

1. Install and configure Redis.
2. Store node metadata and policy configurations in Redis.
3. Launch `ifc-agent` pointing to Redis for read/write state.

### PostgreSQL / File backend

1. Switch backend in config (`backend: "postgres"` or `"file"`).
2. Adjust DB credentials or file path.
3. Launch agent as usual.

---

## 📊 Monitoring & Metrics

Enable metrics to monitor:

- Peer connections
- Policy evaluations
- Applied rule counts

Accessible via `/metrics` endpoint when `--metrics-addr` is used—compatible with Prometheus for dashboards and alerts.

---

## 🧪 Testing

```bash
make test         # Run unit tests
make fmt          # Format code
make lint         # Static analysis checks
```

---

## 🙌 Contributing

Contributions welcome! Please:

1. Fork the repo and create a branch.
2. Submit a PR with clear description of proposed change.
3. Ensure tests pass and maintain consistent code style.

---

## 📄 License

Licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.

---

## ℹ️ Contact & Support

For support or inquiries: open an issue or discussion on GitHub. You can also join the Nebula community Slack or forums for broader networking help.

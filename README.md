
# Username Syslog Generator

This script is designed to generate fake syslog messages for simulation and testing purposes. It can be used to simulate Palo Alto User-ID events or other similar scenarios. The generated syslog messages can be sent to a syslog server using UDP packets.

## Usage

1. Make sure you have Python installed on your system.
2. Install the required Python packages using the following command:

```bash
pip install faker
```

3. Run the script with the desired command-line arguments.
4. 
```bash
python fake_syslog_generator.py [options]
```

## Command-line Options

- `-d`, `--destination`: Destination IP address for syslog server.  (Default: localhost)
- `-n`, `--num_users`: Number of fake users to generate. (Default: 20)
- `--domain`: Domain name to be appended to generated server names. (Default: corp.com)
- `--network`: Subnet used for username mapping. (Default: 172.16.0.0/12)
- `--speed`: Rate at which logs are generated; options: slow, medium, fast. (Default: medium)

## Usage Examples

Generate fake syslog messages with a destination IP address:

```bash
python fake_syslog_generator.py -d 192.168.1.10 -n 20 --domain wigits.com
```

Generate fake syslog messages with a slower rate:

```bash
python fake_syslog_generator.py -d 192.168.1.10 --speed slow
```

## Palo Alto User-ID Filtering

To simulate Palo Alto User-ID events, you can apply filters to the generated syslog messages using regular expressions (regex) in either the NGFW or a User-ID agent.

### Regex

**Event Type - Login**
- Event Regex : `(Accepted password){1}`
- Username Regex: `Accepted password for (.*?)\s`
- Address Regex: `from (.*?)\s`

**Event Type - Logout**
- Event Regex : `(Disconnected from user ){1}`
- Username Regex: `Disconnected from user (.*?)\s`
- Address Regex: `Disconnected from user .*?\s(.*?)\s`

## Disclaimer

This script is intended for simulation and testing purposes only. Do not use it to generate actual logs on production systems.

## License

This project is licensed under the MIT License - see the [LICENSE](https://mit-license.org/) file for details.

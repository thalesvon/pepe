# Set up

### Clone Repository

```
git clone https://github.com/thalesvon/pepe.git
```

### Environment

Set [AWS Crendetials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config)

Get a set of ready to use functions (bash):
```bash
cd pepe/
source scripts.sh
```

# Available Commands

## help

Provides helpful information of available commands and how to interact with pepe.

*Syntax*: `help` or `help command`
## waf

Release IP address on given WAF location.

*Syntax*: `waf <location> <CIDR>`

*Tips*

- WAF Global: 

`aws waf list-ip-sets --query "IPSets[*]" | jq '.[] | "\(.Name) \(.IPSetId)"'`

- WAF Regional: 

`aws waf-regional list-ip-sets --query "IPSets[*]" --region us-east-1 | jq '.[] | "\(.Name) \(.IPSetId)"'`


## Tests

` pytest ./src/tests --cov-report term-missing --cov=./src/main/ip_release.py -vvv`
# Blockstack Click CLI

This is a POC for creating a blockstack-cli that maps all the endpoints on the [`blockstack api`](https://blockstack.github.io/blockstack-core/) to a cli with better ergonomics.

I've built this demo using the [`Click`](https://github.com/pallets/click) command line tool repository written in python. This will enable Blockstack to use prebuilt methods from `blockstack_client` to quickly fill out the functionality of the current CLI. I have only implemented the endpoints currently, but any python methods can be used under commands easily in this framework.

### Getting started

```
$ git clone git@github.com:jackzampolin/blockstack-cli.git && cd blockstack-cli
$ . venv/bin/activate
$ pip install --editable .
$ blockstack-cli --help
```

### Current Progress

All the endpoints have been implemented except the following:

```
$ blockstack-cli blockchain send_transaction
$ blockstack-cli wallet set_key
$ blockstack-cli wallet send
$ blockstack-cli gaia *
```

### Cool features

Try the `-debug` flag! It will print out the details of the request sent for troubleshooting!

Also cool is the `-fmt` flag. Outputs the returned data in `{json|yaml|toml}`!

### Future work

- [ ] Integrate [`pyinstaller`](https://pyinstaller.readthedocs.io/en/stable/operating-mode.html) to make builds for all OS
- [ ] Build different OS versions with the [`pyinstaller-docker`](https://github.com/cdrx/docker-pyinstaller/) images for mad convenience

To reach feature parity with the current `blockstack` cli the following work needs to be completed.

- [X] Make the top level `--host` and `--password` flags work as intended
- [X] Make all `--flags` configurable via `ENV` with a commonsense naming scheme (`BLOCKSTACK_CLI_HOST`, `BLOCKSTACK_CLI_DIRECTORY`, etc..)
- [X] Implement the `blockchain` commands with their proper methods
- [ ] Implement the `gaia` commands with their proper methods - Waiting per @jcnelson
- [X] Implement the `name` commands with their proper methods
- [X] Implement the `namespace` commands with their proper methods
- [X] Implement the `node` commands with their proper methods
- [X] Implement the `price` commands with their proper methods
- [X] Implement the `wallet` commands with their proper methods
- [X] Have commands for generating a config file and be able to set values programmatically, not interactively

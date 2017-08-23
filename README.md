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

All the endpoints have commands stubbed out with the arguments they need printing to console. I have only wired up two commands:

```
$ blockstack-cli node ping
$ blockstack-cli node config get 
```

These just output the raw JSON returned by `blockstack.blockstack_client.ping()` and `blockstack.blockstack_client.read_config_file()`.

### Future work

To reach feature parity with the current `blockstack` cli the following work needs to be completed.

- [ ] Make the top level `--host` and `--directory` flags work as intended (Or maybe just the `--directory` flag)
- [ ] Make all `--flags` configurable via `ENV` with a commonsense naming scheme (`BLOCKSTACK_CLI_HOST`, `BLOCKSTACK_CLI_DIRECTORY`, etc..)
- [ ] Implement the `blockchain` commands with their proper methods
- [ ] Implement the `gaia` commands with their proper methods
- [ ] Implement the `name` commands with their proper methods
- [ ] Implement the `namespace` commands with their proper methods
- [ ] Implement the `node` commands with their proper methods
- [ ] Implement the `price` commands with their proper methods
- [ ] Implement the `wallet` commands with their proper methods
- [ ] Add and implement the `blockstack api` command
